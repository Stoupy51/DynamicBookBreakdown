
#> sticker_book:open
#
# @executed	as @a[scores={sticker_book.action=1..}] & at @s
#
# @within	sticker_book:action/main
#			sticker_book:on_use
#

scoreboard players set @s sticker_book.action 0
scoreboard players enable @s sticker_book.action
execute unless score @s sticker_book.page matches 1.. run scoreboard players set @s sticker_book.page 1
execute if score @s sticker_book.page > $max sticker_book.page run scoreboard players operation @s sticker_book.page = $max sticker_book.page
playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1
execute store result storage sticker_book:temp open.page int 1 run scoreboard players get @s sticker_book.page
function sticker_book:open_page with storage sticker_book:temp open

