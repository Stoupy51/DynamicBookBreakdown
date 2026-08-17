# DynamicBookBreakdown

A working, self-contained rebuild of the Smithed Summit sticker book: a dialog based book whose contents
unlock per player at runtime. Three pages, 32 sticker slots, greyed out until found.

Read [COURSE.md](COURSE.md) for the full breakdown of how it works.

```sh
beet build                      # datapack + resourcepack into build/
python tools/preview_book.py    # render a page to PNG without launching the game
```

In game, `/function sticker_book:dev/unlock_all` and `/function sticker_book:dev/reset` drive the whole
thing; the book is handed to every player automatically.
