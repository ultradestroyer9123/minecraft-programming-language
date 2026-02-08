import os, time, pyautogui, pyperclip, keyboard
import sys
import re
import traceback


def split_string_by_vars(text):
    parts = re.split(r"(\{.*?\})", text)
    return [part for part in parts if part]



def split_ignore_case(text, delimiter):
    # Escape delimiter in case it's a regex special char, and compile with re.IGNORECASE
    pattern = re.compile(re.escape(delimiter), re.IGNORECASE)
    return pattern.split(text)

os.chdir(os.path.dirname(__file__))
ORIGIN = []
MAX_CHAR_LIMIT_BEFORE_MANUAL = 230

settings = {
    'buildbutton': 'b',
    'output': 'keyboard',
}

variablesFor = "c"
selected_player = "@a"
current_x = 0
current_y = 0
current_z = 0
command_block_before_me = False
most_recent_if_command = ""
next_command_block_is_conditional = False
next_command_block_is_always_active = False
next_command_block_type = None
just_made_function = False
just_made_comment = False
recent_while_loop = {}
recent_function_name = ""
recent_comment = ""

armor_stand_tags = [
  "Invisible",
  "Invulnerable",
  "NoGravity",
  "Marker",
  "Small",
  "ShowArms",
  "DisabledSlots",
  "Silent",
  "NoBasePlate",
  "CustomNameVisible",
  "CustomName"
]
operations = ["%=","+=","-=","/=","*=","<",">","><","="]

commands_to_run = []
blocks = []
variables = []
functions = {}
event_listeners = {}
chunks = {}

def run_cmd_in_chat(cmd):
    pyperclip.copy(cmd)
    pyautogui.press('t', interval=0, _pause=False)
    time.sleep(0.05)
    pyautogui.hotkey('ctrl', 'v', interval=0, _pause=False)
    time.sleep(0.05)
    pyautogui.press('enter', interval=0, _pause=False)
    time.sleep(0.08)

def make_tellraw(text):
    global variablesFor
    formatted_text = split_string_by_vars(text)
    text_and_vars = []
    for items in formatted_text:
        if items.startswith("{") and items.endswith("}"):
            text_and_vars.append(r'{"score":{"name":"' + variablesFor + '","objective":"' + items[1:-1] + '"}}')
        else:
            text_and_vars.append(r'{"text":"' + items + '"}')
    return f"tellraw {selected_player} [" + ",".join(text_and_vars) + "]"


def create_cmd_block(cmd, typeOfBlock, conditional, always_active, use_single_quotes = False):
    global ORIGIN, current_x, current_y, current_z, command_block_before_me, next_command_block_is_conditional, next_command_block_type, just_made_function, recent_function_name, just_made_comment, recent_comment, next_command_block_is_always_active

    if always_active == "always":
        always_active = True
    elif always_active == "need":
        always_active = False

    if next_command_block_type != None:
        typeOfBlock = next_command_block_type
        next_command_block_type = None

    if conditional == "conditional" or next_command_block_is_conditional:
        conditional = 'true'
    else:
        conditional = 'false'

    string_sample = f"setblock {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {typeOfBlock}" + f'[facing=east,conditional={conditional}]' + "{Command:'" + cmd + "'" + f',auto:{always_active if command_block_before_me else "0b"}' + '}'

    if typeOfBlock == "impulse":
        typeOfBlock = "command_block"
    elif typeOfBlock == "chain":
        typeOfBlock = "chain_command_block"
    elif typeOfBlock == "repeating":
        typeOfBlock = "repeating_command_block"

    if always_active or next_command_block_is_always_active:
        always_active = '1b'
    else:
        always_active = '0b'
    if use_single_quotes:
        if len("/" + string_sample) > MAX_CHAR_LIMIT_BEFORE_MANUAL and settings['output'] == "keyboard":
            blocks.append(f"(MANUAL:{cmd})setblock {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {typeOfBlock}" + f'[facing=east,conditional={conditional}]' + "{" + f'auto:{always_active if command_block_before_me else "0b"}' + '}')
        else:
            blocks.append(f"setblock {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {typeOfBlock}" + f'[facing=east,conditional={conditional}]' + "{Command:'" + cmd + "'" + f',auto:{always_active if command_block_before_me else "0b"}' + '}')
    else:
        if len("/" + string_sample) > MAX_CHAR_LIMIT_BEFORE_MANUAL and settings['output'] == "keyboard":
            blocks.append(f"(MANUAL:{cmd})setblock {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {typeOfBlock}" + f'[facing=east,conditional={conditional}]' + "{" + f'auto:{always_active if command_block_before_me else "0b"}' + '}')
        else:
            blocks.append(f"setblock {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {typeOfBlock}" + f'[facing=east,conditional={conditional}]' + '{Command:"' + cmd + '"' + f',auto:{always_active if command_block_before_me else "0b"}' + '}')
    command_block_before_me = True
    next_command_block_is_conditional = False
    next_command_block_is_always_active = False
    if just_made_function:
        run_cmd('setblock ' + f"{str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y + 1)} {str(int(ORIGIN[2]) + current_z)}" + ' oak_sign[rotation=4]{front_text:{messages:["' + recent_function_name + r'","","",""]}}')
        just_made_function = False
    elif just_made_comment:
        run_cmd('setblock ' + f"{str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y + 1)} {str(int(ORIGIN[2]) + current_z)}" + ' oak_sign[rotation=4]{front_text:{messages:["' + recent_comment + r'","","",""]}}')
        just_made_comment = False
    current_x += 1

