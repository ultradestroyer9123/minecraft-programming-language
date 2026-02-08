# 🧾 Custom Minecraft Command Block Script Language — Functionality Guide

This scripting engine is designed to convert a custom, readable syntax into Minecraft `setblock` commands that build **command block machines** in your world.

Use this file as a **reference guide** to understand what each part of the scripting engine does and how to build your own scripts.

---

## ⚙️ Base System & Context

### ✅ Key Settings and Internal State

| Variable | Purpose |
|----------|---------|
| `.buildbutton=b` | Sets the default build trigger/button key. |
| `.output=(keyboard <- default, clipboard, file, both <- clipboard & file)` | Sets the way the file is outputted when pressing the build button. |
| `.module=true` | Sets file to module file. |
| `variablesFor = "c"` | The default entity/player for scoreboard variables. |
| `selected_player = "@a"` | The default target for commands like `say`, `tellraw`, etc. |
| `current_x/y/z = 0` | Internal cursor to track where command blocks are placed. |
| `origin_x/y/z` | The base offset for all coordinates, set using `origin x,y,z`. |
| `just_made_function`, `just_made_comment` | Flags for placing visible labels (as signs) above blocks. |
| `armor_stand_tags[]` | Predefined tags used when spawning armor stands. |
| `operations[]` | Supported operators in variable expressions. |

---

## 📘 Why You Should Build a Guide File

Because this scripting system supports **custom syntax**, **dynamic control flow**, and even **modular file imports**, it’s highly beneficial to create a **reference guide file** that lists:

1. **All supported commands** with examples.
2. **What each function in your code does**.
3. **Common variables** you might access like `{current_x}` or `{origin_x}`.
4. **Macros or custom behaviors** you've defined in your own logic.

> 🛠️ This can double as **documentation and a test file**, letting you explore or demonstrate what each command will build in-game.

---

## 🛠️ Functional Categories

### 1. 📍 Position & Layout

| Command | Description |
|--------|-------------|
| `origin x,y,z` | Sets base coordinates (`ORIGIN`). |
| `next`, `goback` | Moves Z forward/backward. |
| `layerup`, `layerdown` | Adjusts the current Y level. |
| `space`, `backspace` | Moves X forward/backward. |
| `cleararea`, `clearLine [N]` | Removes blocks in a region. |

---

### 2. ⛏️ Command Blocks

| Command | Description |
|--------|-------------|
| `cmd <command>, <type>, <condition>, <alwaysActive>` | Places a command block with full control. |
| `[conditional]`, `[alwaysactive]` | Flags that modify how the *next* command block behaves. |
| `[repeating/impulse/chain]` | Flags that modify the *next* type of the command block. |
| `say <msg>` | Adds a `tellraw` block, with scoreboard variable injection support. |
| `cmd_manual <command>` | Runs the command through chat and not in a command block. |

---

### 3. 📊 Scoreboard & Variables

| Command | Description |
|--------|-------------|
| `set A to 5` | `scoreboard players set` |
| `set A add 1` | `scoreboard players add` |
| `set A subtract 1` | `scoreboard players remove` |
| `set A = B` | `scoreboard players operation A = B` |
| `clear` | Resets scores for `variablesFor`. |
| `random A, min, max` | Gives `A` a random value in range. |

---

### 4. 🤖 Functions & Flow

| Command | Description |
|--------|-------------|
| `function name` | Creates a callable command sequence. |
| `name()` / `name(args)` | Calls a previously defined function. |
| `chunk name` | Used primarily for readability, puts code into wherever its called. |
| `endchunk` | Ends chunk. |
| `#name` | Imports a chunk. |
| `run`, `runnextrow` | Triggers command chains with redstone. |
| `stop (function_name)` | Clears any redstone blocks on that function's first command block. |
| `exit` | Stops parsing the rest of the file. |

---

### 5. 🔁 Control Flow

| Command | Description |
|--------|-------------|
| `if ... and ... then` | Begins a conditional block. |
| `if ... and ... run {command}` | Runs the command in the same if command block. |
| `else` | Alternate branch for the previous `if`. |
| `while A < B` | Starts a scoreboard-based loop. |
| `endwhile` | Ends the loop. |
| `repeat x` | Repeat the commands x amount of times. |
| `endrepeat` | Ends selection to repeat. |
| `timer {duration} {type: ticks/seconds/minutes/hours/days/years}` | Wait for x amount of time |
| `waitFor {block/score} {variable} {supposed to equal} {function name}` | Wait for x amount of time |
| `waitUntil {variablesFor} {variable} {operation} [{value}/{variablesFor} {variable}]` | Waits until operation is true to move onto next |
---

### 6. 🧍 Armor Stands

| Command | Description |
|--------|-------------|
| `armorstand create TAG x y z [NBT]` | Spawns armor stand. |
| `armorstand move TAG x y z` | Teleports armor stand. |
| `armorstand run TAG command` | Executes from stand's location. |
| `armorstand remove TAG` | Deletes armor stand by tag. |

---

### 7. 👂 Event Listeners

| Command | Description |
|--------|-------------|
| `currentPlayer {playerName}` | Sets current player for event listeners. |
| `isHolding {item} {event function name} {command}` | Detects when current player holds certain item. |
---

### 8. 🧭 Coordinate Substitution

This scripting engine supports dynamic variables in commands.

You can include expressions like:

- `{current_x+2}`
- `{origin_z+5}`
- `{@globalVariable+1}`

*(Unless that global variable is a string!)*

These are automatically evaluated and substituted via `replace_int_variable()`.

---

## 🧩 File & Import System

- **`import filename`**: Includes other `.mcmd` files.
- Prevents **circular imports**.
- Each import is followed by `layerup` to keep them from overlapping in space.

---

## 🧮 Global Variables

You can define and use global variables within your scripts like this:

```mcmd
@health = 10
@speed = 5
@block_type = "redstone_block"
@message = 'THIS IS INSANE!'
*also works with other assignment operators such as +=, -=, /=, *=, %=*