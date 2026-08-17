# Building a dynamic book in Minecraft

This repository is a working, self-contained rebuild of the Smithed Summit sticker book, stripped of
everything Summit specific so the mechanism is visible. It is a three page book: a cover, and two
two-page spreads holding sixteen sticker slots each. Slots start empty and fill in as the player finds
things, without the player ever having to close and reopen anything.

![The cover](docs/img/cover.png)

![A spread, eight of sixteen stickers found](docs/img/tropics.png)

Everything you see above is text. There is no GUI, no custom renderer, no entity. It is one `dialog`
command, one translation key, and one font.

---

## The three ideas

Before any code, three ideas do all the work. If you understand these, the rest is bookkeeping.

**1. A book is a dialog.** Since 1.21.6 a datapack can push an arbitrary window onto the player's screen
with `dialog show`. The window can hold text, and text can hold click and hover events. That is the whole
interface budget: a paragraph of text you are allowed to click.

**2. A font is a layout engine.** A resource pack font maps characters to images and to horizontal
offsets. Offsets are allowed to be negative. So "print this image, then move the cursor back 292 pixels,
then print that image" is a perfectly ordinary string. Once you can move the cursor anywhere, a paragraph
of text becomes a canvas.

**3. An advancement is a save file.** Advancements are stored per player, survive restarts, are queryable
from a selector, and pop a toast for free when granted. That makes them the natural place to record "this
player has found the parrot".

The book is those three things wired together: the font draws it, the dialog shows it, the advancements
decide what gets drawn.

---

## Part 1: Fonts

A font lives at `assets/<namespace>/font/<name>.json` and is a list of providers. Two kinds matter here.

### Bitmap providers

```json
{
  "type": "bitmap",
  "file": "sticker_book:book/tropics_page_left.png",
  "ascent": 11,
  "height": 195,
  "chars": ["\ue001"]
}
```

This says: the character `\ue001`, in this font, is that PNG.

- **`height`** is how tall the image is drawn, in pixels. The width follows the aspect ratio. The source
  PNG here is 146x195 and `height` is 195, so it draws at its native size. Set `height` to 390 and it
  draws twice as large, blurry, at 292x390.
- **`ascent`** is how far above the baseline the top of the image sits. Positive lifts it, negative drops
  it. An ascent of 11 on a 195 tall image means 11 pixels above the baseline and 184 below it: the page
  hangs down from the line it is written on.
- **`chars`** are the characters this provider defines. Use the Unicode private use area, `U+E000` to `U+F8FF`, so you never collide with a character a player might actually type.

The one number that is not in the JSON is the **advance**: how far the cursor moves after drawing. For a
bitmap glyph it is the drawn width plus one pixel. That `+1` is the source of most off-by-a-few font bugs,
so it is worth burning in:

```
   baseline
   |
   |    +-----------------+
   |    |                 |  ^
   |    |    the image    |  | height
   |    |                 |  v
---+----+-----------------+------------------
   |<-->|                 |
   ascent (negative here, so the glyph sits below the baseline)

   |<--- drawn width ---->|<->|
                            +1
   |<------- advance ---------->|
```

### Space providers

```json
{
  "type": "space",
  "advances": {"\ud000": -292, "\ud001": 38, "\ud002": 204}
}
```

A space provider defines characters that draw nothing and move the cursor by an exact amount. No `+1`,
no image, just movement. Negative values move the cursor backwards, which is what lets you draw two things
on top of each other, or draw the right page first and then back up to draw the left one.

Positive spaces are padding. Negative spaces are the interesting half.

### Centering

The last rule you need: **a dialog body centres every line on its own total advance.** Add up the advance
of every character on the line, call it `W`, and the line starts at `x = -W/2` relative to the centre of
the body.

That is not a detail, it is the coordinate system. It means you never position anything absolutely. You
position it by controlling the total width of the line it lives on. Every space value in this pack was
derived from that one equation.

### Worked example: drawing a two-page spread

The two page images are 146x195 (left) and 145x195 (right). Their advances are 147 and 146. We want the
spread centred, so the seam between the pages lands at x = 0.

The line is written as: right page, then a big negative space, then left page.

```
\ue002        draw the right page      advance +146,  cursor now at start+146
\ud000        jump backwards           advance -292,  cursor now at start-146
\ue001        draw the left page       advance +147,  cursor now at start+1
```

