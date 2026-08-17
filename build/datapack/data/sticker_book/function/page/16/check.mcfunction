
#> sticker_book:page/16/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus={canyon=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={fossil=true}}] run function sticker_book:page/16/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus={canyon=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={fossil=true}}] run function sticker_book:page/16/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus={canyon=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={fossil=true}}] run function sticker_book:page/16/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus={canyon=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={fossil=true}}] run function sticker_book:page/16/ff

