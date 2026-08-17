
#> sticker_book:page/9/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics/hibiscus=true}] unless entity @s[advancements={sticker_book:sticker/tropics/coral=true}] run function sticker_book:page/9/ll
execute if entity @s[advancements={sticker_book:sticker/tropics/hibiscus=true}] unless entity @s[advancements={sticker_book:sticker/tropics/coral=true}] run function sticker_book:page/9/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics/hibiscus=true}] if entity @s[advancements={sticker_book:sticker/tropics/coral=true}] run function sticker_book:page/9/lf
execute if entity @s[advancements={sticker_book:sticker/tropics/hibiscus=true}] if entity @s[advancements={sticker_book:sticker/tropics/coral=true}] run function sticker_book:page/9/ff

