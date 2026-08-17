schedule function sticker_book:second 1s replace

# Handing the book back once a second covers joining, dying and throwing it away, without a per tick scan
execute as @a unless predicate sticker_book:has_book run function sticker_book:give
