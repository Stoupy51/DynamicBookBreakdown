# A tab sends its page number plus ten, so the whole tab strip needs no function per page
scoreboard players operation @s sticker_book.page = @s sticker_book.action
scoreboard players remove @s sticker_book.page 10

playsound sticker_book:section_flip player @s ~ ~ ~ 1 1
