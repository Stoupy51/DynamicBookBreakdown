
#> sticker_book:page/5/check
#
# @within	???
#

# One line per variant, so nothing has to be recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={parrot=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={pineapple=true}}] run function sticker_book:page/5/ll
execute if entity @s[advancements={sticker_book:sticker/tropics={parrot=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={pineapple=true}}] run function sticker_book:page/5/fl
execute unless entity @s[advancements={sticker_book:sticker/tropics={parrot=true}}] if entity @s[advancements={sticker_book:sticker/tropics={pineapple=true}}] run function sticker_book:page/5/lf
execute if entity @s[advancements={sticker_book:sticker/tropics={parrot=true}}] if entity @s[advancements={sticker_book:sticker/tropics={pineapple=true}}] run function sticker_book:page/5/ff

