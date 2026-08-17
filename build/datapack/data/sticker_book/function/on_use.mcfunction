
#> sticker_book:on_use
#
# @executed	as @a[scores={sticker_book.use=1..}] & at @s
#
# @within	sticker_book:tick [ as @a[scores={sticker_book.use=1..}] & at @s ]
#

scoreboard players reset @s sticker_book.use
execute if predicate sticker_book:holding_book run function sticker_book:open

