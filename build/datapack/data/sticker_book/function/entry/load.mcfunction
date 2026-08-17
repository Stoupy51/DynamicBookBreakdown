
#> sticker_book:entry/load
#
# @within	#minecraft:load
#

# Entry pages extend the book past the index, so the page clamp has to know about them
scoreboard players set $max sticker_book.page 19
scoreboard players set $per_page sticker_book.page 2

