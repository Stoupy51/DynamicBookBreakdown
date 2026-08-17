
#> sticker_book:page/18/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/plateaus/coyote=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/sage=true}] run function sticker_book:page/18/ll
execute if entity @s[advancements={sticker_book:sticker/plateaus/coyote=true}] unless entity @s[advancements={sticker_book:sticker/plateaus/sage=true}] run function sticker_book:page/18/fl
execute unless entity @s[advancements={sticker_book:sticker/plateaus/coyote=true}] if entity @s[advancements={sticker_book:sticker/plateaus/sage=true}] run function sticker_book:page/18/lf
execute if entity @s[advancements={sticker_book:sticker/plateaus/coyote=true}] if entity @s[advancements={sticker_book:sticker/plateaus/sage=true}] run function sticker_book:page/18/ff