def run_cmd_before_everything(cmd):
    commands_to_run.append(cmd)

def run_cmd(cmd):
    blocks.append(cmd)

def run_function(name, conditional = False, stopping = False):
    if stopping:
        initiate_block = "air"
    else:
        initiate_block = "redstone_block"

    func = functions.get(name.lower())
    if func is None:
        print(f"Error: undefined function {name}")
        return
    x = str(func[0])
    y = str(func[1])
    z = str(func[2])
    create_cmd_block(f"setblock {x} {y} {z} {initiate_block} destroy", "chain" if command_block_before_me else "impulse", "conditional" if conditional else "unconditional", "always" if command_block_before_me else "need")
    create_cmd_block('kill @e[type=item,nbt={Item:{id:"minecraft:redstone_block"}}]', "chain", "unconditional", "always", use_single_quotes = True)


def run_coords(x, y, z):
    run_cmd(f"setblock {x} {y} {z} redstone_block destroy")
    run_cmd('kill @e[type=item,nbt={Item:{id:"minecraft:redstone_block"}}]')

def read_file(file):
    file = open(file, 'r')
    file_content = file.read()
    file.close()
    return file_content

file = split_ignore_case(read_file(sys.argv[1] if len(sys.argv) > 1 else "file.mcmd"),"\nexit")[0]

def input_global_string_variables(line):
    global variablesFor, selected_player
    line = line.replace(r"{variablesFor}", variablesFor)
    line = line.replace(r"{selectedPlayer}", selected_player)
    return line

def replace_int_variable(file, match, replaceWith):
    pattern = r"\{" + re.escape(match) + r"([^\}]*)\}"
    
    def replacer(m):
        expr = m.group(1)
        try:
            return str(round(eval(str(replaceWith) + expr)))
        except Exception as e:
            return m.group(0)  # if eval fails, keep original
    
    return re.sub(pattern, replacer, file)

visted_files = []
def recursive_import(file):
    global visited_files
    final = file
    for line in file.split("\n"):
        l = line.lower()
        if l.startswith("import "):
            imported_file = read_file(l.split(" ", 1)[1])
            if l.split(" ", 1)[1] in visted_files:
                print("Error: Circular import detected")
                exit()
            visted_files.append(l.split(" ", 1)[1])
            final = final.replace(line, recursive_import(imported_file) + "\nlayerup\n")
    return final

for line in file.split('\n'):
    l = line.lower()
    if l == "exit":
        break
    if l.startswith('origin '):
        ORIGIN = l.split(' ', 1)[1].replace(" ","").split(",")
    elif l.replace(" ","") == ".module=true":
        # stop expecting an origin if module
        break

file = recursive_import(file)

global_variables = {}
        


file = replace_int_variable(file, "origin_x", ORIGIN[0])
file = replace_int_variable(file, "origin_y", ORIGIN[1])
file = replace_int_variable(file, "origin_z", ORIGIN[2])

