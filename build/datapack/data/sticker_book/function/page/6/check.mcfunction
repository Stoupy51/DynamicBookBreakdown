
#> sticker_book:page/6/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={fish=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={shell=true}}] run function sticker_book:page/6/ll
execute if entity @s[advancements={sticker_book:sticker/tropics={fish=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={shell=true}}] run function sticker_book:page/6/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics={fish=true}}] if entity @s[advancements={sticker_book:sticker/tropics={shell=true}}] run function sticker_book:page/6/lf
execute if entity @s[advancements={sticker_book:sticker/tropics={fish=true}}] if entity @s[advancements={sticker_book:sticker/tropics={shell=true}}] run function sticker_book:page/6/ff

