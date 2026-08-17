
#> sticker_book:page/12/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus={mesa=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={cactus=true}}] run function sticker_book:page/12/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus={mesa=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={cactus=true}}] run function sticker_book:page/12/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus={mesa=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={cactus=true}}] run function sticker_book:page/12/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus={mesa=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={cactus=true}}] run function sticker_book:page/12/ff

