# The cover carries a single dynamic element: the sticker awarded for filling the whole book
data modify storage sticker_book:temp page set value {completion: "{text:''}"}
execute if entity @s[advancements={sticker_book:all_stickers=true}] run data modify storage sticker_book:temp page.completion set value "{translate:'gui.sticker_book.completion',hover_event:{action:'show_text',value:{translate:'gui.sticker_book.completion.hover',color:'gold'}}}"

function sticker_book:page/1/dialog with storage sticker_book:temp page
