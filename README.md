# DynamicBookBreakdown

A working, self-contained rebuild of the Smithed Summit sticker book, extended into a field guide:
a dialog based book whose contents unlock per player at runtime.
A cover, two index spreads of 16 sticker slots each, and one entry page per pair.
Slots are greyed out until found, and clicking any slot opens its entry.

[COURSE.md](COURSE.md) is the breakdown, in seven parts:

| Part | What it covers |
|:--|:--|
| [1. Fonts](docs/1-fonts.md) | Providers, types, height, ascent, advance, spaces |
| [2. Drawing a page](docs/2-drawing-a-page.md) | Centring, the spread arithmetic, the lang file as layout |
| [3. The dialog](docs/3-the-dialog.md) | `dialog show`, and why every click goes through a trigger |
| [4. Player state](docs/4-player-state.md) | One advancement per spread, one criterion per sticker |
| [5. The rest of the pack](docs/5-the-pack.md) | The plumbing functions, and what adding a sticker costs |
| [6. Entry pages](docs/6-entry-pages.md) | Left aligned text, and the beet plugin it forces |
| [7. Going further](docs/7-going-further.md) | Making it yours. File map and credits |

```sh
beet build                            # datapack + resourcepack into build/
python tools/preview_book.py docs/img # render pages to PNG without launching the game
python tools/generate_stickers.py     # rewrite the derived half of src/ from the sticker table
```

Index pages are hand written in [src/data/sticker_book/](src/data/sticker_book/). Entry pages are generated
at build time by [src/entry_pages/](src/entry_pages/), a beet plugin in the pipeline, because left aligned
text has to be measured before it can be positioned.

In game, `/function sticker_book:dev/unlock_random_half` is the useful one: it flips a coin per sticker, so
every page lands in a different found / not found mix. `dev/unlock_all` and `dev/reset` do what they say.
The book is handed to every player automatically.

