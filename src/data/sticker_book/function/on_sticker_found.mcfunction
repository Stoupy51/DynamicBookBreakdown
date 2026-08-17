# Run by every sticker advancement the first time it is granted, never again afterwards
scoreboard players add @s sticker_book.found 1

playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6

execute if score @s sticker_book.found matches 32.. run advancement grant @s only sticker_book:all_stickers
