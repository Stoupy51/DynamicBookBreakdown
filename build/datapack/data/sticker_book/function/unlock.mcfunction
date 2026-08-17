
#> sticker_book:unlock
#
# @within	sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "palm"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "sun"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "parrot"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "pineapple"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "fish"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "shell"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "crab"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "turtle"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "coconut"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "starfish"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "hibiscus"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "coral"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "dolphin"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "lagoon"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "tiki"}
#			sticker_book:dev/unlock_random_half {spread: "tropics", sticker: "wave"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "mesa"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "cactus"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "hawk"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "arch"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "campfire"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "boulder"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "lizard"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "tumbleweed"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "canyon"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "fossil"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "geode"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "dust_devil"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "coyote"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "sage"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "sunset"}
#			sticker_book:dev/unlock_random_half {spread: "plateaus", sticker: "quarry"}
#
# @args		spread (string)
#			sticker (string)
#

$execute unless entity @s[advancements={sticker_book:sticker/$(spread)={$(sticker)=true}}] run function sticker_book:on_sticker_found
$advancement grant @s only sticker_book:sticker/$(spread) $(sticker)

