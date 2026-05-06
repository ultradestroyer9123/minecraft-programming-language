from pygltflib import GLTF2
import sys
import os
import numpy as np


os.chdir(os.path.dirname(__file__))

filename = "Untitled.glb"
nodes = None
cubes = {}

create_cube_commands = []
orient_cube_commands = ["function form_model_%s" % filename.split(".")[0], "	cmd impulse, unconditional, need, say this is a filler command, modify"]
 
def _safe_list(x, default):
	return list(x) if x is not None else default


def get_node_info(gltf):
	result = {}
	nodes_list = gltf.nodes or []
	if not nodes_list:
		debug_lines.append("No nodes found in GLB.")
		return result

	# build parent map (gltf nodes only list children)
	parent = {i: None for i in range(len(nodes_list))}
	for i, n in enumerate(nodes_list):
		if getattr(n, 'children', None):
			for c in n.children:
				parent[c] = i

	debug_lines.append("\n--- DEBUG: All GLTF Nodes ---")
	for i, node in enumerate(nodes_list):
		raw_name = node.name or f"node_{i}"
		translation = _safe_list(node.translation, [0, 0, 0])
		scale = _safe_list(node.scale, [1, 1, 1])
		rotation = _safe_list(node.rotation, [0, 0, 0, 1])
		debug_lines.append(f"Node {i}: name={raw_name}, translation={translation}, scale={scale}, rotation={rotation}")

	def node_world_matrix(idx):
		# recursively compute world matrix for node index
		mats = []
		cur = idx
		while cur is not None:
			n = nodes_list[cur]
			if getattr(n, 'matrix', None) is not None and any(n.matrix):
				m = np.array(n.matrix, dtype=float).reshape((4, 4))
			else:
				t = _safe_list(n.translation, [0, 0, 0])
				s = _safe_list(n.scale, [1, 1, 1])
				r = _safe_list(n.rotation, [0, 0, 0, 1])
				m = trs_to_matrix(t, r, s)
			mats.append(m)
			cur = parent.get(cur)
		# multiply from root down: M_root * ... * M_node
		M = np.eye(4)
		for m in reversed(mats):
			M = M @ m
		return M

	def trs_to_matrix(t, q, s):
		# build 4x4 matrix from translation t, quaternion q, scale s
		t = np.array(t, dtype=float)
		s = np.array(s, dtype=float)
		x, y, z, w = q[0], q[1], q[2], q[3]
		# quaternion to rotation matrix
		R = np.array([
			[1 - 2*(y*y+z*z), 2*(x*y - z*w),     2*(x*z + y*w)],
			[2*(x*y + z*w),     1 - 2*(x*x+z*z), 2*(y*z - x*w)],
			[2*(x*z - y*w),     2*(y*z + x*w),   1 - 2*(x*x+y*y)]
		], dtype=float)
		# apply scale
		R = R * s.reshape((1, 3))
		M = np.eye(4, dtype=float)
		M[:3, :3] = R
		M[:3, 3] = t
		return M

	def transform_aabb(M, minv, maxv):
		# transform 8 corners and compute world min/max
		corners = []
		for xi in (minv[0], maxv[0]):
			for yi in (minv[1], maxv[1]):
				for zi in (minv[2], maxv[2]):
					v = np.array([xi, yi, zi, 1.0], dtype=float)
					vt = M @ v
					corners.append(vt[:3])
		corners = np.array(corners)
		minw = corners.min(axis=0).tolist()
		maxw = corners.max(axis=0).tolist()
		centerw = ((corners.max(axis=0) + corners.min(axis=0)) / 2.0).tolist()
		sizew = (corners.max(axis=0) - corners.min(axis=0)).tolist()
		return minw, maxw, centerw, sizew
	for i, node in enumerate(nodes_list):
		raw_name = node.name or f"node_{i}"
		name = raw_name  # Use full name for uniqueness
		translation = _safe_list(node.translation, [0, 0, 0])
		scale = _safe_list(node.scale, [1, 1, 1])
		rotation = _safe_list(node.rotation, [0, 0, 0, 1])
		block = raw_name.split(".")[0] if raw_name != "Origin" else "air"
		info = {
			"block": block,
			"translation": [float(x) for x in translation],
			"scale": [float(x) for x in scale],
			"rotation": [float(x) for x in rotation],
		}
		# if node references a mesh, try to read POSITION accessor min/max for AABB
		try:
			mesh_idx = node.mesh
			if mesh_idx is not None:
				mesh = gltf.meshes[mesh_idx]
				if mesh.primitives:
					prim = mesh.primitives[0]
					attr = getattr(prim.attributes, 'POSITION', None)
					if attr is not None:
						acc = gltf.accessors[attr]
						if getattr(acc, 'min', None) is not None and getattr(acc, 'max', None) is not None:
							minv = [float(x) for x in acc.min]
							maxv = [float(x) for x in acc.max]
							# compute local aabb center/size
							center = [(a + b) / 2.0 for a, b in zip(minv, maxv)]
							size = [b - a for a, b in zip(minv, maxv)]
							# compute world transform for this node index i
							M = node_world_matrix(i)
							minw, maxw, centerw, sizew = transform_aabb(M, minv, maxv)
							info['aabb_min'] = minv
							info['aabb_max'] = maxv
							info['aabb_center'] = center
							info['aabb_size'] = size
							info['world_aabb_min'] = minw
							info['world_aabb_max'] = maxw
							info['world_aabb_center'] = centerw
							info['world_aabb_size'] = sizew
		except Exception:
			# be forgiving; if anything fails just skip accessor-based AABB
			pass
		result[name] = info
		debug_lines.append(f"  -> Parsed node '{name}': block={block}, translation={translation}, scale={scale}, rotation={rotation}")
		if 'aabb_min' in info:
			debug_lines.append(f"     AABB local min={info['aabb_min']}, max={info['aabb_max']}, center={info['aabb_center']}, size={info['aabb_size']}")
			debug_lines.append(f"     AABB world min={info['world_aabb_min']}, max={info['world_aabb_max']}, center={info['world_aabb_center']}, size={info['world_aabb_size']}")
	return result
		
