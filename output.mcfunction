setblock 1 -60 -12 command_block[facing=east,conditional=false]{Command:"kill @e[type=minecraft:armor_stand,tag=backroomsBuilder]",auto:0b}
setblock 1 -59 -12 oak_sign[rotation=4]{front_text:{messages:["start","","",""]}}
setblock 2 -60 -12 chain_command_block[facing=east,conditional=false]{Command:'summon armor_stand 1 -50 -14 {Tags:["backroomsBuilder"],NoGravity:1b}',auto:1b}
setblock 3 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add GRID_SIZE dummy",auto:1b}
setblock 4 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c GRID_SIZE 25",auto:1b}
setblock 5 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add x dummy",auto:1b}
setblock 6 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c x 0",auto:1b}
setblock 7 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add y dummy",auto:1b}
setblock 8 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c y 0",auto:1b}
setblock 9 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add one dummy",auto:1b}
setblock 10 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c one 1",auto:1b}
setblock 11 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add randNum dummy",auto:1b}
setblock 12 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c randNum 0",auto:1b}
setblock 13 -60 -12 chain_command_block[facing=east,conditional=false]{Command:"setblock 0 -60 -10 redstone_block destroy",auto:1b}
setblock 1 -60 -10 command_block[facing=east,conditional=false]{Command:"scoreboard players operation c x += c one",auto:0b}
setblock 1 -59 -10 oak_sign[rotation=4]{front_text:{messages:["addRoom","","",""]}}
setblock 2 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x >= c GRID_SIZE",auto:1b}
setblock 3 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute as @e[type=minecraft:armor_stand,tag=backroomsBuilder] at @s run tp @s 1 ~ ~6",auto:1b}
setblock 4 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"scoreboard players operation c y += c one",auto:1b}
setblock 5 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"scoreboard players set c x 0",auto:1b}
setblock 6 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute unless  score c x >= c GRID_SIZE",auto:1b}
setblock 7 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute as @e[type=minecraft:armor_stand,tag=backroomsBuilder] at @s run tp @s ~6 ~ ~",auto:1b}
setblock 8 -60 -10 chain_command_block[facing=east,conditional=false]{Command:'tellraw @a [{"text":"ArmorStand at "},{"score":{"name":"c","objective":"x"}},{"text":", "},{"score":{"name":"c","objective":"y"}}]',auto:1b}
setblock 9 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 10 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute store result score c randNum run random value 1..24",auto:1b}
setblock 11 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 11 -59 -10 oak_sign[rotation=4]{front_text:{messages:["All rooms","","",""]}}
setblock 12 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 1 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 0 -61 -22 6 -56 -16 ~ ~ ~",auto:1b}
setblock 13 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 14 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 2 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 7 -61 -22 13 -56 -16 ~ ~ ~",auto:1b}
setblock 15 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 16 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 3 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 14 -61 -22 20 -56 -16 ~ ~ ~",auto:1b}
setblock 17 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 18 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 4 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 21 -61 -22 27 -56 -16 ~ ~ ~",auto:1b}
setblock 19 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 20 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 5 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 28 -61 -22 34 -56 -16 ~ ~ ~",auto:1b}
setblock 21 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 22 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 6 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 35 -61 -22 41 -56 -16 ~ ~ ~",auto:1b}
setblock 23 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 24 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 7 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 42 -61 -22 48 -56 -16 ~ ~ ~",auto:1b}
setblock 25 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 26 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 8 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 49 -61 -22 55 -56 -16 ~ ~ ~",auto:1b}
setblock 27 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 28 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 9 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 56 -61 -22 62 -56 -16 ~ ~ ~",auto:1b}
setblock 29 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 30 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 10 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 63 -61 -22 69 -56 -16 ~ ~ ~",auto:1b}
setblock 31 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 32 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 11 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 70 -61 -22 76 -56 -16 ~ ~ ~",auto:1b}
setblock 33 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 34 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 12 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 77 -61 -22 83 -56 -16 ~ ~ ~",auto:1b}
setblock 35 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 36 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 13 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 84 -61 -22 90 -56 -16 ~ ~ ~",auto:1b}
setblock 37 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 38 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 14 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 91 -61 -22 97 -56 -16 ~ ~ ~",auto:1b}
setblock 39 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 40 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 15 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 98 -61 -22 104 -56 -16 ~ ~ ~",auto:1b}
setblock 41 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 42 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 16 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 105 -61 -22 111 -56 -16 ~ ~ ~",auto:1b}
setblock 43 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 44 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 17 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 112 -61 -22 118 -56 -16 ~ ~ ~",auto:1b}
setblock 45 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 46 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 18 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 119 -61 -22 125 -56 -16 ~ ~ ~",auto:1b}
setblock 47 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 48 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 19 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 126 -61 -22 132 -56 -16 ~ ~ ~",auto:1b}
setblock 49 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 50 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 20 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 133 -61 -22 139 -56 -16 ~ ~ ~",auto:1b}
setblock 51 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 52 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 21 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 140 -61 -22 146 -56 -16 ~ ~ ~",auto:1b}
setblock 53 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 54 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 22 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 147 -61 -22 153 -56 -16 ~ ~ ~",auto:1b}
setblock 55 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 56 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 23 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 154 -61 -22 160 -56 -16 ~ ~ ~",auto:1b}
setblock 57 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 58 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"execute if score c randNum matches 24 run execute at @e[type=armor_stand,tag=backroomsBuilder] run clone 161 -61 -22 167 -56 -16 ~ ~ ~",auto:1b}
setblock 59 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x < c GRID_SIZE  run execute if  score c y < c GRID_SIZE",auto:1b}
setblock 60 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"setblock 0 -60 -10 redstone_block destroy",auto:1b}
setblock 61 -60 -10 chain_command_block[facing=east,conditional=false]{Command:'kill @e[type=item,nbt={Item:{id:"minecraft:redstone_block"}}]',auto:1b}
setblock 62 -60 -10 chain_command_block[facing=east,conditional=false]{Command:"execute if  score c x matches 0  run execute if  score c y = c GRID_SIZE",auto:1b}
setblock 63 -60 -10 chain_command_block[facing=east,conditional=true]{Command:"setblock 0 -60 -8 redstone_block destroy",auto:1b}
setblock 1 -60 -8 command_block[facing=east,conditional=false]{Command:"fill 7 -50 -14 157 -46 -14 stripped_bamboo_block",auto:0b}
setblock 1 -59 -8 oak_sign[rotation=4]{front_text:{messages:["createOutlineWalls","","",""]}}
setblock 2 -60 -8 chain_command_block[facing=east,conditional=false]{Command:"fill 7 -50 -14 7 -46 136 stripped_bamboo_block",auto:1b}
setblock 3 -60 -8 chain_command_block[facing=east,conditional=false]{Command:"fill 157 -50 -14 157 -46 136 stripped_bamboo_block",auto:1b}
setblock 4 -60 -8 chain_command_block[facing=east,conditional=false]{Command:"fill 7 -50 136 157 -46 136 stripped_bamboo_block",auto:1b}
setblock 1 -60 -6 command_block[facing=east,conditional=false]{Command:"tag @a remove monster",auto:0b}
setblock 1 -59 -6 oak_sign[rotation=4]{front_text:{messages:["assignMonster","","",""]}}
setblock 2 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"tag @r add monster",auto:1b}
setblock 3 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team add monster",auto:1b}
setblock 4 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team empty monster",auto:1b}
setblock 5 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team add survivors",auto:1b}
setblock 6 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team empty survivors",auto:1b}
setblock 7 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team join monster @a[tag=monster]",auto:1b}
setblock 8 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team join survivors @a[tag=!monster]",auto:1b}
setblock 9 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team modify survivors friendlyFire false",auto:1b}
setblock 10 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team modify monster nametagVisibility hideForOtherTeams",auto:1b}
setblock 11 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team modify survivors nametagVisibility hideForOtherTeams",auto:1b}
setblock 12 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team modify survivors color dark_red",auto:1b}
setblock 13 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"team modify monster color black",auto:1b}
setblock 14 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"tellraw @a[tag=monster] {'text':'YOU ARE THE MONSTER!','color':'red','bold':true}",auto:1b}
setblock 15 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"tellraw @a[tag=!monster] {'text':'You are NOT the monster!','color':'green'}",auto:1b}
setblock 16 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:scale base set 1",auto:1b}
setblock 17 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:movement_speed base set 0.12",auto:1b}
setblock 18 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:sneaking_speed base set 0.3",auto:1b}
setblock 19 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:attack_damage base set 0",auto:1b}
setblock 20 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:attack_knockback base set 0",auto:1b}
setblock 21 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:attack_speed base set 4",auto:1b}
setblock 22 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p minecraft:entity_interaction_range base set 3",auto:1b}
setblock 23 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:scale base set 1.3",auto:1b}
setblock 24 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:movement_speed base set 0.124",auto:1b}
setblock 25 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:attack_damage base set 5",auto:1b}
setblock 26 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:attack_knockback base set 2",auto:1b}
setblock 27 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:attack_speed base set 0.8",auto:1b}
setblock 28 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:entity_interaction_range base set 1",auto:1b}
setblock 29 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"attribute @p[tag=monster] minecraft:sneaking_speed base set 0.5",auto:1b}
setblock 30 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add monster.echo minecraft.used:minecraft.goat_horn",auto:1b}
setblock 31 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set @a monster.echo 0",auto:1b}
setblock 32 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"give @a[tag=monster] minecraft:goat_horn[instrument='yearn_goat_horn']",auto:1b}
setblock 33 -60 -6 chain_command_block[facing=east,conditional=false]{Command:"setblock 0 -60 -4 redstone_block destroy",auto:1b}
setblock 1 -60 -4 repeating_command_block[facing=east,conditional=false]{Command:"execute if score @a[tag=monster,limit=1] monster.echo matches 1.. run scoreboard players set @a[tag=monster] monster.echo 0",auto:0b}
setblock 1 -59 -4 oak_sign[rotation=4]{front_text:{messages:["detectMonsterEcho","","",""]}}
setblock 2 -60 -4 chain_command_block[facing=east,conditional=true]{Command:"effect give @a glowing 8 255 true",auto:1b}
setblock 3 -60 -4 chain_command_block[facing=east,conditional=true]{Command:"effect give @a minecraft:blindness 4 255 true",auto:1b}
setblock 4 -60 -4 chain_command_block[facing=east,conditional=true]{Command:"effect give @a minecraft:darkness 4 255 true",auto:1b}
setblock 5 -60 -4 chain_command_block[facing=east,conditional=true]{Command:"execute at @a[tag=monster] run playsound minecraft:item.goat_horn.sound.5 voice @a ~ ~ ~ 100 0.5 0",auto:1b}
setblock 1 -60 -2 command_block[facing=east,conditional=false]{Command:"execute at @a[tag=monster] run playsound minecraft:entity.warden.heartbeat player @a ~ ~ ~ 1 2",auto:0b}
setblock 1 -59 -2 oak_sign[rotation=4]{front_text:{messages:["monsterFootSteps","","",""]}}
setblock 2 -60 -2 chain_command_block[facing=east,conditional=false]{Command:"scoreboard objectives add sys.timer dummy",auto:1b}
setblock 3 -60 -2 chain_command_block[facing=east,conditional=false]{Command:"scoreboard players set c sys.timer 5",auto:1b}
fill 4 -60 -2 11 -60 -2 air
setblock 4 -60 -2 chain_command_block[facing=east,conditional=false]{Command:"setblock 6 -60 -2 redstone_block destroy",auto:1b}
setblock 7 -60 -2 repeating_command_block[facing=east,conditional=false]{Command:"execute if score c sys.timer matches 1.. run scoreboard players remove c sys.timer 1",auto:0b}
setblock 8 -60 -2 chain_command_block[facing=east,conditional=false]{Command:"execute if score c sys.timer matches 0 run setblock 6 -60 -2 air",auto:1b}
setblock 9 -60 -2 chain_command_block[facing=east,conditional=true]{Command:"setblock 11 -60 -2 redstone_block destroy",auto:1b}
setblock 12 -60 -2 command_block[facing=east,conditional=false]{Command:"setblock 0 -60 -2 minecraft:redstone_block destroy",auto:0b}
setblock 13 -60 -2 chain_command_block[facing=east,conditional=false]{Command:"kill @e[type=item]",auto:1b}