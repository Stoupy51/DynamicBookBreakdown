# What the player last clicked inside the dialog, see action/main for the meaning of each value
scoreboard objectives add sticker_book.action trigger

# Page the player is currently reading; $max holds the number of pages in the book
scoreboard objectives add sticker_book.page dummy
scoreboard players set $max sticker_book.page 3

# How many stickers the player has found so far, compared against the total in on_sticker_found
scoreboard objectives add sticker_book.found dummy

# Right clicking a written book, which is the only way the book is opened
scoreboard objectives add sticker_book.use minecraft.used:minecraft.written_book

function sticker_book:const
function sticker_book:second