def convert_into_cubes(nodes_dict):
	global cubes
	cubes = {}
	name_counters = {}

	# compute origin translation (if an Origin node exists) so we can
	# make all cube positions relative to that origin
	origin_translation = nodes_dict.get("Origin", {}).get("translation", [0.0, 0.0, 0.0])

	debug_lines.append("\n--- DEBUG: Converting Nodes to Cubes ---")
	for base_name, info in nodes_dict.items():
		translation = info.get("translation", [0, 0, 0])
		scale = info.get("scale", [1, 1, 1])
		rotation = info.get("rotation", [0, 0, 0, 1])

		debug_lines.append(f"Node '{base_name}': original translation={translation}, scale={scale}, rotation={rotation}")
		debug_lines.append(f"  Origin translation: {origin_translation}")

		# Use absolute sizes for division
		abs_scale = [abs(float(s)) for s in scale]

		# determine cube size as the minimum non-zero scale component
		non_zero = [s for s in abs_scale if s > 1e-9]
		if non_zero:
			cube_size = min(non_zero)
		else:
			cube_size = 1.0

		# build per-axis size lists (fix: always at least one cube per axis, remainder goes to last)
		sizes_per_axis = []
		for axis_len in abs_scale:
			if axis_len <= 1e-9:
				sizes_per_axis.append([0.0])
				continue
			base_count = int(axis_len // cube_size)
			remainder = axis_len - (base_count * cube_size)
			if base_count == 0:
				sizes = [axis_len]
			else:
				sizes = [cube_size] * base_count
				if remainder > 1e-9:
					sizes.append(remainder)
			sizes_per_axis.append(sizes)

		debug_lines.append(f"  Axis division: sizes_per_axis={sizes_per_axis}")

		# compute start corner (assume translation is center)
		start_corner = [translation[i] - abs_scale[i] / 2.0 for i in range(3)]
		debug_lines.append(f"  Start corner: {start_corner}")

		# iterate through grid and create cubes
		for ix, sx in enumerate(sizes_per_axis[0]):
			for iy, sy in enumerate(sizes_per_axis[1]):
				for iz, sz in enumerate(sizes_per_axis[2]):
					# compute center for this cube
					x_off = sum(sizes_per_axis[0][:ix]) + sx / 2.0
					y_off = sum(sizes_per_axis[1][:iy]) + sy / 2.0
					z_off = sum(sizes_per_axis[2][:iz]) + sz / 2.0
					cx = start_corner[0] + x_off
					cy = start_corner[1] + y_off
					cz = start_corner[2] + z_off

					# unique naming per base_name
					idx = name_counters.get(base_name, 0) + 1
					name_counters[base_name] = idx
					cube_name = f"{base_name}_{idx}" if base_name != "Origin" else "Origin"

					# Use a single scalar for cube scale (cube side length).
					# Take the average of the three axis lengths to produce a single decimal.
					cube_side = float((sx + sy + sz) / 3.0)
					# make translation relative to Origin node
					rel_tx = float(cx - origin_translation[0])
					rel_ty = float(cy - origin_translation[1])
					rel_tz = float(cz - origin_translation[2])
					cubes[cube_name] = {
						"block": info.get("block", "air"),
						"translation": [rel_tx, rel_ty, rel_tz],
						"scale": cube_side,
						"rotation": rotation,
					}
					debug_lines.append(f"    Cube '{cube_name}': center=({cx}, {cy}, {cz}), rel=({rel_tx}, {rel_ty}, {rel_tz}), scale={cube_side}, rotation={rotation}")

	debug_lines.append(f"  -> Total cubes created: {len(cubes)}")
	return cubes

def output_commands():
	with open(f"output.mcmd", "w") as f:
		for cmd in create_cube_commands:
			f.write(cmd + "\n")
		for cmd in orient_cube_commands:
			f.write(cmd + "\n")

	f.close()
	

def main(path="Untitled.glb"):
	global debug_lines
	debug_lines = []
	# Try working directory first, then script parent
	if not os.path.exists(path):
		alt = os.path.join(os.path.dirname(__file__), "..", path)
		alt = os.path.normpath(alt)
		if os.path.exists(alt):
			path = alt
	if not os.path.exists(path):
		print(f"GLB file not found: {path}")
		sys.exit(2)
	gltf = GLTF2().load(path)
	print(f"Loaded: {path}")
	nodes = get_node_info(gltf)
	debug_lines.append("\n--- DEBUG: Node Info Dictionary ---")
	for n, d in nodes.items():
		debug_lines.append(f"  {n}: {d}")
	cubes = convert_into_cubes(nodes)
	debug_lines.append("\n--- DEBUG: Final Cubes Dictionary ---")
	for n, d in cubes.items():
		debug_lines.append(f"  {n}: {d}")
	def blender_to_minecraft_coords(vec):
		# Blender: X (right), Y (forward), Z (up)
		# Minecraft: X (east), Y (up), Z (south)
		# Swap Blender Y and Z for Minecraft, and round early
		x, y, z = vec
		return [round(x, 3), round(y, 3), round(z, 3)]

	for name, info in cubes.items():
		block = info['block']
		translation = info["translation"]
		# Round and swap axes for Minecraft (upright)
		mc_translation = blender_to_minecraft_coords(translation)
		# Swap Y and Z for upright orientation
		x_pos = mc_translation[0]
		y_pos = mc_translation[2]
		z_pos = mc_translation[1]

		scale = round(info["scale"], 3)
		rotation = info["rotation"]

		create_cube_commands.append('cmd_manual summon armor_stand ~ ~ ~ {NoGravity:1b,Silent:1b,Invulnerable:1b,Marker:1b,Invisible:1b,NoBasePlate:1b,Tags:["%s","%s"],attributes:[{id:"minecraft:scale",base:%s}],equipment:{head:{id:"minecraft:%s",count:1}}}' % (name, filename.split(".")[0], scale, block))

		orient_cube_commands.append('  cmd chain, unconditional, always, execute at @e[type=armor_stand,tag=Origin,tag=%s,limit=1] run tp @e[type=minecraft:armor_stand,tag=%s,limit=1] ^%s ^%s ^%s facing ^ ^ ^10000' % (filename.split(".")[0], name, x_pos, z_pos, y_pos))
		debug_lines.append(f"{name}: B={block}, T={translation} (MC: {[x_pos, y_pos, z_pos]}), S={scale}, R={rotation}")
	output_commands()

	# Write debug output to debug.txt
	debug_path = os.path.join(os.path.dirname(__file__), 'debug.txt')
	with open(debug_path, 'w') as dbg:
		dbg.write('\n'.join(debug_lines))
	

if __name__ == "__main__":
	arg = sys.argv[1] if len(sys.argv) > 1 else filename
	main(arg)

