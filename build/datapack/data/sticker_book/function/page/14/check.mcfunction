
#> sticker_book:page/14/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus={campfire=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={boulder=true}}] run function sticker_book:page/14/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus={campfire=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={boulder=true}}] run function sticker_book:page/14/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus={campfire=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={boulder=true}}] run function sticker_book:page/14/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus={campfire=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={boulder=true}}] run function sticker_book:page/14/ff

