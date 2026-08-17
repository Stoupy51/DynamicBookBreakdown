
#> sticker_book:page/11/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics/tiki=true}] unless entity @s[advancements={sticker_book:sticker/tropics/wave=true}] run function sticker_book:page/11/ll
execute if entity @s[advancements={sticker_book:sticker/tropics/tiki=true}] unless entity @s[advancements={sticker_book:sticker/tropics/wave=true}] run function sticker_book:page/11/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics/tiki=true}] if entity @s[advancements={sticker_book:sticker/tropics/wave=true}] run function sticker_book:page/11/lf
execute if entity @s[advancements={sticker_book:sticker/tropics/tiki=true}] if entity @s[advancements={sticker_book:sticker/tropics/wave=true}] run function sticker_book:page/11/ff

