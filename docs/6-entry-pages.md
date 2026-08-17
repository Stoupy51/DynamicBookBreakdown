# Part 6: Entry pages

Everything so far was made of glyphs whose width you already knew. Text is different, and that difference is
what forces a build step.

![An entry spread, both halves found](img/entry_ff.png)

A heading centred on each page, an icon, a name beside it, four label and value pairs in two columns, and a
wrapped paragraph. Six of those seven are left aligned, and a dialog body centres every line on its own
total advance. Centring is free. Left aligning is not.

## The one equation

For runs of advance `t0..tn` that should start at `x0..xn`, with `p` the pad before each run:

```
p[i] = x[i] - x[i-1] - t[i-1]
p[0] = 2 * x[0] + sum(p[1:]) + sum(t)
```

Check it with a single run: `p[0] = 2*x0 + t0`, so `W = 2*x0 + 2*t0`, the line starts at `-x0 - t0`, and the
run lands at `x0`. That is [layout.py](../src/entry_pages/layout.py), all fourteen lines of it.

Corollary worth keeping: **centring a run at `c` needs no measurement at all**, because a lone leading pad
of `2c` puts the run's centre at `c` whatever its width. That is how the headings are placed.

## So you have to measure the font

Every `t` above is a real pixel width, and one wrong value shifts everything after it.
[metrics.py](../src/entry_pages/metrics.py) implements the `BitmapProvider` formula from Part 1 against the
actual PNG rather than a hardcoded width table, so you can redraw the font and the pages stay correct.

The body font is `ascii_tall.png`, a normal 8x8 sheet sitting in the top of an 8x22 cell with the rest
transparent padding for the toast. Cropping each cell to its top eight rows gives a plain ASCII sheet:

```python
small.paste(tall.crop((0, row * cell_height, tall.width, row * cell_height + 8)), (0, row * 8))
ctx.assets.textures["sticker_book:font/ascii_small"] = Texture(small)
```

It goes into the font **before** `minecraft:include/default`, or vanilla's glyphs win and measurements drift
by a pixel here and there. `minecraft:include/space` goes in too, otherwise U+0020 is an empty cell
advancing 1 instead of 4.

## Offsets as characters

Pads have to be spelled as space characters. Rather than mint one per distinct pad, the plugin defines an
alphabet: one character per decimal digit per magnitude, in both signs. Seventy two characters cover every
offset under 10000, and any pad costs at most four of them.

```
-137  ->  <-100><-30><-7>
```

Binary decomposition is fewer characters on average and much harder to eyeball in a lang file.

## Four variants per page

The annoying consequence of `p[0]`: it depends on everything else on the line. The two halves of a spread
share their lines, so **whether the left entry is found changes where the right entry starts**. Padding is a
property of the pair, not of one entry.

A datapack cannot measure text, so the plugin solves all four combinations at build time and the datapack
picks one:

```mcfunction
# One line per variant, so nothing is recomputed while the book is open
execute unless entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/ll
execute if     entity @s[advancements={sticker_book:sticker/tropics={palm=true}}] unless entity @s[advancements={sticker_book:sticker/tropics={sun=true}}] run function sticker_book:page/4/fl
```

32 entries, two per spread, four variants each: 64 generated dialogs and 16 checks, none of them yours to
maintain. It also caps entries per spread, since three per page is eight variants and four is sixteen. Index
pages avoid all of this because their slots are fixed width glyphs.

## The width trap

The plugin will happily compute a line Minecraft refuses to draw. The total advance has a tidy closed form,
since the line starts at `-W/2` and the last run ends at `W/2`:

```
W = 2 * (x of the last run + its advance)
```

**The line width is twice the right edge of whatever is written last.** Draw the left page then the right,
and line 1 advances `2 * (0 + 146) = 292` against a body 291 wide. One pixel over, and `FocusableTextWidget`
wraps it: left page on line 1, right page on line 2, stacked nine pixels apart, which reads in game as a
single page with content spilling off both sides.

The fix is the order, not the arithmetic. Write the rightmost run first:

```python
lines[PAGE_LINE] = [Run(x=0, text=right_page), Run(x=-146, text=left_page)]
```

The last run is now the left page, ending at `-146 + 147 = 1`, so `W = 2`. Same reason the index pages in
Part 2 are written right page, jump back, left page: never about draw order, always about not wrapping.
`Layout.line` raises at build time when a line exceeds the body, and `preview_book.py` warns on it.

## The plugin

It restates nothing the pack already knows: names, descriptions, glyphs and spread titles are read back out
of `ctx.assets` at build time, so the lang file stays the single source of truth.

| File | Job |
|:--|:--|
| [metrics.py](../src/entry_pages/metrics.py) | Measures the font off its PNG, encodes offsets, wraps paragraphs |
| [layout.py](../src/entry_pages/layout.py) | The pad equation, and nothing else |
| [entries.py](../src/entry_pages/entries.py) | The 32 rows an entry adds: where it is seen, four taxonomy lines |
| [render.py](../src/entry_pages/render.py) | Where each part of an entry sits, and in what colour |
| [\_\_init\_\_.py](../src/entry_pages/__init__.py) | `beet_default`: build the font, emit the pages, wire the datapack |

Three things connect it back to the hand written half:

- Every index slot carries `trigger sticker_book.action set <100 + index>`. `action/open_entry` subtracts the
  base, divides by entries per page and adds the first entry page. No table, no function per entry.
- The plugin appends `sticker_book:entry/load` to `#minecraft:load`, raising `$max` from 3 to 19 so the page
  clamp lets you reach the new pages.
- Locked slots are clickable too, so a player can read what they are missing. That is why the locked
  component moved from one shared value in `const.mcfunction` to one per slot: a shared component cannot
  carry a per-slot click event.

![An entry spread in game, one side found and one side not](img/entry_spread.png)

## What you give up

Text baked into a dialog command is not translatable. Index pages keep their layout in the lang file and
stay translatable; entry pages do not, because their spacing is computed from the English strings. A German
translation means re-running the plugin against a German lang file. That is a cost of building it ahead of
time, not of the technique: keeping every entry centred needs no measurement and therefore no build step.

## Iterating on it

`tools/preview_book.py` reads the generated pages back out of `build/` and draws them. It re-derives the
advances independently, so a disagreement between plugin and preview shows up as a visibly wrong page. That
is how the 26 versus 24 trimming bug was found.

```sh
beet build && python tools/preview_book.py docs/img
```

Next: [Part 7: Going further](7-going-further.md).
