# 1 = previous page, 2 = next page, 3 = close the book, 1x = jump to page x, 100+i = open entry i

execute if score @s sticker_book.action matches 3 run function sticker_book:action/close
execute if score @s sticker_book.action matches 1 run scoreboard players remove @s sticker_book.page 1
execute if score @s sticker_book.action matches 2 run scoreboard players add @s sticker_book.page 1
execute if score @s sticker_book.action matches 11..13 run function sticker_book:action/goto_page
execute if score @s sticker_book.action matches 100.. run function sticker_book:action/open_entry

# Closing put the trigger back to 0, so only a page change ever reaches this line
execute if score @s sticker_book.action matches 1.. run function sticker_book:open