Total advance `W = 146 - 292 + 147 = 1`, so the line starts at `x = -0.5`. The right page is drawn from
-0.5 to 144.5, and the left page from -146.5 to -0.5. They meet at the origin, and the whole spread is
centred. The `-292` is simply `-(146 + 146)`: back over the page just drawn, then back over the page about
to be drawn.

Now a row of stickers on that spread. A sticker slot is a 26x26 image, so it advances 27. Four of them in
a row advance 108, and the row is visually 107 wide. We want one row centred on the left page (centre
`-73.5`) and one centred on the right page (centre `72`). Writing `G` for the gap between them:

```
W = 108 + G + 108
left row starts at  -W/2  and is centred at  -W/2 + 53.5   ->  we want -73.5  ->  W = 254
right row starts at -W/2 + 108 + G                          ->  G = 254 - 216 = 38
```

So `\ud001 = 38` and the row line is `<four slots>\ud001<four slots>`. That is the entire derivation of
every magic number in `font/assets.json`. There is no guessing step, and there does not need to be one.

### Iterating without launching the game

`tools/preview_book.py` implements exactly the rules above, reads the real font and lang files, and writes
a PNG. All three images in this document came out of it. Every image in this document is therefore a test:
if the geometry is wrong, the preview is wrong in the same way the game would be.

```sh
python tools/preview_book.py docs/img
```

---

## Part 2: The lang file is the layout

You could put the whole page into the `dialog` command as one long string of private use characters. Do
not. Put it in the lang file instead, and keep the command holding only the pieces that change.

`assets/sticker_book/lang/en_us.json`:

```json
"gui.sticker_book.page.spread": "%1$s\ud000%2$s\n\n\n\n%3$s\ud001%4$s\n\n\n\n\n\n%5$s\ud001%6$s\n\n\n\n\n%7$s\n%8$s\n\n\n\n",
"gui.sticker_book.row": "%1$s%2$s%3$s%4$s"
```

A `translate` component fills `%1$s`, `%2$s` and so on from its `with` list. Read the spread template as a
grid, one line per line of text:

| Line | Content | What it is |
|:--|:--|:--|
| 1 | `%1$s\ud000%2$s` | right page, jump back, left page |
| 5 | `%3$s\ud001%4$s` | first row of slots on each page |
| 11 | `%5$s\ud001%6$s` | second row of slots on each page |
| 16 | `%7$s` | the previous / next arrows |
| 17 | `%8$s` | the tab strip |

Blank lines do the vertical spacing, nine pixels each. Rows land at 37 and 91 pixels below the top of the
page, and the tabs at 176, which is past the bottom edge of the 195 pixel page image, so they stick out
underneath like real book tabs.

Three reasons this belongs in the lang file and not in the command:

- **Translators get the layout for free.** A German page needs different spacing? That is a lang file, not
  a datapack edit.
- **The command stays readable.** `{translate: 'gui.sticker_book.row', with: [...]}` says what it is.
  A 400 character run of `\ue1xx` does not.
- **Templates nest.** `row` is used inside `page.spread`, which keeps the argument count of each template
  small enough to hold in your head.

---

## Part 3: The dialog

`src/data/sticker_book/function/page/2/dialog.mcfunction`, trimmed to its skeleton:

```mcfunction
$dialog show @s { \
    type: 'minecraft:multi_action', \
    title: {translate: 'gui.sticker_book.title'}, \
    body: [{ \
        type: 'minecraft:plain_message', \
        width: 291, \
        contents: { \
            translate: 'gui.sticker_book.page.spread', font: 'sticker_book:assets', color: 'white', shadow_color: 0, \
            with: [ ... ] \
        } \
    }], \
    inputs: [], \
    can_close_with_escape: true, \
    pause: false, \
    after_action: 'none', \
    actions: [{label: {translate: 'gui.sticker_book.done'}, width: 291, action: {...}}] \
}
```

Points worth stopping on:

- **`font: 'sticker_book:assets'`** on the outer component. Set it once and every nested component inherits
  it, so you never repeat it on 16 slots.
- **`shadow_color: 0`** kills the drop shadow. Without it every page image is drawn twice, offset by one
  pixel, in black. It is the first thing to check when a page looks muddy.
- **`width`** on a `plain_message` is the wrapping width, not the window width. The window is sized by the
  widest action button, which is why the cover uses 211 and the spreads use 291.
- **`pause: false`** matters on a server. `after_action: 'none'` stops the Done button from closing the
  window on its own, because we want to close it ourselves.

