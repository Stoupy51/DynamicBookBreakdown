""" Typed reads of the pack the plugin is handed.

beet hands back JsonDict, whose values are Any, so indexing a font provider type checks no matter what
is written there. Everything the plugin takes out of ctx goes through here instead, which turns a
malformed pack into an exception at build time rather than a page that quietly draws wrong.
"""
# Imports
from dataclasses import dataclass

from beet import Context
from PIL import Image

# Constants
type FontValue = str | int | list[str] | dict[str, int]
""" Every value a font provider holds.
Naming the union is what lets isinstance narrow it without a cast: assigning beet's Any into a declared
type turns it into something pyright can actually follow.
"""


# Classes
@dataclass(frozen=True)
class BitmapProvider:
	""" One bitmap entry of a font, reduced to the four fields the plugin needs. """
	file: str
	chars: list[str]
	height: int
	ascent: int


# Functions
class Pack:
	""" Everything the plugin reads out of the packs, narrowed on the way through. """

	@staticmethod
	def text(value: FontValue) -> str:
		""" Assert that a value coming out of a pack file really is a string. """
		if isinstance(value, str):
			return value
		raise TypeError(f"expected a string in the pack, got {value!r}")

	@staticmethod
	def number(value: FontValue) -> int:
		""" Assert that a value coming out of a pack file really is a whole number. """
		if isinstance(value, int) and not isinstance(value, bool):
			return value
		raise TypeError(f"expected a number in the pack, got {value!r}")

	@staticmethod
	def rows(value: FontValue) -> list[str]:
		""" Assert that a value coming out of a pack file really is a list of strings. """
		if isinstance(value, list):
			return value
		raise TypeError(f"expected a list in the pack, got {value!r}")

	@staticmethod
	def bitmaps(ctx: Context, font: str) -> list[BitmapProvider]:
		""" Every bitmap provider of a font, in declaration order. """
		out: list[BitmapProvider] = []
		for entry in ctx.assets.fonts[font].data["providers"]:
			provider: dict[str, FontValue] = entry
			if provider.get("type") != "bitmap":
				continue
			out.append(BitmapProvider(
				file=Pack.text(provider["file"]),
				chars=Pack.rows(provider["chars"]),
				height=Pack.number(provider["height"]),
				ascent=Pack.number(provider["ascent"]),
			))
		return out

	@staticmethod
	def texture(ctx: Context, reference: str) -> Image.Image:
		""" The image behind a font provider's file reference, as the pack currently holds it. """
		return ctx.assets.textures[reference.removesuffix(".png")].image.convert("RGBA")

	@staticmethod
	def lang(ctx: Context, language: str) -> dict[str, str]:
		""" The language file, which the plugin both reads entry text from and writes page glyphs into. """
		return ctx.assets.languages[language].data

	@staticmethod
	def add_to_load_tag(ctx: Context, function: str) -> None:
		""" Append a function to #minecraft:load, after everything already listed there. """
		values: list[str] = ctx.data.function_tags["minecraft:load"].data["values"]
		values.append(function)
