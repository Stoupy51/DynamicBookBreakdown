$dialog show @s { \
    type: 'minecraft:multi_action', \
    title: {translate: 'gui.sticker_book.title'}, \
    body: [{ \
        type: 'minecraft:plain_message', \
        width: 291, \
        contents: { \
            translate: 'gui.sticker_book.page.spread', font: 'sticker_book:assets', color: 'white', shadow_color: 0, \
            with: [ \
                {translate: 'gui.sticker_book.page.plateaus.right'}, \
                {translate: 'gui.sticker_book.page.plateaus.left'}, \
                {translate: 'gui.sticker_book.row', with: [$(slot_1), $(slot_2), $(slot_3), $(slot_4)]}, \
                {translate: 'gui.sticker_book.row', with: [$(slot_5), $(slot_6), $(slot_7), $(slot_8)]}, \
                {translate: 'gui.sticker_book.row', with: [$(slot_9), $(slot_10), $(slot_11), $(slot_12)]}, \
                {translate: 'gui.sticker_book.row', with: [$(slot_13), $(slot_14), $(slot_15), $(slot_16)]}, \
                {translate: 'gui.sticker_book.nav.left', with: [ \
                    {translate: 'gui.sticker_book.arrow.previous', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.nav.previous'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 1'}} \
                ]}, \
                {translate: 'gui.sticker_book.tabs', with: [ \
                    {translate: 'gui.sticker_book.tab.front.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.front.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 11'}}, \
                    {translate: 'gui.sticker_book.tab.tropics.idle', hover_event: {action: 'show_text', value: {translate: 'gui.sticker_book.tab.tropics.hover'}}, click_event: {action: 'run_command', command: 'trigger sticker_book.action set 12'}}, \
                    {translate: 'gui.sticker_book.tab.plateaus.selected'} \
                ]} \
            ] \
        } \
    }], \
    inputs: [], \
    can_close_with_escape: true, \
    pause: false, \
    after_action: 'none', \
    actions: [{ \
        label: {translate: 'gui.sticker_book.done'}, \
        width: 291, \
        action: {type: 'run_command', command: 'trigger sticker_book.action set 3'} \
    }] \
}