### Why every click goes through a trigger

A click event inside the body runs a command *as the player*, which means it runs at permission level 0.
It cannot run `function`, and it cannot run `dialog`. What it can run is `trigger`.

So every clickable thing in the book does the same thing: set a number.

```mcfunction
click_event: {action: 'run_command', command: 'trigger sticker_book.action set 2'}
```

And one line in `tick.mcfunction` picks that number up at operator level:

```mcfunction
execute as @a[scores={sticker_book.action=1..}] at @s run function sticker_book:action/main
```

`action/main.mcfunction` is the whole input handler:

```mcfunction
# 1 = previous page, 2 = next page, 3 = close the book, 1x = jump straight to page x

execute if score @s sticker_book.action matches 3 run function sticker_book:action/close
execute if score @s sticker_book.action matches 1 run scoreboard players remove @s sticker_book.page 1
execute if score @s sticker_book.action matches 2 run scoreboard players add @s sticker_book.page 1
execute if score @s sticker_book.action matches 11.. run function sticker_book:action/goto_page

# Closing put the trigger back to 0, so only a page change ever reaches this line
execute if score @s sticker_book.action matches 1.. run function sticker_book:open
```

The tab values are deliberately `page + 10`. Three tabs, and no per-tab function: `goto_page` copies the
trigger into the page score and subtracts 10. Add a fourth spread and the tab strip needs no new code.

The redraw is not clever and does not need to be. Change the page number, call `open` again, `open` shows
the dialog again. Minecraft replaces the open window rather than stacking a second one, so from the player's
side it reads as a page turn.

---

## Part 4: Per-player state

This is the part Gneiss actually asked about: a slot that is greyed out until the player finds the thing.

![Found and unfound slots](docs/img/slots.png)

### One advancement per sticker

`src/data/sticker_book/advancement/sticker/tropics/palm.json`:

```json
{
  "parent": "sticker_book:root",
  "display": {
    "title": [
      {"translate": "gui.sticker_book.toast.background", "font": "sticker_book:toast"},
      {"translate": "gui.sticker_book.toast.text", "font": "sticker_book:advancement_text", "color": "#4d7d9b"}
    ],
    "icon": {"id": "minecraft:poisonous_potato", "components": {"minecraft:item_model": "sticker_book:sticker_book"}},
    "description": "",
    "announce_to_chat": false
  },
  "criteria": {"requirement": {"trigger": "minecraft:impossible"}},
  "rewards": {"function": "sticker_book:on_sticker_found"}
}
```

Four things at once, from one file:

- `minecraft:impossible` means it can never be earned by playing. It is granted by command, which makes it
  a flag you control rather than a condition you hope fires.
- It is saved per player, forever, with no scoreboard to maintain and nothing to reset on death.
- `advancements={...=true}` in a selector reads it back.
- Granting it pops a toast. And because a toast title is a text component, it can use a custom font, which
  is how the toast gets its own artwork instead of the vanilla frame.

The parent `sticker_book:root` has **no `display` field at all**. An advancement tree whose root has no
display never appears in the advancement screen. The whole 32 sticker tree is invisible in the GUI while
still toasting normally. That is the trick that keeps a collectible system from spamming the vanilla
advancement tab.

`rewards.function` runs as and at the player the first time the advancement is granted, and never again:

```mcfunction
scoreboard players add @s sticker_book.found 1
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6
execute if score @s sticker_book.found matches 32.. run advancement grant @s only sticker_book:all_stickers
```

That "and never again" is doing real work. It means the counter cannot double count, so there is never a
need to recount 32 advancements to find out where the player is.

Unlocking a sticker from anywhere else in the pack is one macro call:

```mcfunction
function sticker_book:unlock {sticker: "tropics/palm"}
```

### Turning state into a page

The dialog itself is static text. What varies is the 16 arguments handed to it, and those come from
storage through a macro function.

`page/2/check.mcfunction`:

```mcfunction
# Start from a fully locked page, then reveal only what this player has already found
data modify storage sticker_book:temp page set from storage sticker_book:const locked_page

execute if entity @s[advancements={sticker_book:sticker/tropics/palm=true}] run \
    data modify storage sticker_book:temp page.slot_1 set value "{translate:'gui.sticker_book.sticker.tropics.palm', ...}"
... one line per slot ...

function sticker_book:page/2/dialog with storage sticker_book:temp page
```

