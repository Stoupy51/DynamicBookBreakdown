
#> sticker_book:page/1/dialog
#
# @within	sticker_book:page/1/check with storage sticker_book:temp page
#
# @args		completion (string)
#

$dialog show @s { type: 'minecraft:multi_action', title: {translate: 'gui.sticker_book.title'}, body: [{ type: 'minecraft:plain_message', width: 137, contents: { translate: 'gui.sticker_book.page.cover', font: 'sticker_book:assets', color: 'white', shadow_color: 0, with: [ {translate: 'gui.sticker_book.nav.front', with: [ {translate: 'gui.sticker_book.arrow.next_gold', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.nav.next'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 2'}} ]}, {translate: 'gui.sticker_book.tabs.front', with: [ {translate: 'gui.sticker_book.tab.front.selected'}, {translate: 'gui.sticker_book.tab.tropics.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.tropics.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 12'}}, {translate: 'gui.sticker_book.tab.plateaus.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.plateaus.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 13'}} ]}, $(completion) ] } }], inputs: [], can_close_with_escape: true, pause: false, after_action: 'none', actions: [{ label: {translate: 'gui.sticker_book.done'}, width: 211, action: {type: 'run_command', command: 'trigger sticker_book.action set 3'} }] }

