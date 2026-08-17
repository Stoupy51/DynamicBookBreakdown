
#> sticker_book:page/10/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={dolphin=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={lagoon=true}}] run function sticker_book:page/10/ll
execute if entity @s[advancements={sticker_book:sticker/tropics={dolphin=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={lagoon=true}}] run function sticker_book:page/10/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics={dolphin=true}}] if entity @s[advancements={sticker_book:sticker/tropics={lagoon=true}}] run function sticker_book:page/10/lf
execute if entity @s[advancements={sticker_book:sticker/tropics={dolphin=true}}] if entity @s[advancements={sticker_book:sticker/tropics={lagoon=true}}] run function sticker_book:page/10/ff

