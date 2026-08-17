
#> sticker_book:page/19/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus={sunset=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={quarry=true}}] run function sticker_book:page/19/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus={sunset=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={quarry=true}}] run function sticker_book:page/19/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus={sunset=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={quarry=true}}] run function sticker_book:page/19/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus={sunset=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={quarry=true}}] run function sticker_book:page/19/ff

