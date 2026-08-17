""" Render a page of the sticker book outside of Minecraft.

The layout rules implemented here are the ones the game uses for a dialog body: every line
is centred on its own total advance, a bitmap glyph advances by its width plus one pixel,
a space provider advances by exactly its declared value, and lines are nine pixels apart.
Getting a page wrong is a two second round trip here instead of a full game restart.

Index pages come out of src/ and are resolved from their lang templates. Entry pages only exist
after the build, so they are read straight back out of the dialog command in build/, which also
means this doubles as a check that the plugin emitted what it thinks it emitted.
"""
# Imports
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

# Constants
ROOT: Path = Path(__file__).parent.parent
""" Repository root. """

SOURCE_ASSETS: Path = ROOT / "src" / "assets" / "sticker_book"
""" Hand written half of the resource pack. """

BUILT_ASSETS: Path = ROOT / "build" / "resourcepack" / "assets" / "sticker_book"
""" Resource pack after the pipeline has run, including everything the plugin added. """

BUILT_FUNCTIONS: Path = ROOT / "build" / "datapack" / "data" / "sticker_book" / "function"
""" Data pack after the pipeline has run. """

LINE_HEIGHT: int = 9
""" Vertical distance between two consecutive lines of a dialog body. """

GLYPH_PADDING: int = 1
""" Extra pixel Minecraft adds after every bitmap glyph. """

BOLD_PADDING: int = 1
""" Extra advance a bold glyph gets. """

SPACE_ADVANCE: int = 4
""" Advance of U+0020, contributed by minecraft:include/space. """

PAGE_SIZE: tuple[int, int] = (420, 260)
""" Canvas the preview draws into, comfortably larger than a spread. """

PAGE_ORIGIN: tuple[int, int] = (210, 30)
""" Where the first baseline sits on that canvas. """

type Json = str | int | float | bool | list[Json] | dict[str, Json] | None
""" Everything json.loads can hand back.
Spelling the shape out is what lets isinstance narrow a font provider or a text component with no cast.
"""


# Classes
class Read:
	""" Narrowing helpers for parsed JSON, so a malformed file raises here instead of drawing nonsense. """

	@staticmethod
	def field(value: Json, key: str) -> Json:
		""" One member of an object, or None when the object does not have it.

		Examples:
			>>> Read.field({"a": 1}, "a")
			1
			>>> Read.field({"a": 1}, "b") is None
			True
		"""
		return value.get(key) if isinstance(value, dict) else None

	@staticmethod
	def array(value: Json) -> list[Json]:
		""" A JSON array, treating anything else as empty. """
		return value if isinstance(value, list) else []

	@staticmethod
	def mapping(value: Json) -> dict[str, Json]:
		""" A JSON object, treating anything else as empty. """
		return value if isinstance(value, dict) else {}

	@staticmethod
	def text(value: Json, default: str | None = None) -> str:
		""" A JSON string, falling back only when a default was offered. """
		if isinstance(value, str):
			return value
		if default is not None:
			return default
		raise TypeError(f"expected a string, got {value!r}")

	@staticmethod
	def number(value: Json, default: int | None = None) -> int:
		""" A JSON number, falling back only when a default was offered. """
		if isinstance(value, int) and not isinstance(value, bool):
			return value
		if isinstance(value, float):
			return round(value)
		if default is not None:
			return default
		raise TypeError(f"expected a number, got {value!r}")


@dataclass(frozen=True)
class Styled:
	""" A run of characters sharing one style, which is all the renderer needs to know. """
	text: str
	bold: bool = False
	color: str = ""


@dataclass(frozen=True)
class Glyph:
	""" One bitmap character: the drawn image, its baseline offset and the advance Minecraft gives it. """
	image: Image.Image
	ascent: int
	advance: int


