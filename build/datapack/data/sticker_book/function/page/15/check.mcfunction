
#> sticker_book:page/15/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus/lizard=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/tumbleweed=true}] run function sticker_book:page/15/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus/lizard=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/tumbleweed=true}] run function sticker_book:page/15/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus/lizard=true}] if entity @s[advancements={sticker_book:sticker/plateaus/tumbleweed=true}] run function sticker_book:page/15/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus/lizard=true}] if entity @s[advancements={sticker_book:sticker/plateaus/tumbleweed=true}] run function sticker_book:page/15/ff

