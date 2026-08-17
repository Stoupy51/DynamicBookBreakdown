
#> sticker_book:page/8/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={coconut=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={starfish=true}}] run function sticker_book:page/8/ll
execute if entity @s[advancements={sticker_book:sticker/tropics={coconut=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={starfish=true}}] run function sticker_book:page/8/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics={coconut=true}}] if entity @s[advancements={sticker_book:sticker/tropics={starfish=true}}] run function sticker_book:page/8/lf
execute if entity @s[advancements={sticker_book:sticker/tropics={coconut=true}}] if entity @s[advancements={sticker_book:sticker/tropics={starfish=true}}] run function sticker_book:page/8/ff

