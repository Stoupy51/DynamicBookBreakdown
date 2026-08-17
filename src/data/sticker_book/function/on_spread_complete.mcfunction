# Fires when the last criterion of a spread lands, so the only thing left to check is the other spreads
execute if entity @s[advancements={sticker_book:sticker/tropics=true,sticker_book:sticker/plateaus=true}] run advancement grant @s only sticker_book:all_stickers
