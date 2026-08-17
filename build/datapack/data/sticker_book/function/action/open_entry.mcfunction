
#> sticker_book:action/open_entry
#
# @executed	as @a[scores={sticker_book.action=1..}] & at @s
#
# @within	sticker_book:action/main
#

# A slot sends 100 plus its index in the book, which maps onto one half of one page
scoreboard players operation @s sticker_book.page = @s sticker_book.action
scoreboard players remove @s sticker_book.page 100
scoreboard players operation @s sticker_book.page /= $per_page sticker_book.page
scoreboard players add @s sticker_book.page 4

playsound sticker_book:section_flip player @s ~ ~ ~ 1 1

