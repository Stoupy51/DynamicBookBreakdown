
#> sticker_book:page/2/dialog
#
# @within	sticker_book:page/2/check with storage sticker_book:temp page
#
# @args		slot_1 (unknown)
#			slot_2 (unknown)
#			slot_3 (unknown)
#			slot_4 (unknown)
#			slot_5 (unknown)
#			slot_6 (unknown)
#			slot_7 (unknown)
#			slot_8 (unknown)
#			slot_9 (unknown)
#			slot_10 (unknown)
#			slot_11 (unknown)
#			slot_12 (unknown)
#			slot_13 (unknown)
#			slot_14 (unknown)
#			slot_15 (unknown)
#			slot_16 (unknown)
#

$dialog show @s { type: 'minecraft:multi_action', title: {translate: 'gui.sticker_book.title'}, body: [{ type: 'minecraft:plain_message', width: 291, contents: { translate: 'gui.sticker_book.page.spread', font: 'sticker_book:assets', color: 'white', shadow_color: 0, with: [ {translate: 'gui.sticker_book.page.tropics.right'}, {translate: 'gui.sticker_book.page.tropics.left'}, {translate: 'gui.sticker_book.row', with: [$(slot_1), $(slot_2), $(slot_3), $(slot_4)]}, {translate: 'gui.sticker_book.row', with: [$(slot_5), $(slot_6), $(slot_7), $(slot_8)]}, {translate: 'gui.sticker_book.row', with: [$(slot_9), $(slot_10), $(slot_11), $(slot_12)]}, {translate: 'gui.sticker_book.row', with: [$(slot_13), $(slot_14), $(slot_15), $(slot_16)]}, {translate: 'gui.sticker_book.nav.both', with: [ {translate: 'gui.sticker_book.arrow.previous', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.nav.previous'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 1'}}, {translate: 'gui.sticker_book.arrow.next', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.nav.next'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 2'}} ]}, {translate: 'gui.sticker_book.tabs', with: [ {translate: 'gui.sticker_book.tab.front.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.front.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 11'}}, {translate: 'gui.sticker_book.tab.tropics.selected'}, {translate: 'gui.sticker_book.tab.plateaus.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.plateaus.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 13'}} ]} ] } }], inputs: [], can_close_with_escape: true, pause: false, after_action: 'none', actions: [{ label: {translate: 'gui.sticker_book.done'}, width: 291, action: {type: 'run_command', command: 'trigger sticker_book.action set 3'} }] }