class Book:
	""" The font and the lang file of the pack, loaded once and queried by key. """

	def __init__(self, assets: Path) -> None:
		""" Read en_us.json and assets.json, scaling every bitmap to its declared height. """
		self.assets: Path = assets
		self.lang: dict[str, str] = json.loads((assets / "lang" / "en_us.json").read_text(encoding="utf-8"))
		self.glyphs: dict[str, Glyph] = {}
		self.spaces: dict[str, int] = {}
		font: Json = json.loads((assets / "font" / "assets.json").read_text(encoding="utf-8"))
		for provider in Read.array(Read.field(font, "providers")):
			kind: str = Read.text(Read.field(provider, "type"), default="")
			if kind == "space":
				for character, advance in Read.mapping(Read.field(provider, "advances")).items():
					self.spaces[character] = Read.number(advance)
			elif kind == "bitmap":
				self.load_bitmap(provider)

	def load_bitmap(self, provider: Json) -> None:
		""" Slice a bitmap provider into glyphs, scaling every cell to the declared height. """
		reference: str = Read.text(Read.field(provider, "file"))
		source: Image.Image = Image.open(self.assets / "textures" / reference.split(":", 1)[1]).convert("RGBA")
		alpha: Image.Image = source.getchannel("A")
		grid: list[str] = [Read.text(row) for row in Read.array(Read.field(provider, "chars"))]
		ascent: int = Read.number(Read.field(provider, "ascent"))
		height: int = Read.number(Read.field(provider, "height"))
		cell: tuple[int, int] = (source.width // max(len(row) for row in grid), source.height // len(grid))
		scale: float = height / cell[1]
		for row_index, row in enumerate(grid):
			for column_index, character in enumerate(row):
				if ord(character) == 0:
					continue
				box: tuple[int, int, int, int] = (column_index * cell[0], row_index * cell[1], (column_index + 1) * cell[0], (row_index + 1) * cell[1])
				bounds: tuple[int, int, int, int] | None = alpha.crop(box).getbbox()
				trimmed: int = bounds[2] if bounds else 0
				image: Image.Image = source.crop(box).resize((max(1, round(cell[0] * scale)), height), Image.Resampling.NEAREST)
				self.glyphs[character] = Glyph(image, ascent, int(0.5 + trimmed * scale) + GLYPH_PADDING)

	def expand(self, key: str, arguments: list[str] | None = None) -> str:
		""" Replace every %n$s of a lang template by its argument, the way the game resolves a translate component.

		Examples:
			>>> Book(SOURCE_ASSETS).expand("gui.sticker_book.row", ["a", "b", "c", "d"])
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

	def advance(self, character: str, bold: bool = False) -> float:
		""" Horizontal distance the cursor moves after drawing one character. """
		if character in self.spaces:
			return self.spaces[character]
		if character == " ":
			return SPACE_ADVANCE
		if character not in self.glyphs:
			return 0.0
		return self.glyphs[character].advance + (BOLD_PADDING if bold else 0)

	def render(self, runs: list[Styled]) -> Image.Image:
		""" Draw a page, centring each line on its own total advance just like the game does. """
		canvas: Image.Image = Image.new("RGBA", PAGE_SIZE, (25, 25, 35, 255))
		lines: list[list[Styled]] = [[]]
		for run in runs:
			for index, piece in enumerate(run.text.split(chr(10))):
				if index:
					lines.append([])
				lines[-1].append(Styled(piece, run.bold, run.color))

		for line_number, line in enumerate(lines):
			x: float = -sum(self.advance(character, run.bold) for run in line for character in run.text) / 2
			y: int = LINE_HEIGHT * line_number
			for run in line:
				for character in run.text:
					if character in self.glyphs:
						glyph: Glyph = self.glyphs[character]
						canvas.alpha_composite(tint(glyph.image, run.color), (int(PAGE_ORIGIN[0] + x), int(PAGE_ORIGIN[1] + y - glyph.ascent)))
					x += self.advance(character, run.bold)
		return canvas


# Functions
class Pages:
	""" The pages of the book, assembled exactly as their dialog functions assemble them. """

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
		""" One index spread, showing the first n stickers as found and the rest as empty slots. """
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


class Built:
	""" Reads a generated entry page straight back out of its dialog command. """

	@staticmethod
	def runs(book: Book, page: int, variant: str) -> list[Styled]:
		""" Flatten the dialog body of one page variant into styled runs of characters. """
		command: str = (BUILT_FUNCTIONS / "page" / str(page) / f"{variant}.mcfunction").read_text(encoding="utf-8")
		command = re.sub(r"^\s*#.*$", "", command, flags=re.MULTILINE).strip()
		dialog: Json = json.loads(command[len("dialog show @s "):])
		body: Json = Read.array(Read.field(dialog, "body"))[0]
		out: list[Styled] = []
		Built.walk(book, Read.field(body, "contents"), out, Styled(""))
		return out

	@staticmethod
	def walk(book: Book, component: Json, out: list[Styled], style: Styled) -> None:
		""" Depth first walk of a text component, resolving translate keys against the lang file. """
		if isinstance(component, list):
			for child in component:
				Built.walk(book, child, out, style)
			return
		if isinstance(component, str):
			out.append(Styled(component, style.bold, style.color))
			return
		if not isinstance(component, dict):
			return

		style = Styled("", Read.field(component, "bold") is True or style.bold, Read.text(Read.field(component, "color"), default=style.color))
		if "text" in component:
			out.append(Styled(Read.text(component["text"]), style.bold, style.color))
		if "translate" in component:
			arguments: list[str] = []
			for argument in Read.array(Read.field(component, "with")):
				nested: list[Styled] = []
				Built.walk(book, argument, nested, style)
				arguments.append("".join(run.text for run in nested))
			out.append(Styled(book.expand(Read.text(component["translate"]), arguments), style.bold, style.color))
		for child in Read.array(Read.field(component, "extra")):
			Built.walk(book, child, out, style)


def main() -> None:
	""" Write one PNG per page into the folder given as first argument, or next to the script. """
	destination: Path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
	destination.mkdir(parents=True, exist_ok=True)

	source: Book = Book(SOURCE_ASSETS)
	for name, text in {
		"cover": Pages.cover(source, complete=True),
		"tropics": Pages.spread(source, "tropics", 0xE100, unlocked=8),
	}.items():
		save(source.render([Styled(text)]), destination / f"{name}.png")

	if not BUILT_ASSETS.exists():
		print("build/ is missing, run `beet build` to preview the generated entry pages")
		return
	built: Book = Book(BUILT_ASSETS)
	save(built.render(Built.runs(built, page=4, variant="ff")), destination / "entry_ff.png")


def tint(image: Image.Image, color: str) -> Image.Image:
	""" Multiply a white glyph by its text colour, which is what Minecraft does when it draws it. """
	if not color.startswith("#"):
		return image
	rgba: tuple[int, int, int, int] = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 255)
	solid: Image.Image = Image.new("RGBA", image.size, rgba)
	solid.putalpha(image.getchannel("A"))
	return solid


def save(image: Image.Image, path: Path) -> None:
	""" Write a preview at double size so single pixels stay visible. """
	image.convert("RGB").resize((PAGE_SIZE[0] * 2, PAGE_SIZE[1] * 2), Image.Resampling.NEAREST).save(path)
	print(f"wrote {path}")


if __name__ == "__main__":
	main()
