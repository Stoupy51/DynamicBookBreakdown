""" Beet plugin generating the entry pages of the sticker book.

The index pages in src/ are hand written on purpose: they are small enough to read. Entry pages are not,
because placing left aligned text means measuring it, and measuring it means every line of every page
has its own padding. So the whole of pages 4 and up is built here instead, from the sticker names and
descriptions already present in the lang file plus the extra fields in entries.py.
"""
# Imports
import json

from beet import Context, Function, Texture
from PIL import Image

from .entries import Entries, Entry
from .metrics import FontMetrics
from .pack import Pack
from .render import BODY_WIDTH, Spread

# Constants
NAMESPACE: str = "sticker_book"
""" Namespace of both packs. """

FIRST_ENTRY_PAGE: int = 4
""" Page number of the first entry page; 1 is the cover and 2 and 3 are the index spreads. """

ENTRIES_PER_PAGE: int = 2
""" One entry per half of the spread, exactly like the reference field guide. """

ENTRY_ACTION_BASE: int = 100
""" A slot click sends this plus its index, which action/open_entry turns back into a page number. """

SMALL_FONT_HEIGHT: int = 8
""" Rendered height of the body font, which is the cell height of the cropped sheet. """

SMALL_FONT_ASCENT: int = 7
""" Baseline of the body font, matching the vanilla convention for an 8 pixel sheet. """

PAGE_ASCENT: int = 11
""" Baseline of a page image, the same one the index spreads use. """

PAGE_GLYPHS: dict[str, tuple[str, str, int]] = {
	"gui.sticker_book.page.entry.left": (chr(0xE005), "book/entry_page_left.png", 195),
	"gui.sticker_book.page.entry.right": (chr(0xE006), "book/entry_page_right.png", 195),
}
""" Blank parchment pages the entries are written onto: character, texture and drawn height. """

VARIANTS: tuple[tuple[bool, bool], ...] = ((False, False), (True, False), (False, True), (True, True))
""" The four found / not found combinations a spread of two entries can be in. """


# Functions
def variant_name(found_left: bool, found_right: bool) -> str:
	""" Short suffix naming one of the four page variants. """
	return ("f" if found_left else "l") + ("f" if found_right else "l")


def build_metrics(ctx: Context) -> FontMetrics:
	""" Crop the tall toast sheet down to an 8 pixel body font, then measure everything the pages draw. """
	tall: Image.Image = ctx.assets.textures[f"{NAMESPACE}:font/ascii_tall"].image.convert("RGBA")
	cell_height: int = tall.height // 16
	small: Image.Image = Image.new("RGBA", (tall.width, 16 * SMALL_FONT_HEIGHT), (0, 0, 0, 0))
	for row in range(16):
		small.paste(tall.crop((0, row * cell_height, tall.width, row * cell_height + SMALL_FONT_HEIGHT)), (0, row * SMALL_FONT_HEIGHT))
	ctx.assets.textures[f"{NAMESPACE}:font/ascii_small"] = Texture(small)

	metrics: FontMetrics = FontMetrics()
	metrics.measure_sheet(small, ascii_grid(ctx), SMALL_FONT_HEIGHT)

	# Page images and sticker artwork share their lines with the text, and are measured the same way:
	# a glyph advances by its trimmed width, so the transparent margin of a sticker does not count
	lang: dict[str, str] = Pack.lang(ctx, f"{NAMESPACE}:en_us")
	for provider in Pack.bitmaps(ctx, f"{NAMESPACE}:assets"):
		metrics.measure_sheet(Pack.texture(ctx, provider.file), provider.chars, provider.height)
	for key, (character, texture, height) in PAGE_GLYPHS.items():
		metrics.measure_sheet(Pack.texture(ctx, f"{NAMESPACE}:{texture}"), [character], height)
		lang[key] = character
	return metrics


def ascii_grid(ctx: Context) -> list[str]:
	""" The 16x16 codepoint grid of the toast sheet, reused as-is by the cropped one. """
	for provider in Pack.bitmaps(ctx, f"{NAMESPACE}:advancement_text"):
		return provider.chars
	raise ValueError("advancement_text has no bitmap provider to take the codepoint grid from")


def register_font(ctx: Context, metrics: FontMetrics) -> None:
	""" Add the body font, the offset alphabet and a vanilla fallback to the book's font.

	Order matters: Minecraft keeps the first provider that defines a character, so the cropped sheet has
	to come before minecraft:include/default or the vanilla glyphs would win and every measurement here
	would be off.
	"""
	providers: list[dict[str, object]] = ctx.assets.fonts[f"{NAMESPACE}:assets"].data["providers"]
	for character, texture, height in PAGE_GLYPHS.values():
		providers.append({"type": "bitmap", "file": f"{NAMESPACE}:{texture}", "ascent": PAGE_ASCENT, "height": height, "chars": [character]})
	body_font: list[dict[str, object]] = [
		{"type": "reference", "id": "minecraft:include/space"},
		{"type": "bitmap", "file": f"{NAMESPACE}:font/ascii_small.png", "ascent": SMALL_FONT_ASCENT, "height": SMALL_FONT_HEIGHT, "chars": ascii_grid(ctx)},
		{"type": "space", "advances": metrics.offset_advances()},
		{"type": "reference", "id": "minecraft:include/default"},
	]
	providers += body_font