def if_variables_exist_run(line):
    global current_x, current_y, current_z, global_variables
    if r'{current_x' in line:
        line = replace_int_variable(line, "current_x", str(int(ORIGIN[0]) + int(current_x)))
    if r'{current_y' in line:
        line = replace_int_variable(line, "current_y", str(int(ORIGIN[1]) + int(current_y)))
    if r'{current_z' in line:
        line = replace_int_variable(line, "current_z", str(int(ORIGIN[2]) + int(current_z)))

    for value in global_variables:
        if r'{' + value in line:
            line = replace_int_variable(line, value, str(global_variables[value])) if str(global_variables[value]).isdigit else str(global_variables[value])
    return line

lineNumber = 0
# start of commands
lines = file.split('\n')
i = 0
while i < len(lines):
    try:
        line = lines[i]
        line = line.lstrip('\t')
        line = line.lstrip(' ')
        line = input_global_string_variables(line)
        lineNumber += 1
        line = if_variables_exist_run(line)
        l = line.lower()
        if l.startswith('origin '):
            ORIGIN = l.split(' ', 1)[1].replace(" ","").split(",")
        elif l.startswith('cmd '):
            l = line.split(' ', 1)[1].split(", ",3)
            if l[2].lower() == "always":
                l[2] = True
            else:
                l[2] = False
            create_cmd_block(l[3], l[0], l[1], l[2])
        elif l.startswith('cmd_manual '):
            l = line.split(' ', 1)[1]
            run_cmd(l)
        elif l.startswith('set '):
            line = line.split(' ', 1)[1]
            if ' to ' in l:
                line = line.split(" ")
                if line[0] not in variables:
                    create_cmd_block(f"scoreboard objectives add {line[0]} dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
                    create_cmd_block(f"scoreboard players set {variablesFor} {line[0]} {line[2]}", "chain", "unconditional", "always")
                    variables.append(line[0])
                else:
                    create_cmd_block(f"scoreboard players set {variablesFor} {line[0]} {line[2]}", "chain" if command_block_before_me else "impulse", "unconditional", "always")
            elif ' add ' in l:
                line = split_ignore_case(line, " add ")
                create_cmd_block(f"scoreboard players add {variablesFor} {line[0]} {line[1]}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            elif ' subtract ' in l:
                line = split_ignore_case(line, " subtract ")
                create_cmd_block(f"scoreboard players remove {variablesFor} {line[0]} {line[1]}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            elif l.split(" ")[2] in operations:
                operation = l.split(" ")[2]
                line = line.replace(" ", "").split(operation)
                create_cmd_block(f"scoreboard players operation {variablesFor} {line[0]} {operation} {variablesFor} {line[1]}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            else:
                if line not in variables:
                    create_cmd_block(f"scoreboard objectives add {line} dummy")
                    variables.append(line)
                else:
                    create_cmd_block(f"scoreboard players set {variablesFor} {line[0]} 0", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
        elif l == "next":
            current_x = 0
            current_z += 2
            command_block_before_me = False
        elif l.startswith("function "):
            line = line.split(' ', 1)[1]
            just_made_function = True
            recent_function_name = line
            current_x = 0
            current_z += 2
            command_block_before_me = False
            # store function names case-insensitively
            functions[line.lower()] = [int(ORIGIN[0]) - 1, int(ORIGIN[1]) + current_y, int(ORIGIN[2]) + current_z]
        elif l.startswith("chunk "):
            # Capture a named chunk: store its lines and skip executing them now.
            chunk_name = line.split(' ', 1)[1].strip().lower()
            j = i + 1
            chunk_lines = []
            while j < len(lines):
                if lines[j].strip().lower().startswith('endchunk'):
                    break
                chunk_lines.append(lines[j])
                j += 1
            if j >= len(lines):
                print(f"Error: unmatched chunk starting at line {lineNumber}")
                exit()
            chunks[chunk_name] = chunk_lines
            # remove the chunk definition (chunk .. endchunk) from active lines
            lines[i:j+1] = []
            # do not advance i; process the new line now at index i
            continue
        elif not l.startswith("stop ") and (l.endswith('()') or (l.endswith(')') and l.count('(') == 1 and l.split("(")[0] in functions)):
            if l.endswith("()") == False:
                parameters = line.split("(")[1].split(")")[0].replace(" ", "").split(",")
                for param in parameters:
                    key,value = param.split("=")
                    if value.isdigit():
                        create_cmd_block(f"scoreboard players set {variablesFor} {key} {value}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
                    else:
                        create_cmd_block(f"scoreboard players operation {variablesFor} {key} = {variablesFor} {value}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            line = line.split("(")[0]
            run_function(line)
        elif l == "run":
            run_coords(str(int(ORIGIN[0]) - 1), str(int(ORIGIN[1]) + current_y), str(int(ORIGIN[2]) + current_z))
        elif l == "clear":
            run_cmd(f"scoreboard players reset {variablesFor}")
        elif l.startswith("if "):
            if "then" in l:
                command = "execute if "
                line = split_ignore_case(split_ignore_case(line, "if")[1], " then")
                conditions = split_ignore_case(line[0], "and")
                command += " run execute if ".join(conditions).replace(r"{variablesFor}", variablesFor)
                create_cmd_block(command, "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            else:
                command = "execute if "
                original_line = line
                line = split_ignore_case(split_ignore_case(line, "if")[1], " run")
                conditions = split_ignore_case(line[0], "and")
                command += " run execute if ".join(conditions).replace(r"{variablesFor}", variablesFor) + " run " + original_line.split(" run ")[-1]
                create_cmd_block(command, "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            most_recent_if_command = command
        elif l.startswith("variablesFor "):
            variablesFor = l.split(' ', 1)[1]
        elif l == "goback":
            current_x = 0
            current_z -= 2
            command_block_before_me = False
        elif l == "cleararea":
            run_cmd_before_everything(f"fill {str(int(ORIGIN[0])-1)} {str(int(ORIGIN[1]))} {str(int(ORIGIN[2])-1)} {str(int(ORIGIN[0])+40)} {str(int(ORIGIN[1])+10)} {str(int(ORIGIN[2])+40)} minecraft:air")
        elif l == "exit":
            break
        elif l.startswith("random "):
            l = line.split(' ', 1)[1]
            variable, min, max = l.split(", ")
            if variable not in variables:
                create_cmd_block(f"scoreboard objectives add {variable} dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
                variables.append(variable)
            create_cmd_block(f"execute store result score {variablesFor} {variable} run random value {min}..{max}", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
        elif l == "[conditional]":
            next_command_block_is_conditional = True
        elif l == "[unconditional]":
            next_command_block_is_conditional = False
        elif l == "[alwaysactive]":
            next_command_block_is_always_active = True
        elif l == "[needredstone]":
            next_command_block_is_always_active = False
        elif l == "[repeating]" or l == "[chain]" or l == "[impulse]":
            next_command_block_type = l[1:-1]
        elif l.startswith("armorstand "):
            line = split_ignore_case(line, " ")[1:]
            l = l.split(" ")[1:]
            if l[0] == "create":
                tag = line[1]
                x = l[2]
                y = l[3]
                z = l[4]
                try:
                    customData = line[5]
                except:
                    customData = ""
                command = f"summon armor_stand {x} {y} {z} "
                if customData != "":
                    command += '{Tags:["' + tag + '"],' + f'{customData}' + '}'
                else:
                    command += '{Tags:["' + tag + '"]}'
                    
                create_cmd_block(command, "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need", use_single_quotes=True)
            elif l[0] == "remove":
                tag = line[1]
                create_cmd_block(f'kill @e[type=minecraft:armor_stand,tag={tag}]', "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            elif l[0] == "move":
                tag = line[1]
                x = l[2]
                y = l[3]
                z = l[4]
                create_cmd_block(f'execute as @e[type=minecraft:armor_stand,tag={tag}] at @s run tp @s {x} {y} {z}', "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            elif l[0] == "run":
                tag = line[1]
                command = " ".join(line[2:])
                create_cmd_block(f'execute as @e[type=minecraft:armor_stand,tag={tag}] at @s run {command}', "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
        elif l.startswith("say "):
            l = line.split(' ', 1)[1]
            create_cmd_block(str(make_tellraw(l)), "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need", use_single_quotes=True)
        elif l.startswith("' "):
            just_made_comment = True
            recent_comment = line.split("' ")[1]
        elif l == "space":
            current_x += 1
        elif l == "backspace":
            current_x -= 1
        elif l == "layerup":
            current_x = 0
            current_y += 2
            current_z = 0
            command_block_before_me = False
        elif l == "layerdown":
            current_x = 0
            current_y -= 2
            current_z = 0
            command_block_before_me = False
        elif l.startswith("timer "): 
            line = line.split(" ")
            duration = int(line[1]) - 2
            if line[2]:
                typeOfDuration = line[2]
            else:
                typeOfDuration = "ticks"
            
            if typeOfDuration == "seconds":
                duration *= 20
            elif typeOfDuration == "minutes":
                duration *= 20 * 60
            elif typeOfDuration == "hours":
                duration *= 20 * 60 * 60
            elif typeOfDuration == "days":
                duration *= 20 * 60 * 60 * 24
            elif typeOfDuration == "years":
                duration *= 20 * 60 * 60 * 24 * 365
            elif typeOfDuration == "ticks":
                pass

            create_cmd_block(f"scoreboard objectives add sys.timer dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            create_cmd_block(f"scoreboard players set {variablesFor} sys.timer {duration}", "chain", "unconditional", "always")
            run_cmd(f"fill {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {str(int(ORIGIN[0]) + current_x + 7)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air")
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) + current_x + 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} redstone_block destroy", "chain", "unconditional", "always")
            current_x += 2
            create_cmd_block(f"execute if score {variablesFor} sys.timer matches 1.. run scoreboard players remove {variablesFor} sys.timer 1", "repeating", "unconditional", "need")
            create_cmd_block(f"execute if score {variablesFor} sys.timer matches 0 run setblock {str(int(ORIGIN[0]) + current_x - 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air", "chain", "unconditional", "always")
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) + current_x + 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} redstone_block destroy", "chain", "conditional", "always")
            current_x += 2
            command_block_before_me = False
        elif l == "clearLine":
            run_cmd(f"fill {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {str(int(ORIGIN[0]) + current_x + 25)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air")
        elif l.startswith("clearLine "):
            amount = l.split(" ")[1]
            run_cmd(f"fill {str(int(ORIGIN[0]) + current_x)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} {str(int(ORIGIN[0]) + current_x + int(amount))} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air")
        elif l == "else":
            create_cmd_block(most_recent_if_command.replace("execute if", "execute unless"), "chain", "unconditional", "always")
        elif l.startswith("isholding "):
            just_made_function = True
            line = line.split(' ', 3)
            item = line[1]
            recent_function_name = line[2]
            current_x = 0
            current_z += 2
            command_block_before_me = False

            create_cmd_block(f"execute as {selected_player}[nbt=" + "{SelectedItem:{id:'minecraft:" + item + "'}}]" + f" run {line[3]}", "repeating", "unconditional", "need")
        elif l.startswith("currentplayer "):
            selected_player = line.split(' ', 1)[1]
        elif l == "runnextrow":
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) - 1)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z + 2)} redstone_block destroy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
        elif l.startswith("waitfor "):
            create_cmd_block(f"scoreboard objectives add sys.waitfor dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            create_cmd_block(f"scoreboard players set {variablesFor} sys.waitfor 0", "chain", "unconditional", "always")
            line = line.split(' ')[1:]
            waitingFor = line[0].lower()
            if waitingFor == "block":
                waitingFor, blockOrScore, x, y, z, eventName = line
            elif waitingFor == "score":
                waitingFor, blockOrScore, value, eventName = line

            command_block_before_me = False
            just_made_function = True
            current_x = 0
            current_z += 2
            recent_function_name = eventName
            functions[eventName] = [int(ORIGIN[0]) - 1, int(ORIGIN[1]) + current_y, int(ORIGIN[2]) + current_z]
            if waitingFor == "block":
                create_cmd_block(f"execute if score {variablesFor} sys.waitfor matches 0 run execute if block {x} {y} {z} {blockOrScore} run setblock {str(int(ORIGIN[0]) + current_x + 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} redstone_block", "repeating", "unconditional", "need")
            elif waitingFor == "score":
                create_cmd_block(f"execute if score {variablesFor} sys.waitfor matches 0 run execute if score {variablesFor} {blockOrScore} matches {value} run setblock {str(int(ORIGIN[0]) + current_x + 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} redstone_block", "repeating", "unconditional", "need")

            current_x += 2
            command_block_before_me = False
            if waitingFor == "block":
                create_cmd_block(f"setblock {x} {y} {z} air", "impulse", "unconditional", "need")
            create_cmd_block(f"scoreboard players set {variablesFor} sys.waitfor 1" , "chain" if waitingFor == "block" else "impulse", "unconditional", "always" if waitingFor == "block" else "need")
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) + current_x - 2)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air", "chain", "unconditional", "always")
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) - 1)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)} air", "chain", "unconditional", "always")
        elif l.startswith("waituntil "):
            cond = line.split(" ", 1)[1].strip()
            # create a debounce objective so the trigger only fires once
            create_cmd_block(f"scoreboard objectives add sys.debounce dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            create_cmd_block(f"scoreboard players set {variablesFor} sys.debounce 0", "chain", "unconditional", "always")

            # Reserve space for the trigger redstone block
            create_cmd_block(f"setblock ~2 ~ ~ redstone_block", "chain", "unconditional", "always")
            current_x += 2

            # Build the repeating check that fires the trigger when the condition is true and debounce is 0
            # If the condition already starts with 'execute', use it directly, otherwise prefix with 'execute if '
            cond_prefix = cond if cond.lower().startswith("execute") else f"execute if {cond}"
            check_cmd = f"{cond_prefix} if score {variablesFor} sys.debounce matches 0 run setblock ~2 ~ ~ redstone_block"
            create_cmd_block(check_cmd, "repeating", "unconditional", "need")
            current_x += 2

            create_cmd_block(f"scoreboard players set {variablesFor} sys.debounce 1", "impulse", "unconditional", "need")
            create_cmd_block(f"setblock ~-5 ~ ~ air", "chain", "unconditional", "always")
            create_cmd_block(f"setblock ~-3 ~ ~ air", "chain", "unconditional", "always")
            command_block_before_me = True
        elif l.startswith("while "):
            line = line.split(' ', 1)[1]
            iteration_variable, operation, goal = line.split(" ")
            iteration_variable,valueOfIteration = iteration_variable.split("=")
            create_cmd_block(f"scoreboard objectives add {iteration_variable} dummy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")
            create_cmd_block(f"scoreboard players set {variablesFor} {iteration_variable} {valueOfIteration}", "chain", "unconditional", "always")
            
            create_cmd_block(f"setblock {str(int(ORIGIN[0]) - 1)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z + 2)} redstone_block destroy", "chain" if command_block_before_me else "impulse", "unconditional", "always" if command_block_before_me else "need")

            current_x = 0
            current_z += 2
            command_block_before_me = False
            recent_while_loop = {"iteration_variable": iteration_variable, "operation": operation, "goal": goal, "xyz": f"{str(int(ORIGIN[0]) - 1)} {str(int(ORIGIN[1]) + current_y)} {str(int(ORIGIN[2]) + current_z)}"}
            create_cmd_block(f"execute if score {variablesFor} {iteration_variable} {operation} {variablesFor} {goal}", "repeating", "unconditional", "need")
        elif l == "endwhile":
            create_cmd_block(f"execute unless score {variablesFor} {recent_while_loop['iteration_variable']} {recent_while_loop['operation']} {variablesFor} {recent_while_loop['goal']} run setblock {recent_while_loop['xyz']} air", "chain", "unconditional", "always")
        elif l.startswith("repeat "):
            # expand the block between repeat .. endrepeat count times, supporting nesting
            try:
                count = int(line.split(' ', 1)[1])
            except Exception:
                print(f"Error: invalid repeat count on line {lineNumber}")
                exit()

            # find matching endrepeat, accounting for nested repeats
            depth = 1
            j = i + 1
            while j < len(lines) and depth > 0:
                lj = lines[j].strip().lower()
                if lj.startswith("repeat "):
                    depth += 1
                elif lj == "endrepeat":
                    depth -= 1
                j += 1

            if depth != 0:
                print(f"Error: unmatched repeat starting at line {lineNumber}")
                exit()

            # inner block is lines i+1 .. j-2 (because j-1 was the matching endrepeat)
            inner = lines[i+1:j-1]

            # build repeated sequence
            repeated = []
            for _ in range(count):
                # append a shallow copy of each inner line
                for itm in inner:
                    repeated.append(itm)

            # replace slice from current repeat line through the endrepeat with the repeated lines
            lines[i:j] = repeated
            # do not advance i; process the newly-inserted line at index i next
            continue
        elif l == "endrepeat":
            # standalone endrepeat (should be handled by repeat expansion) - skip
            i += 1
            continue
        elif l.startswith(".buildbutton="):
            l = l.split("=")[1]
            settings['buildbutton'] = l
        elif l.startswith(".output="):
            l = l.split("=")[1]
            settings["output"] = l
        elif l.startswith("@"):
            l = line.split(" ")
            variable_name = l[0]
            variable_operation = l[1]
            variable_value = l[2]
            if variable_operation == "=" and (variable_value.startswith('"') or variable_value.startswith("'")):
                global_variables[variable_name] = variable_value[1:-1]
            elif variable_operation == "=":
                global_variables[variable_name] = int(variable_value)
            elif variable_operation == "+=":
                global_variables[variable_name] += int(variable_value)
            elif variable_operation == "-=":
                global_variables[variable_name] -= int(variable_value)
            elif variable_operation == "*=":
                global_variables[variable_name] *= int(variable_value)
            elif variable_operation == "/=":
                global_variables[variable_name] /= int(variable_value)
            elif variable_operation == "%=":
                global_variables[variable_name] %= int(variable_value)
        elif l.startswith("#"):
            # Import a previously defined chunk inline at this location.
            chunk_name = l[1:].strip().lower()
            if chunk_name not in chunks:
                print(f"Error: undefined chunk {chunk_name} on line {lineNumber}")
                exit()
            # replace the single `#name` line with the chunk's lines
            lines[i:i+1] = chunks[chunk_name].copy()
            # do not advance i; process the first inserted line next
            continue
        elif l.startswith("stop "):
            l = l[5:].split("(")[0]
            run_function(l, stopping=True)


        # advance to next line unless a branch used `continue`
        i += 1
    except Exception as e:
        traceback.print_exc()
        print("Error: " + line + f", line {str(lineNumber)}")
        exit()

# end of commands

if settings['output'] == "keyboard":
    keyboard.wait(settings['buildbutton'])



sleepTime = 0.08
given_manual_warning = False

file_data = []


for command in commands_to_run:
    if settings['output'] == "keyboard":
        run_cmd_in_chat("/" + command)
    else:
        file_data.append(command)



for block in blocks:
    if settings['output'] == "keyboard":
        if block.startswith("(MANUAL:"):
            cmd = block.split("(MANUAL:")[1].split(")setblock")[0]
            block = "setblock" + block.split(")setblock")[1]
            run_cmd_in_chat("/" + block)
            x,y,z = block.split(" ")[1:4]
            z = str(int(z)+1)

            run_cmd_in_chat(f"/tp @s {x} {y} {z} 180 65")
            if not given_manual_warning:
                print("Warning: Manual command blocks detected, please face north and look at pitch 50 - 74 before 3 seconds")
                run_cmd_in_chat("/say Manual command blocks detected, please face north and look at pitch 50 - 74 before 3 seconds")
                given_manual_warning = True
            pyperclip.copy(cmd)
            time.sleep(0.15)
            pyautogui.rightClick(interval=0, _pause=False)
            time.sleep(0.15)
            pyautogui.hotkey('ctrl', 'v', interval=0, _pause=False)
            time.sleep(0.15)
            pyautogui.press('enter', interval=0, _pause=False)
            time.sleep(0.15)
        else:
            run_cmd_in_chat("/" + block)
    elif settings['output'] == 'clipboard' or settings['output'] == 'both' or settings['output'] == 'file':
        file_data.append(block)

if settings['output'] == 'clipboard' or settings['output'] == 'both':
    pyperclip.copy("\n".join(file_data))
if settings['output'] == 'file' or settings['output'] == 'both':
    with open("output.mcfunction", "w") as f:
        f.write("\n".join(file_data))