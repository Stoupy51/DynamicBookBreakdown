
#> sticker_book:load
#
# @within	#minecraft:load
#

scoreboard objectives add sticker_book.action trigger
scoreboard objectives add sticker_book.page dummy
scoreboard players set $max sticker_book.page 3
scoreboard objectives add sticker_book.found dummy
scoreboard objectives add sticker_book.use minecraft.used:minecraft.written_book
function sticker_book:const
function sticker_book:second

