
#> sticker_book:page/13/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus/hawk=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/arch=true}] run function sticker_book:page/13/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus/hawk=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/arch=true}] run function sticker_book:page/13/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus/hawk=true}] if entity @s[advancements={sticker_book:sticker/plateaus/arch=true}] run function sticker_book:page/13/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus/hawk=true}] if entity @s[advancements={sticker_book:sticker/plateaus/arch=true}] run function sticker_book:page/13/ff

