
#> sticker_book:action/main
#
# @executed	as @a[scores={sticker_book.action=1..}] & at @s
#
# @within	sticker_book:tick [ as @a[scores={sticker_book.action=1..}] & at @s ]
#

execute if score @s sticker_book.action matches 3 run function sticker_book:action/close
execute if score @s sticker_book.action matches 1 run scoreboard players remove @s sticker_book.page 1
execute if score @s sticker_book.action matches 2 run scoreboard players add @s sticker_book.page 1
execute if score @s sticker_book.action matches 11.. run function sticker_book:action/goto_page
execute if score @s sticker_book.action matches 1.. run function sticker_book:open

