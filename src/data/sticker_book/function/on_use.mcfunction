scoreboard players reset @s sticker_book.use

# The statistic fires for every written book, so the held item still has to be checked
execute if predicate sticker_book:holding_book run function sticker_book:open
