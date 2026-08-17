# Part 2: Drawing a page

Placing a glyph is not a coordinate, it is an arithmetic problem. This part solves it once for the spread,
then moves the answer into the lang file.

![A spread, eight of sixteen stickers found](img/tropics.png)

## The centring rule

**A dialog body centres every line on its own total advance.** Add up the advance of every character on the
line, call it `W`, and the line starts at `x = -W/2` relative to the centre of the body.

You never position anything absolutely. You position it by controlling the total width of the line it lives
on. Every space value in this pack comes out of that one rule.

## The spread

The page images are 146x195 (left) and 145x195 (right), so they advance 147 and 146. We want the seam at
`x = 0`. Write the line as right page, big negative space, left page:

```
\ue002   right page     +146    cursor at start+146
\ud000   jump back      -292    cursor at start-146
\ue001   left page      +147    cursor at start+1
```

`W = 1`, so the line starts at `-0.5`. The right page runs -0.5 to 144.5, the left page -146.5 to -0.5, and
the spread is centred. The `-292` is just `-(146 + 146)`: back over the page drawn, then back over the page
about to be drawn.

## A row of slots

Four sticker slots, each a 26x26 image advancing **25** (Part 1: trimmed width plus one), then a gap `G`,
then four more:

```
W = 100 + G + 100
left row centre   = -49.5 - G/2   want -73.5   ->   G = 48
right row centre  =  50.5 + G/2   want  72     ->   G = 43
```

Two answers, which is the honest result. The two centres always sum to 1 while the targets sum to -1.5,
because the left page is 146 wide and the right is 145. There is a fixed 2.5 pixels of error to put
somewhere: `\ud001 = 47` splits it, leaving the left row half a pixel off and the right row two.

Had we used 27 instead of 25 here, every row would sit eight pixels off across the spread.

## The lang file is the layout

You could put the whole page into the `dialog` command as one run of private use characters. Put it in the
[lang file](https://minecraft.wiki/w/Resource_pack#Language) instead, and keep the command holding only
what changes.

```json
"gui.sticker_book.page.spread": "%1$s\ud000%2$s\n\n\n\n%3$s\ud001%4$s\n\n\n\n\n\n%5$s\ud001%6$s\n\n\n\n\n%7$s\n%8$s\n\n\n\n",
"gui.sticker_book.row": "%1$s%2$s%3$s%4$s"
```

A [`translate` component](https://minecraft.wiki/w/Text_component_format) fills `%1$s` and friends from its
`with` list. Read the template as a grid:

| Line | Content | What it is |
|:--|:--|:--|
| 1 | `%1$s\ud000%2$s` | right page, jump back, left page |
| 5 | `%3$s\ud001%4$s` | first row of slots on each page |
| 11 | `%5$s\ud001%6$s` | second row of slots on each page |
| 16 | `%7$s` | the previous and next arrows |
| 17 | `%8$s` | the tab strip |

Blank lines do the vertical spacing, nine pixels each. Rows land 37 and 91 pixels below the top of the page
and the tabs at 176, past the bottom edge of the 195 pixel page image, so they stick out like real tabs.

Why the lang file:

- **Translators get the layout for free.** A German page needing different spacing is a lang edit, not a
  datapack edit.
- **The command stays readable.** `{translate: 'gui.sticker_book.row', with: [...]}` says what it is; 400
  characters of `\ue1xx` does not.
- **Templates nest.** `row` is used inside `page.spread`, keeping each argument list short.

## Iterating without launching the game

`tools/preview_book.py` implements the rules above against the real font and lang files and writes a PNG.
Every rendered image in this course came out of it, which makes each one a test: it re-derives the advances
from the PNGs the game reads, so wrong geometry shows up as a wrong picture.

```sh
python tools/preview_book.py docs/img
```

Next: [Part 3: The dialog](3-the-dialog.md).
