""" Measuring a bitmap font exactly the way Minecraft does.

BitmapProvider computes an advance of `(int)(0.5 + trimmed_width * height / cell_height) + 1`, where
trimmed_width is one past the rightmost column of the cell holding a non transparent pixel. Bold adds
one more pixel per glyph. Reading those numbers off the PNG is the only way to left align text without
guessing, and it keeps working when the font is redrawn.
"""
# Imports
from dataclasses import dataclass, field

from PIL import Image

# Constants
GLYPH_PADDING: int = 1
""" Pixel Minecraft adds after every bitmap glyph. """

BOLD_PADDING: int = 1
""" Extra advance a bold glyph gets, from GlyphInfo.getBoldOffset. """

SPACE_ADVANCE: int = 4
""" Advance of U+0020, which minecraft:include/space contributes. """

OFFSET_ORIGIN: int = 0xD100
""" First character of the block encoding pixel offsets. """

OFFSET_MAGNITUDES: tuple[int, ...] = (1, 10, 100, 1000)
""" One decimal place per magnitude, so any offset under 10000 costs at most four characters. """


# Classes
@dataclass
class FontMetrics:
	""" Advance of every character the book can draw, plus the alphabet used to move the cursor. """

	advances: dict[str, float] = field(default_factory=dict[str, float])
	""" Advance in pixels, keyed by character. """

	def measure_sheet(self, sheet: Image.Image, grid: list[str], height: int) -> None:
		""" Record the advance of every glyph of a bitmap provider, from its own pixels. """
		alpha: Image.Image = sheet.convert("RGBA").getchannel("A")
		cell_width: int = sheet.width // max(len(row) for row in grid)
		cell_height: int = sheet.height // len(grid)
		scale: float = height / cell_height
		for row_index, row in enumerate(grid):
			for column_index, character in enumerate(row):
				if ord(character) == 0:
					continue
				box: tuple[int, int, int, int] = (column_index * cell_width, row_index * cell_height, (column_index + 1) * cell_width, (row_index + 1) * cell_height)
				bounds: tuple[int, int, int, int] | None = alpha.crop(box).getbbox()
				self.advances[character] = int(0.5 + (bounds[2] if bounds else 0) * scale) + GLYPH_PADDING

	def advance(self, text: str, bold: bool = False) -> float:
		""" Total advance of a string, which is what every position on a line is solved against.

		Examples:
			>>> metrics = FontMetrics({"a": 6.0, "b": 6.0})
			>>> metrics.advance("ab")
			12.0
			>>> metrics.advance("ab", bold=True)
			14.0
		"""
		total: float = 0.0
		for character in text:
			total += SPACE_ADVANCE if character == " " else self.advances.get(character, SPACE_ADVANCE)
			total += BOLD_PADDING if bold and character != " " else 0
		return total

	def offset(self, pixels: int) -> str:
		""" Encode a pixel offset as a short run of space characters.

		Examples:
			>>> FontMetrics().offset(0)
			''
			>>> len(FontMetrics().offset(-137))
			3
		"""
		remaining: int = abs(pixels)
		sign_slot: int = 0 if pixels >= 0 else 1
		out: str = ""
		for magnitude_index, magnitude in reversed(list(enumerate(OFFSET_MAGNITUDES))):
			digit: int = remaining // magnitude
			remaining -= digit * magnitude
			if digit:
				out += chr(OFFSET_ORIGIN + (magnitude_index * 9 + digit - 1) * 2 + sign_slot)
		return out

	def offset_advances(self) -> dict[str, int]:
		""" Every character of the offset alphabet, ready to drop into a space provider. """
		out: dict[str, int] = {}
		for magnitude_index, magnitude in enumerate(OFFSET_MAGNITUDES):
			for digit in range(1, 10):
				out[chr(OFFSET_ORIGIN + (magnitude_index * 9 + digit - 1) * 2)] = digit * magnitude
				out[chr(OFFSET_ORIGIN + (magnitude_index * 9 + digit - 1) * 2 + 1)] = -digit * magnitude
		return out

	def wrap(self, text: str, width: int, bold: bool = False) -> list[str]:
		""" Greedy word wrap against real advances rather than a character count.

		Examples:
			>>> FontMetrics({"a": 6.0}).wrap("aa aa aa", 30)
			['aa aa', 'aa']
		"""
		lines: list[str] = []
		current: str = ""
		for word in text.split():
			candidate: str = f"{current} {word}" if current else word
			if current and self.advance(candidate, bold) > width:
				lines.append(current)
				current = word
			else:
				current = candidate
		if current:
			lines.append(current)
		return lines

