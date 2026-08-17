""" Assembling one entry page out of runs, and the dialog command that shows it.

Every page exists in four variants, because the padding of a line depends on the width of everything
drawn on it: whether the left entry is found changes where the right entry starts. Solving all four at
build time is what lets the datapack side stay four lines of `execute if entity`.
"""
# Imports
from typing import ClassVar

from .entries import Entry
from .layout import Layout, Run
from .metrics import FontMetrics

# Constants
LEFT_BOX: int = -132
""" Left edge of the content area on the left page. """

RIGHT_BOX: int = 13
""" Left edge of the content area on the right page. """

BOX_WIDTH: int = 118
""" Usable width inside one page, once the drawn border is taken off. """

PAGE_CENTERS: tuple[float, float] = (-73.5, 72.0)
""" Horizontal centre of each page of the spread, used for the headings. """

ICON_ADVANCE: int = 27
""" A 26 pixel sticker plus the pixel Minecraft adds after every glyph. """

TEXT_INDENT: int = 31
""" Distance from the icon to the name written beside it. """

VALUE_INDENT: int = 52
""" Distance from a field label to its value. """

LAST_LINE: int = 15
""" Last line of the content block; navigation and tabs are appended after it. """

LINES: dict[str, int] = {"heading": 2, "icon": 3, "name": 4, "subtitle": 5, "fields": 8, "description": 13}
""" First line each part of an entry is written on.
The icon is a line above the name because it is 26 pixels tall: starting it there makes it span the
name and the subtitle rather than hang below them.
"""

FIELD_LABELS: tuple[str, ...] = ("Kingdom", "Class", "Family", "Genus")
""" Labels of the four taxonomy lines, in order. """

UNKNOWN: str = "???"
""" Placeholder standing in for every value of an entry that has not been found. """


# Functions
class Palette:
	""" Ink colours, picked to sit on the cream page texture rather than on a dark background. """
	HEADING: ClassVar[str] = "#7a5230"
	NAME: ClassVar[str] = "#43301d"
	SUBTITLE: ClassVar[str] = "#9c8a6a"
	LABEL: ClassVar[str] = "#7a5230"
	VALUE: ClassVar[str] = "#43301d"
	BODY: ClassVar[str] = "#6b5136"
	MISSING: ClassVar[str] = "#a8987e"


class EntryPage:
	""" Builds the run list of a single entry, on whichever half of the spread it belongs to. """

	@staticmethod
	def runs(entry: Entry, found: bool, box: int, centre: float, lang: dict[str, str], metrics: FontMetrics) -> dict[int, list[Run]]:
		""" Every run of one entry, keyed by the line it is written on. """
		key: str = f"{entry.spread}.{entry.sticker_id}"
		heading: str = lang[f"gui.sticker_book.tab.{entry.spread}.hover"]
		glyph: str = lang[f"gui.sticker_book.sticker.{key}"] if found else lang["gui.sticker_book.slot.locked"]
		name: str = lang[f"sticker.sticker_book.{key}"] if found else "Not Found Yet"
		found_in: str = entry.found_in if found else UNKNOWN
		values: tuple[str, ...] = (entry.kind.kingdom, entry.kind.rank, entry.family, entry.genus) if found else (UNKNOWN,) * 4

		lines: dict[int, list[Run]] = {
			LINES["heading"]: [Run(x=EntryPage.centred(heading, centre, metrics), text=heading, color=Palette.HEADING, bold=True)],
			LINES["icon"]: [Run(x=box, text=glyph)],
			LINES["name"]: [Run(x=box + TEXT_INDENT, text=name, color=Palette.NAME if found else Palette.MISSING, bold=True)],
			LINES["subtitle"]: [Run(x=box + TEXT_INDENT, text=f"Seen: {found_in}", color=Palette.SUBTITLE if found else Palette.MISSING)],
		}
		for index, (label, value) in enumerate(zip(FIELD_LABELS, values, strict=True)):
			lines[LINES["fields"] + index] = [
				Run(x=box, text=f"{label}:", color=Palette.LABEL, bold=True),
				Run(x=box + VALUE_INDENT, text=value, color=Palette.VALUE if found else Palette.MISSING),
			]
		if found:
			wrapped: list[str] = metrics.wrap(lang[f"sticker.sticker_book.{key}.desc"], BOX_WIDTH)
			for index, text in enumerate(wrapped[: LAST_LINE - LINES["description"] + 1]):
				lines[LINES["description"] + index] = [Run(x=box, text=text, color=Palette.BODY)]
		return lines

	@staticmethod
	def centred(text: str, centre: float, metrics: FontMetrics) -> int:
		""" Left edge that puts a run's own centre on a given x, since a page centre is not the line centre. """
		return round(centre - metrics.advance(text, bold=True) / 2)


class Spread:
	""" Merges the two halves of a spread into the component list a dialog body takes. """

	@staticmethod
	def contents(left: Entry, right: Entry, found_left: bool, found_right: bool, lang: dict[str, str], metrics: FontMetrics) -> list[dict[str, object]]:
		""" Component list for one of the four found / not found variants of a page. """
		lines: dict[int, list[Run]] = {1: [
			Run(x=-146, text=lang["gui.sticker_book.page.entry.left"]),
			Run(x=0, text=lang["gui.sticker_book.page.entry.right"]),
		]}
		halves: tuple[dict[int, list[Run]], dict[int, list[Run]]] = (
			EntryPage.runs(left, found_left, LEFT_BOX, PAGE_CENTERS[0], lang, metrics),
			EntryPage.runs(right, found_right, RIGHT_BOX, PAGE_CENTERS[1], lang, metrics),
		)
		for half in halves:
			for line_number, runs in half.items():
				lines.setdefault(line_number, []).extend(runs)
		for runs in lines.values():
			runs.sort(key=lambda run: run.x)
		return Layout.page(lines, metrics, LAST_LINE)
