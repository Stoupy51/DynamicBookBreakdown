
#> sticker_book:on_spread_complete
#
# @executed	as the player & at current position
#
# @within	advancement sticker_book:sticker/plateaus
#			advancement sticker_book:sticker/tropics
#

execute if entity @s[advancements={sticker_book:sticker/tropics=true, sticker_book:sticker/plateaus=true}] run advancement grant @s only sticker_book:all_stickers

