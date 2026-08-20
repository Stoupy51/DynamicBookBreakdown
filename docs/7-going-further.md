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

| Built path | What it contains |
|:--|:--|
| [`font/assets.json`](../build/resourcepack/assets/sticker_book/font/assets.json) | Page, tab, arrow and sticker glyphs, plus the space advances |
| [`font/toast.json`](../build/resourcepack/assets/sticker_book/font/toast.json) | The toast background strip |
| [`font/advancement_text.json`](../build/resourcepack/assets/sticker_book/font/advancement_text.json) | The tall ASCII sheet used for entry text |
| [`lang/en_us.json`](../build/resourcepack/assets/sticker_book/lang/en_us.json) | Index page layouts and all visible text |
| [`textures/book/`](../build/resourcepack/assets/sticker_book/textures/book/) | Pages, cover, tabs, arrows and the empty slot |
| [`textures/sticker/`](../build/resourcepack/assets/sticker_book/textures/sticker/) | One PNG per sticker |
| [`advancement/`](../build/datapack/data/sticker_book/advancement/) | One file per spread, each holding one criterion per sticker |
| [`function/page/`](../build/datapack/data/sticker_book/function/page/) | Cover, index spreads and generated entry pages |
| [`function/action/`](../build/datapack/data/sticker_book/function/action/) | The input handler behind the triggers |
| [`function/dev/`](../build/datapack/data/sticker_book/function/dev/) | `unlock_all`, `unlock_random_half`, `reset` |
| [`predicate/`](../build/datapack/data/sticker_book/predicate/) | Has the book, is holding the book and coin flip |

The generator source remains in [`entry_pages/`](../src/entry_pages/), alongside
[`patch_json_indent.py`](../src/patch_json_indent.py). The standalone tools are
[`generate_stickers.py`](../tools/generate_stickers.py) and
[`preview_book.py`](../tools/preview_book.py).

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