The shape is: start from the locked page, overwrite what is unlocked, hand the result to the dialog. The
locked page is built once at load time in `const.mcfunction` and copied per open, so the common case is one
`data modify` instead of sixteen.

Each slot value is a **text component stored as a string**. Macro substitution pastes the string in raw, so
what lands in the command is a real component and not a quoted one. Two rules keep that working:

- Use single quotes inside, because the outer NBT string uses double quotes.
- Never put a newline in it. The tooltip in this pack has two lines, and the newline lives in the lang file
  (`"gui.sticker_book.tooltip": "%1$s\n%2$s"`) precisely so the stored string stays flat.

Sixteen `execute if entity` checks per page open sounds like a lot and is not: it runs once, when a player
opens the book, on one player. Nothing here is on the tick loop.

---

## Part 5: The plumbing

Small, and worth reading once so nothing looks like magic.

| File | Job |
|:--|:--|
| `load.mcfunction` | Creates the four scoreboards, sets `$max` to the page count, kicks off the one second loop |
| `tick.mcfunction` | Two lines: someone right clicked a book, someone clicked in a dialog |
| `second.mcfunction` | Reschedules itself and hands the book back to anyone missing it |
| `on_use.mcfunction` | The `used:written_book` statistic fires for *every* written book, so the held item is checked with a predicate |
| `open.mcfunction` | Re-arms the trigger, clamps the page, plays the page turn, calls the page by number |
| `open_page.mcfunction` | `$function sticker_book:page/$(page)/check` |
| `dev/unlock_all` and `dev/reset` | `advancement grant @s from sticker_book:root` and its inverse |

The book is given by the loop rather than on join, so losing it is self-healing and there is no join event
to hook. A once-per-second predicate check over online players is not something you will ever see in a
profiler.

---

## Part 6: Adding a sticker

Everything repetitive in `src/` was generated from one table so that adding a sticker stays a small change.
By hand, one new sticker means:

1. A 26x26 PNG in `textures/sticker/<spread>/<id>.png`.
2. A bitmap provider in `font/assets.json` claiming the next free `\ue1xx` character.
3. Three lang keys: the glyph, the name, the description.
4. An advancement in `advancement/sticker/<spread>/<id>.json`, copied from any other one.
5. One `execute if entity` line in the spread's `check.mcfunction`.
6. Bump the total in `on_sticker_found.mcfunction`.

Steps 2 through 6 are exactly the kind of thing you should stop doing by hand once the list passes about
twenty entries. That is the point where the sticker table becomes the source of truth and a build step
writes the rest. This pack is at 32, so it is already over that line.

---

## What to change for a field guide

The mock-up that started this is a nature journal, not a sticker album. The differences are smaller than
they look:

- **The slot is bigger.** A plant entry with a name under it wants maybe 40x56 instead of 26x26. Redo the
  row arithmetic in Part 1 with the new advance; nothing else in the system cares.
- **A slot opens an entry page.** Give the unlocked slot a `click_event` that sets `sticker_book.action` to
  a value in a new range, say `100 + entry`, and add a branch in `action/main`. Entry pages are just more
  page numbers.
- **Unlocks come from the world, not from a command.** Anything that can run a function can call
  `sticker_book:unlock`. A player-triggered advancement on `minecraft:player_interacted_with_entity`, an
  interaction entity, a `location` trigger for a biome, whatever fits. The book does not care where the
  grant came from.
- **The index is a page.** An index of thirty entries is a spread of thirty slots whose click events jump to
  entry pages, greyed exactly like the stickers are here.

---

## File map

```
src/
  assets/sticker_book/
    font/assets.json            every page, tab, arrow and sticker glyph, plus the space advances
    font/toast.json             the toast background strip
    font/advancement_text.json  a taller ascii font for the toast label
    lang/en_us.json             the page layouts and all visible text
    textures/book/              pages, cover, tabs, arrows, the empty slot
    textures/sticker/           one PNG per sticker
  data/sticker_book/
    advancement/                one file per sticker, plus the hidden root
    function/page/N/check       decides the state of every slot
    function/page/N/dialog      the macro that shows the page
    function/action/            the input handler behind the triggers
    predicate/                  has the book, is holding the book
tools/preview_book.py           renders a page to PNG without the game
```

## Credits

The artwork, the book layout and the original implementation are from the Smithed Summit sticker book. This
repository reimplements the mechanism under its own namespace, with placeholder sticker art, so it can be
read and modified without the rest of Summit.
