# Part 5: The rest of the pack

The functions that are not about fonts, dialogs or state, and what a new sticker actually costs.

## The plumbing

| File | Job |
|:--|:--|
| `load.mcfunction` | Creates the three scoreboards, sets `$max` to the page count, kicks off the one second loop |
| `tick.mcfunction` | Two lines: someone right clicked a book, someone clicked in a dialog |
| `second.mcfunction` | Reschedules itself and hands the book back to anyone missing it |
| `on_use.mcfunction` | `used:written_book` fires for every written book, so the held item is checked with a predicate |
| `open.mcfunction` | Re-arms the trigger, clamps the page, plays the page turn, calls the page by number |
| `open_page.mcfunction` | `$function sticker_book:page/$(page)/check` |
| `unlock.mcfunction` | The one entry point anything else calls to award a sticker |
| `dev/` | `unlock_all`, `unlock_random_half`, `reset` |

The book is given by the loop rather than on join, so losing it is self-healing and there is no join event
to hook. A once per second predicate check over online players will never show up in a profiler.

## Adding a sticker

By hand, one new sticker is six edits:

1. A 26x26 PNG in `textures/sticker/<spread>/<id>.png`.
2. A bitmap provider in `font/assets.json` claiming the next free `\ue1xx` character.
3. Three lang keys: the glyph, the name, the description.
4. One criterion in `advancement/sticker/<spread>.json`.
5. One `execute if entity` line in the spread's `check.mcfunction`.
6. A row in `entries.py`, so it gets an entry page too.

Steps 2 to 6 are exactly what to stop doing by hand past about twenty entries, which is why
`tools/generate_stickers.py` owns 1 to 5 and the plugin from Part 6 owns 6. Both read one table, so a new
sticker is one row plus a rebuild.

The advancement regrouping in Part 4 paid off here: step 4 used to be a whole new file, and there used to be
a seventh step bumping a hardcoded total.

Next: [Part 6: Entry pages](6-entry-pages.md).
