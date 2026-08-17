
#> sticker_book:action/goto_page
#
# @executed	as @a[scores={sticker_book.action=1..}] & at @s
#
# @within	sticker_book:action/main
#

scoreboard players operation @s sticker_book.page = @s sticker_book.action
scoreboard players remove @s sticker_book.page 10
playsound sticker_book:section_flip player @s ~ ~ ~ 1 1

