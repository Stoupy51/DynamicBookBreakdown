# Single entry point for the rest of the pack: function sticker_book:unlock {spread:"tropics",sticker:"palm"}
# The guard runs first, so the toast and the sound only happen the first time a sticker is found
$execute unless entity @s[advancements={sticker_book:sticker/$(spread)={$(sticker)=true}}] run function sticker_book:on_sticker_found
$advancement grant @s only sticker_book:sticker/$(spread) $(sticker)
