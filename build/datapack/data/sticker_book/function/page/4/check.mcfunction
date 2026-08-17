
#> sticker_book:page/4/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/ll
execute if entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] if entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/lf
execute if entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] if entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/ff

