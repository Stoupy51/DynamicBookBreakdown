# Building a dynamic book in Minecraft

A book whose pages fill in as the player finds things, built out of a font, a dialog and a handful of
advancements. No GUI, no custom renderer, no entity. Everything you see below is text.

![The cover](docs/img/cover.png)

![A spread, eight of sixteen stickers found](docs/img/tropics.png)

This repository is a self-contained rebuild of the Smithed Summit sticker book, stripped of everything
Summit specific and extended into a field guide: a cover, two index spreads of sixteen slots each, and one
entry page per pair of stickers.

## The three ideas

**A font is a layout engine.** A resource pack font maps characters to images and to horizontal offsets,
and offsets are allowed to be negative. "Draw this image, move back 292 pixels, draw that one" is an
ordinary string. Once the cursor goes anywhere, a paragraph is a canvas.

**A book is a dialog.** Since 1.21.6 a datapack can push a window onto the player's screen with
`dialog show`. It holds text, and text holds click and hover events. That is the entire interface budget.

**An advancement is a save file.** Per player, survives restarts, queryable from a selector, toasts for
free. That is where "this player found the parrot" lives.

## The course

| Part | What it covers |
|:--|:--|
| [1. Fonts](docs/1-fonts.md) | Providers, types, height, ascent, advance, spaces. The concepts everything else assumes |
| [2. Drawing a page](docs/2-drawing-a-page.md) | Centring, the spread arithmetic, why the layout lives in the lang file |
| [3. The dialog](docs/3-the-dialog.md) | `dialog show`, and why every click goes through a trigger |
| [4. Player state](docs/4-player-state.md) | One advancement per spread, one criterion per sticker, and how a page reads it |
| [5. The rest of the pack](docs/5-the-pack.md) | The plumbing functions, and what adding a sticker costs |
| [6. Entry pages](docs/6-entry-pages.md) | Left aligned text, why it forces a build step, and the beet plugin that does it |
| [7. Going further](docs/7-going-further.md) | Turning this into your own field guide. File map and credits |

Parts 1 to 5 build the index pages, which are hand written and small enough to read in full. Part 6 covers
the generated half.

## Running it

```sh
beet build                            # datapack + resourcepack into build/
python tools/preview_book.py docs/img # render pages to PNG without launching the game
python tools/generate_stickers.py     # rewrite the derived half of src/ from the sticker table
```

In game, `/function sticker_book:dev/unlock_random_half` is the useful one: it flips a coin per sticker, so
every page lands in a different mix. `dev/unlock_all` and `dev/reset` do what they say. The book is handed
to every player automatically.

Start with [Part 1: Fonts](docs/1-fonts.md).

