
#> sticker_book:page/7/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics/crab=true}] unless entity @s[advancements={sticker_book:sticker/tropics/turtle=true}] run function sticker_book:page/7/ll
execute if entity @s[advancements={sticker_book:sticker/tropics/crab=true}] unless entity @s[advancements={sticker_book:sticker/tropics/turtle=true}] run function sticker_book:page/7/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics/crab=true}] if entity @s[advancements={sticker_book:sticker/tropics/turtle=true}] run function sticker_book:page/7/lf
execute if entity @s[advancements={sticker_book:sticker/tropics/crab=true}] if entity @s[advancements={sticker_book:sticker/tropics/turtle=true}] run function sticker_book:page/7/ff

