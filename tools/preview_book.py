""" Render a page of the sticker book outside of Minecraft.

The layout rules implemented here are the ones the game uses for a dialog body: every line
is centred on its own total advance, a bitmap glyph advances by its width plus one pixel,
a space provider advances by exactly its declared value, and lines are nine pixels apart.
Getting a page wrong is a two second round trip here instead of a full game restart.
"""
# Imports
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# Constants
ASSETS: Path = Path(__file__).parent.parent / "src" / "assets" / "sticker_book"
""" Resource pack namespace holding the font, the lang file and the textures. """

LINE_HEIGHT: int = 9
""" Vertical distance between two consecutive lines of a dialog body. """

GLYPH_PADDING: int = 1
""" Extra pixel Minecraft adds after every bitmap glyph. """


# Classes
@dataclass(frozen=True)
class Glyph:
	""" One bitmap character: the already scaled image and how high above the baseline it starts. """
	image: Image.Image
	ascent: int


class Book:
	""" The font and the lang file of the pack, loaded once and queried by key. """

	def __init__(self) -> None:
		""" Read en_us.json and assets.json, scaling every bitmap to its declared height. """
		self.lang: dict[str, str] = json.loads((ASSETS / "lang" / "en_us.json").read_text(encoding="utf-8"))
		self.glyphs: dict[str, Glyph] = {}
		self.spaces: dict[str, int] = {}
		for provider in json.loads((ASSETS / "font" / "assets.json").read_text(encoding="utf-8"))["providers"]:
			if provider["type"] == "space":
				self.spaces.update(provider["advances"])
				continue
			source: Image.Image = Image.open(ASSETS / "textures" / provider["file"].split(":", 1)[1]).convert("RGBA")
			width: int = round(source.width * provider["height"] / source.height)
			self.glyphs[provider["chars"][0]] = Glyph(source.resize((width, provider["height"]), Image.NEAREST), provider["ascent"])

	def expand(self, key: str, arguments: list[str] | None = None) -> str:
		""" Replace every %n$s of a lang template by its argument, the way the game resolves a translate component.

		Examples:
			>>> Book().expand("gui.sticker_book.row", ["a", "b", "c", "d"])
			'abcd'
		"""
		arguments = arguments or []
		template: str = self.lang[key]
		out: str = ""
		index: int = 0
		while index < len(template):
			if template[index] == "%" and template[index + 2:index + 4] == "$s":
				out += arguments[int(template[index + 1]) - 1]
				index += 4
			else:
				out += template[index]
				index += 1
		return out

	def advance(self, character: str) -> int:
		""" Horizontal distance the cursor moves after drawing one character. """
		if character in self.spaces:
			return self.spaces[character]
		return self.glyphs[character].image.width + GLYPH_PADDING if character in self.glyphs else 0

	def render(self, text: str, size: tuple[int, int] = (420, 260), origin: tuple[int, int] = (210, 30)) -> Image.Image:
		""" Draw a resolved page, centring each line on its own total advance just like the game does. """
		canvas: Image.Image = Image.new("RGBA", size, (25, 25, 35, 255))
		for line_number, line in enumerate(text.split("\n")):
			x: float = -sum(self.advance(character) for character in line) / 2
			y: int = LINE_HEIGHT * line_number
			for character in line:
				if character in self.glyphs:
					glyph: Glyph = self.glyphs[character]
					canvas.alpha_composite(glyph.image, (int(origin[0] + x), int(origin[1] + y - glyph.ascent)))
				x += self.advance(character)
		return canvas


# Functions
class Pages:
	""" The three pages of the book, assembled exactly as their dialog functions assemble them. """

	@staticmethod
	def cover(book: Book, complete: bool) -> str:
		""" Cover page, with the completion sticker only present once the book is full. """
		return book.expand("gui.sticker_book.page.cover", [
			book.expand("gui.sticker_book.nav.front", [book.lang["gui.sticker_book.arrow.next_gold"]]),
			book.expand("gui.sticker_book.tabs.front", [
				book.lang["gui.sticker_book.tab.front.selected"],
				book.lang["gui.sticker_book.tab.tropics.idle"],
				book.lang["gui.sticker_book.tab.plateaus.idle"],
			]),
			book.lang["gui.sticker_book.completion"] if complete else "",
		])

	@staticmethod
	def spread(book: Book, spread_id: str, first_char: int, unlocked: int) -> str:
		""" One two page spread, showing the first n stickers as found and the rest as empty slots. """
		slots: list[str] = [chr(first_char + index) if index < unlocked else book.lang["gui.sticker_book.slot.locked"] for index in range(16)]
		rows: list[str] = [book.expand("gui.sticker_book.row", slots[start:start + 4]) for start in (0, 4, 8, 12)]
		return book.expand("gui.sticker_book.page.spread", [
			book.lang[f"gui.sticker_book.page.{spread_id}.right"],
			book.lang[f"gui.sticker_book.page.{spread_id}.left"],
			*rows,
			book.expand("gui.sticker_book.nav.both", [
				book.lang["gui.sticker_book.arrow.previous"],
				book.lang["gui.sticker_book.arrow.next"],
			]),
			book.expand("gui.sticker_book.tabs", [
				book.lang["gui.sticker_book.tab.front.idle"],
				book.lang[f"gui.sticker_book.tab.{spread_id}.selected"],
				book.lang["gui.sticker_book.tab.plateaus.idle"],
			]),
		])


def main() -> None:
	""" Write one PNG per page next to the script, or into the folder given as first argument. """
	destination: Path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
	destination.mkdir(parents=True, exist_ok=True)

	book: Book = Book()
	pages: dict[str, str] = {
		"cover": Pages.cover(book, complete=True),
		"tropics": Pages.spread(book, "tropics", 0xE100, unlocked=8),
		"plateaus": Pages.spread(book, "plateaus", 0xE120, unlocked=3),
	}
	for name, text in pages.items():
		book.render(text).convert("RGB").resize((840, 520), Image.NEAREST).save(destination / f"{name}.png")
		print(f"wrote {destination / f'{name}.png'}")


if __name__ == "__main__":
	main()
