
#> sticker_book:page/17/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus={geode=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={dust_devil=true}}] run function sticker_book:page/17/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus={geode=true}}] unless entity @s[advancements={sticker_book:sticker/plateaus={dust_devil=true}}] run function sticker_book:page/17/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus={geode=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={dust_devil=true}}] run function sticker_book:page/17/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus={geode=true}}] if entity @s[advancements={sticker_book:sticker/plateaus={dust_devil=true}}] run function sticker_book:page/17/ff

