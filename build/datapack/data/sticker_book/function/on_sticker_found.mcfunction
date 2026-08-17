
#> sticker_book:on_sticker_found
#
# @executed	as the player & at current position
#
# @within	advancement sticker_book:sticker/plateaus/arch
#			advancement sticker_book:sticker/plateaus/boulder
#			advancement sticker_book:sticker/plateaus/cactus
#			advancement sticker_book:sticker/plateaus/campfire
#			advancement sticker_book:sticker/plateaus/canyon
#			advancement sticker_book:sticker/plateaus/coyote
#			advancement sticker_book:sticker/plateaus/dust_devil
#			advancement sticker_book:sticker/plateaus/fossil
#			advancement sticker_book:sticker/plateaus/geode
#			advancement sticker_book:sticker/plateaus/hawk
#			advancement sticker_book:sticker/plateaus/lizard
#			advancement sticker_book:sticker/plateaus/mesa
#			advancement sticker_book:sticker/plateaus/quarry
#			advancement sticker_book:sticker/plateaus/sage
#			advancement sticker_book:sticker/plateaus/sunset
#			advancement sticker_book:sticker/plateaus/tumbleweed
#			advancement sticker_book:sticker/tropics/coconut
#			advancement sticker_book:sticker/tropics/coral
#			advancement sticker_book:sticker/tropics/crab
#			advancement sticker_book:sticker/tropics/dolphin
#			advancement sticker_book:sticker/tropics/fish
#			advancement sticker_book:sticker/tropics/hibiscus
#			advancement sticker_book:sticker/tropics/lagoon
#			advancement sticker_book:sticker/tropics/palm
#			advancement sticker_book:sticker/tropics/parrot
#			advancement sticker_book:sticker/tropics/pineapple
#			advancement sticker_book:sticker/tropics/shell
#			advancement sticker_book:sticker/tropics/starfish
#			advancement sticker_book:sticker/tropics/sun
#			advancement sticker_book:sticker/tropics/tiki
#			advancement sticker_book:sticker/tropics/turtle
#			advancement sticker_book:sticker/tropics/wave
#

scoreboard players add @s sticker_book.found 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6
execute if score @s sticker_book.found matches 32.. run advancement grant @s only sticker_book:all_stickers

