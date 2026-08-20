# Part 5: The rest of the pack

The functions that are not about fonts, dialogs or state, and what a new sticker actually costs.

## The plumbing

| File | Job |
|:--|:--|
| [`load.mcfunction`](../build/datapack/data/sticker_book/function/load.mcfunction) | Creates the three scoreboards, sets `$max` to the page count, kicks off the one second loop |
| [`tick.mcfunction`](../build/datapack/data/sticker_book/function/tick.mcfunction) | Two lines: someone right clicked a book, someone clicked in a dialog |
| [`second.mcfunction`](../build/datapack/data/sticker_book/function/second.mcfunction) | Reschedules itself and hands the book back to anyone missing it |
| [`on_use.mcfunction`](../build/datapack/data/sticker_book/function/on_use.mcfunction) | `used:written_book` fires for every written book, so the held item is checked with a predicate |
| [`open.mcfunction`](../build/datapack/data/sticker_book/function/open.mcfunction) | Re-arms the trigger, clamps the page, plays the page turn, calls the page by number |
| [`open_page.mcfunction`](../build/datapack/data/sticker_book/function/open_page.mcfunction) | `$function sticker_book:page/$(page)/check` |
| [`unlock.mcfunction`](../build/datapack/data/sticker_book/function/unlock.mcfunction) | The one entry point anything else calls to award a sticker |
| [`dev/`](../build/datapack/data/sticker_book/function/dev/) | `unlock_all`, `unlock_random_half`, `reset` |

The book is given by the loop rather than on join, so losing it is self-healing and there is no join event
to hook. A once per second predicate check over online players will never show up in a profiler.

## Adding a sticker

By hand, one new sticker is six edits:

1. A 26x26 PNG in [`textures/sticker/<spread>/<id>.png`](../build/resourcepack/assets/sticker_book/textures/sticker/).
2. A bitmap provider in [`font/assets.json`](../build/resourcepack/assets/sticker_book/font/assets.json) claiming the next free `\ue1xx` character.
3. Three lang keys: the glyph, the name, the description.
4. One criterion in [`advancement/sticker/<spread>.json`](../build/datapack/data/sticker_book/advancement/sticker/).
5. One `execute if entity` line in the spread's [`check.mcfunction`](../build/datapack/data/sticker_book/function/page/2/check.mcfunction).
6. A row in `entries.py`, so it gets an entry page too.

Past about twenty entries, stop. `tools/generate_stickers.py` owns steps 1 to 5, the generator from Part 6
owns step 6, and both read one table, so a new sticker is one row plus a rebuild. `generate_stickers.py` is
a plain script writing files into `src/`: run it, read the diff, commit it.

The regrouping in Part 4 paid off here. Step 4 used to be a whole new file, and there used to be a seventh
step bumping a hardcoded total.

Next: [Part 6: Entry pages](6-entry-pages.md).