def navigation(page: int, last_page: int) -> dict[str, object]:
	""" Previous and next arrows, dropping the next one on the very last page of the book. """
	previous: dict[str, object] = {
		"translate": "gui.sticker_book.arrow.previous",
		"hover_event": {"action": "show_text", "value": {"translate": "gui.sticker_book.nav.previous"}},
		"click_event": {"action": "run_command", "command": "trigger sticker_book.action set 1"},
	}
	following: dict[str, object] = {
		"translate": "gui.sticker_book.arrow.next",
		"hover_event": {"action": "show_text", "value": {"translate": "gui.sticker_book.nav.next"}},
		"click_event": {"action": "run_command", "command": "trigger sticker_book.action set 2"},
	}
	if page == last_page:
		return {"translate": "gui.sticker_book.nav.left", "with": [previous]}
	return {"translate": "gui.sticker_book.nav.both", "with": [previous, following]}


def tabs() -> dict[str, object]:
	""" The tab strip, which always jumps back out of the entries and into an index page. """
	return {"translate": "gui.sticker_book.tabs", "with": [
		{
			"translate": f"gui.sticker_book.tab.{name}.idle",
			"hover_event": {"action": "show_text", "value": {"translate": f"gui.sticker_book.tab.{name}.hover"}},
			"click_event": {"action": "run_command", "command": f"trigger sticker_book.action set {value}"},
		}
		for name, value in (("front", 11), ("tropics", 12), ("plateaus", 13))
	]}


def dialog_command(contents: list[dict[str, object]], page: int, last_page: int) -> str:
	""" The single command a page variant compiles down to. """
	body: dict[str, object] = {
		"text": "",
		"font": f"{NAMESPACE}:assets",
		"color": "white",
		"shadow_color": 0,
		"extra": [*contents, {"text": "\n"}, navigation(page, last_page), {"text": "\n"}, tabs(), {"text": "\n\n\n\n"}],
	}
	dialog: dict[str, object] = {
		"type": "minecraft:multi_action",
		"title": {"translate": "gui.sticker_book.title"},
		"body": [{"type": "minecraft:plain_message", "width": BODY_WIDTH, "contents": body}],
		"inputs": [],
		"can_close_with_escape": True,
		"pause": False,
		"after_action": "none",
		"actions": [{
			"label": {"translate": "gui.sticker_book.done"},
			"width": BODY_WIDTH,
			"action": {"type": "run_command", "command": "trigger sticker_book.action set 3"},
		}],
	}
	return f"dialog show @s {json.dumps(dialog, ensure_ascii=False)}"


def build_pages(ctx: Context, metrics: FontMetrics) -> int:
	""" Write the four variants of every entry page plus the check that picks between them. """
	lang: dict[str, str] = Pack.lang(ctx, f"{NAMESPACE}:en_us")
	pairs: list[tuple[Entry, Entry]] = [
		(Entries.ALL[index], Entries.ALL[index + 1])
		for index in range(0, len(Entries.ALL), ENTRIES_PER_PAGE)
	]
	last_page: int = FIRST_ENTRY_PAGE + len(pairs) - 1

	for offset, (left, right) in enumerate(pairs):
		page: int = FIRST_ENTRY_PAGE + offset
		for found_left, found_right in VARIANTS:
			contents: list[dict[str, object]] = Spread.contents(left, right, found_left, found_right, lang, metrics)
			ctx.data[f"{NAMESPACE}:page/{page}/{variant_name(found_left, found_right)}"] = Function([dialog_command(contents, page, last_page)])

		checks: list[str] = ["# One line per variant, so nothing has to be recomputed while the book is open"]
		for found_left, found_right in VARIANTS:
			tests: str = " ".join(
				("if" if found else "unless") + f" entity @s[advancements={{{NAMESPACE}:sticker/{entry.spread}={{{entry.sticker_id}=true}}}}]"
				for entry, found in ((left, found_left), (right, found_right))
			)
			checks.append(f"execute {tests} run function {NAMESPACE}:page/{page}/{variant_name(found_left, found_right)}")
		ctx.data[f"{NAMESPACE}:page/{page}/check"] = Function(checks)

	return last_page


def build_datapack_glue(ctx: Context, last_page: int) -> None:
	""" Teach the rest of the pack that these pages exist and how a slot click reaches them. """
	ctx.data[f"{NAMESPACE}:entry/load"] = Function([
		"# Entry pages extend the book past the index, so the page clamp has to know about them",
		f"scoreboard players set $max {NAMESPACE}.page {last_page}",
		f"scoreboard players set $per_page {NAMESPACE}.page {ENTRIES_PER_PAGE}",
	])
	Pack.add_to_load_tag(ctx, f"{NAMESPACE}:entry/load")

	ctx.data[f"{NAMESPACE}:action/open_entry"] = Function([
		f"# A slot sends {ENTRY_ACTION_BASE} plus its index in the book, which maps onto one half of one page",
		f"scoreboard players operation @s {NAMESPACE}.page = @s {NAMESPACE}.action",
		f"scoreboard players remove @s {NAMESPACE}.page {ENTRY_ACTION_BASE}",
		f"scoreboard players operation @s {NAMESPACE}.page /= $per_page {NAMESPACE}.page",
		f"scoreboard players add @s {NAMESPACE}.page {FIRST_ENTRY_PAGE}",
		"",
		f"playsound {NAMESPACE}:section_flip player @s ~ ~ ~ 1 1",
	])


def beet_default(ctx: Context) -> None:
	""" Generate every entry page, the font they need and the wiring that reaches them. """
	metrics: FontMetrics = build_metrics(ctx)
	register_font(ctx, metrics)
	build_datapack_glue(ctx, build_pages(ctx, metrics))

