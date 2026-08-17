
#> sticker_book:on_book_complete
#
# @executed	as the player & at current position
#
# @within	advancement sticker_book:all_stickers
#

tellraw @a [{selector: "@s", color: "light_purple"}, {text: " filled the whole sticker book!", color: "white"}]
particle minecraft:firework ~ ~1 ~ 0.4 0.5 0.4 0.2 60 normal
playsound minecraft:entity.firework_rocket.large_blast neutral @a ~ ~ ~ 1 1
playsound minecraft:entity.firework_rocket.twinkle neutral @a ~ ~ ~ 1 1

