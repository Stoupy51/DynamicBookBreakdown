# Part 7: Going further

What to change to turn this into your own field guide, and where everything lives.

## Making it yours

- **Bigger slot art.** A plant with its name underneath wants maybe 40x56 rather than 26x26. Redo the row
  arithmetic from [Part 2](2-drawing-a-page.md) with the new advance, remembering it is the trimmed advance.
  Nothing else in the system cares.
- **Unlocks from the world.** Anything that can run a function can call `sticker_book:unlock`: an
  advancement on `minecraft:player_interacted_with_entity`, an interaction entity, a `location` trigger for
  a biome. The book only cares that the criterion exists.
- **More fields, or fields that vary per entry.** `FIELD_LABELS` in
  [render.py](../src/entry_pages/render.py) is a tuple; making it per entry is one dataclass and one loop.
  Watch the vertical budget: a 195 pixel page is about seventeen usable 9 pixel lines, and navigation and
  tabs take the last two.
- **Real artwork.** The 32 generated stickers exist to be replaced. Drop PNGs into
  `textures/sticker/<spread>/` and delete the generator's `Textures` class.

The one structural decision worth making early is how many entries share a spread, because that sets the
variant count: two entries is four variants, three is eight, four is sixteen.

## File map

```
src/
  assets/sticker_book/
    font/assets.json            page, tab, arrow and sticker glyphs, plus the space advances
    font/toast.json             the toast background strip
    font/advancement_text.json  the tall ascii sheet the entry font is cropped from
    lang/en_us.json             the index page layouts and all visible text
    textures/book/              pages, cover, tabs, arrows, the empty slot
    textures/sticker/           one PNG per sticker
  data/sticker_book/
    advancement/                one file per spread, each holding one criterion per sticker
    function/page/1..3/         cover and index spreads: check picks the state, dialog shows it
    function/action/            the input handler behind the triggers
    function/dev/               unlock_all, unlock_random_half, reset
    predicate/                  has the book, is holding the book, coin flip
  entry_pages/                  generator: pages 4 and up, the body font, the offset alphabet
  patch_json_indent.py          readable JSON in the build output
tools/
  generate_stickers.py          rewrites the derived half of src/ from the sticker table
  preview_book.py               renders any page to PNG, from src/ or from build/
```

`assets/` and `data/` are an ordinary resource pack and datapack, and come back out that way in `build/`.
Only `entry_pages/` and `patch_json_indent.py` are beet plugins.

Porting it, the one thing to reproduce is the order: entry pages are generated after the hand written
functions are read and before the packs are zipped. Any build with a "read, add files, write" step in the
middle has that shape.

## Credits

The artwork, the book layout and the original implementation are from the Smithed Summit sticker book. This
repository reimplements the mechanism under its own namespace, with placeholder sticker art, so it can be
read and modified without the rest of Summit.

Back to [the index](../README.md).
