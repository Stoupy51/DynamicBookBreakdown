
# Part 1: Fonts

Everything in this book is one font doing the drawing. This part is the vocabulary: what a provider is,
what `height` and `ascent` do, and where the advance comes from. Reference:
[Font](https://minecraft.wiki/w/Font) on the wiki.

## A font is a list of providers

A font lives at `assets/<namespace>/font/<name>.json` and is a stack of providers. The shipped font is
[`assets.json`](../build/resourcepack/assets/sticker_book/font/assets.json):

```json
{"providers": [ {"type": "bitmap", "...": "..."}, {"type": "reference", "id": "minecraft:include/default"} ]}
```

**Providers are searched in order and the first match wins**, so everything after a match is a fallback for
characters it did not define. Put your glyphs first, vanilla last.

Name it on any [text component](https://minecraft.wiki/w/Text_component_format):

```json
{"translate": "gui.sticker_book.page.spread", "font": "sticker_book:assets"}
{"text": "\ud000", "font": "sticker_book:assets"}
```

## The five types

| Type | What it does |
|:--|:--|
| [`bitmap`](https://minecraft.wiki/w/Font#Bitmap_provider) | A PNG cut into a grid of cells, one character per cell. The one this pack uses |
| [`space`](https://minecraft.wiki/w/Font#Space_provider) | Characters that draw nothing and move the cursor by an exact number of pixels |
| [`reference`](https://minecraft.wiki/w/Font#Reference_provider) | Splices another font's providers in at this position |
| [`ttf`](https://minecraft.wiki/w/Font#TTF_provider) | A real font file, with size, oversampling and a shift |
| [`unihex`](https://minecraft.wiki/w/Font#Unihex_provider) | A GNU unifont zip, how vanilla ships CJK |

## Bitmap providers

```json
{
  "type": "bitmap",
  "file": "sticker_book:book/tropics_page_left.png",
  "ascent": 11,
  "height": 195,
  "chars": ["\ue001"]
}
```

| Field | Meaning |
|:--|:--|
| `file` | Path under `textures/`, so this reads `textures/book/tropics_page_left.png` |
| `chars` | A grid: one string per row, one character per cell. Rows must be equal length, `\u0000` leaves a cell unused |
| `height` | How tall a cell is drawn, in pixels. Defaults to 8. Width follows the aspect ratio |
| `ascent` | How far above the baseline the top of the glyph sits. Must not exceed `height`, or the pack fails to load |

The image is divided by the shape of `chars`, not by any declared cell size: a 128x128 PNG with sixteen rows
of sixteen characters gives 8x8 cells. `height` then rescales them. This page is a 146x195 PNG in a 1x1 grid
at `height: 195`, so it draws at native size; `height: 390` would draw it at 292x390, blurry.

`ascent` is where the glyph hangs from. Positive lifts it above the baseline, negative drops it below.

```
   baseline
   |
   |    +-----------------+
   |    |                 |  ^
   |    |    the image    |  | height
   |    |                 |  v
---+----+-----------------+------------------
   |<-->|
   ascent

   |<--- drawn width ---->|<->|
                            +1
   |<------- advance ---------->|
```

At `ascent: 11` on a 195 tall image, 11 pixels sit above the line and 184 below: the page hangs down from
the line it is written on. The tab glyphs use `ascent: -32`, so they hang lower still and stick out from
under the page.

## The advance

The one number that is not in the JSON: how far the cursor moves after drawing. The wiki says the width is
"automatically determined based on the last right-most column of pixels containing any alpha value above 0";
`BitmapProvider` says exactly how:

```java
(int)(0.5 + actualGlyphWidth * pixelScale) + 1
```

- `pixelScale` is `height / cell_height`.
- `actualGlyphWidth` is one past the **rightmost column of the cell holding a non transparent pixel**.
- Bold adds one more pixel per glyph (`GlyphInfo.getBoldOffset`).

That trimming causes most off-by-a-few font bugs. A sticker slot is a 26x26 PNG whose art stops at column
24, so it advances **25, not 27**. Assuming the image width pulls every row two pixels per slot toward the
spine, eight across a spread.

**A glyph advances by its trimmed width plus one, not by its image width.**

## Space providers

```json
{"type": "space", "advances": {"\ud000": -292, "\ud001": 47}}
```

The complete set of page, slot and offset providers is in [`assets.json`](../build/resourcepack/assets/sticker_book/font/assets.json).

Characters that draw nothing and move the cursor by exactly that value. No image, no `+1`. Negative values
move it backwards, which is what lets you draw two things on top of each other, or draw the right page first
and then back up for the left one.

Positive spaces are padding. Negative spaces are the interesting half.

## Reference providers

```json
{"type": "reference", "id": "minecraft:include/space"}
```

Splices another font's providers in at that point in the stack. `minecraft:include/space` gives U+0020 as a
real 4 pixel space (without it, a space is an empty glyph advancing 1), and `minecraft:include/default`
gives the whole vanilla font as a fallback.

## Gotchas

- **Pick characters from the private use area**, `U+E000` to `U+F8FF`, so nothing a player types collides
  with a glyph. This pack uses `\ue000` and up for page art, `\ue1xx` for stickers.
- **Drop shadow doubles every image.** Set
  [`shadow_color: 0`](https://minecraft.wiki/w/Text_component_format) on the component or every page is
  drawn twice, one pixel apart, in black.
- **First match wins.** A provider added after `minecraft:include/default` is never reached for a character
  vanilla already defines.
- **Duplicate characters warn and lose.** Declaring a codepoint twice logs a warning and keeps the last one.

Next: [Part 2: Drawing a page](2-drawing-a-page.md), where these turn into an actual layout.

