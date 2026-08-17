# DynamicBookBreakdown

A working, self-contained rebuild of the Smithed Summit sticker book, extended into a field guide:
a dialog based book whose contents unlock per player at runtime.
A cover, two index spreads of 16 sticker slots each, and one entry page per pair.
Slots are greyed out until found, and clicking any slot opens its entry.

Read [COURSE.md](COURSE.md) for the full breakdown of how it works.

```sh
beet build                            # datapack + resourcepack into build/
python tools/preview_book.py docs/img # render pages to PNG without launching the game
python tools/generate_stickers.py     # rewrite the derived half of src/ from the sticker table
```

Index pages are hand written in [src/data/sticker_book/](src/data/sticker_book/). Entry pages are generated
at build time by [src/entry_pages/](src/entry_pages/), a beet plugin in the pipeline, because left aligned
text has to be measured before it can be positioned.

In game, `/function sticker_book:dev/unlock_all` and `/function sticker_book:dev/reset` drive the whole
thing; the book is handed to every player automatically.
