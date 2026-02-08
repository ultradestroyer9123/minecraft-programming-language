import os, json

os.chdir(os.path.dirname(os.path.abspath(__file__)))

start_cue = "# start of commands"
end_cue = "# end of commands"
tab_size = "        "
start = False
json_file = json.loads(open("commands.json", "r").read())

for line in open("mcParse.py", "r").read().split("\n"):
  if line == start_cue:
    start = True
  elif line == end_cue:
    break
  if start:
    if line.startswith(f"{tab_size}if ") or line.startswith(f"{tab_size}elif "):
      print(line)
      name = input("Name for command > ")
      if name == "":
         continue
      description = input("Description for command > ")
      json_file[name] = description

json_file = json.dumps(json_file, indent=2)
open("commands.json", "w").write(json_file)