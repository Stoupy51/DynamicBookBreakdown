
#> sticker_book:second
#
# @within	sticker_book:load
#			sticker_book:second 1s replace [ scheduled ]
#

schedule function sticker_book:second 1s replace
execute as @a unless predicate sticker_book:has_book run function sticker_book:give

