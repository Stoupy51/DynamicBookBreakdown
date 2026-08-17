""" Regenerate everything in src/ that is derived from the sticker table below.

Only the repetitive half of the pack is written from here: the placeholder artwork, the font,
the lang file, one advancement per sticker and the per page check functions. The hand written
logic (dialogs, actions, predicates, loot table) is never touched, so this is safe to re-run.
"""
# Imports
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from PIL import Image, ImageDraw

# Constants
SRC: Path = Path(__file__).parent.parent / "src"
""" Root of the beet source folder. """

RP: Path = SRC / "assets" / "sticker_book"
""" Resource pack namespace folder. """

DP: Path = SRC / "data" / "sticker_book"
""" Data pack namespace folder. """

DIGITS: dict[str, list[str]] = {
	"0": ["111", "101", "101", "101", "111"],
	"1": ["010", "110", "010", "010", "111"],
	"2": ["111", "001", "111", "100", "111"],
	"3": ["111", "001", "111", "001", "111"],
	"4": ["101", "101", "111", "001", "001"],
	"5": ["111", "100", "111", "001", "111"],
	"6": ["111", "100", "111", "101", "111"],
	"7": ["111", "001", "001", "001", "001"],
	"8": ["111", "101", "111", "101", "111"],
	"9": ["111", "101", "111", "001", "111"],
	"?": ["111", "001", "010", "000", "010"],
}
""" Tiny 3x5 pixel font used to number the placeholder stickers. """


# Classes
@dataclass(frozen=True)
class Sticker:
	""" One collectible sticker: its identity, where it sits in the book and what the tooltip says. """
	sticker_id: str
	name: str
	description: str
	hue: int


@dataclass(frozen=True)
class Spread:
	""" One two-page spread of the book, holding sixteen sticker slots. """
	spread_id: str
	title: str
	page: int
	stickers: list[Sticker]


# Functions
class Data:
	""" The whole book described once, so every generated file stays in sync. """

	TROPICS: ClassVar[list[Sticker]] = [
		Sticker(sticker_id="palm",      name="Palm Tree",     description="Standing tall on the beach.",        hue=95),
		Sticker(sticker_id="sun",       name="Blazing Sun",   description="Never sets over the tropics.",       hue=45),
		Sticker(sticker_id="parrot",    name="Parrot",        description="Repeats everything it hears.",       hue=10),
		Sticker(sticker_id="pineapple", name="Pineapple",     description="Sweet, spiky and stubborn.",         hue=50),
		Sticker(sticker_id="fish",      name="Reef Fish",     description="Darts between the coral heads.",     hue=190),
		Sticker(sticker_id="shell",     name="Spiral Shell",  description="Hold it up and hear the waves.",     hue=30),
		Sticker(sticker_id="crab",      name="Hermit Crab",   description="Always looking for a bigger home.",  hue=5),
		Sticker(sticker_id="turtle",    name="Sea Turtle",    description="In no hurry whatsoever.",            hue=140),
		Sticker(sticker_id="coconut",   name="Coconut",       description="Falls exactly where you stand.",     hue=25),
		Sticker(sticker_id="starfish",  name="Starfish",      description="Five arms, zero opinions.",          hue=20),
		Sticker(sticker_id="hibiscus",  name="Hibiscus",      description="Blooms for a single day.",           hue=340),
		Sticker(sticker_id="coral",     name="Coral Fan",     description="A whole city, built by tiny hands.", hue=310),
		Sticker(sticker_id="dolphin",   name="Dolphin",       description="Rides the bow wave for fun.",        hue=205),
		Sticker(sticker_id="lagoon",    name="Lagoon",        description="Warm, shallow and impossibly blue.", hue=175),
		Sticker(sticker_id="tiki",      name="Tiki Mask",     description="Carved to keep bad weather away.",   hue=15),
		Sticker(sticker_id="wave",      name="Rolling Wave",  description="The one every surfer waits for.",    hue=195),
	]
	""" The sixteen stickers of the first spread. """

	PLATEAUS: ClassVar[list[Sticker]] = [
		Sticker(sticker_id="mesa",        name="Red Mesa",      description="Layered like a stack of pancakes.",   hue=15),
		Sticker(sticker_id="cactus",      name="Saguaro",       description="Older than the road beside it.",      hue=110),
		Sticker(sticker_id="hawk",        name="Desert Hawk",   description="Circles all afternoon, lands once.",  hue=30),
		Sticker(sticker_id="arch",        name="Stone Arch",    description="Carved by nothing but wind.",         hue=20),
		Sticker(sticker_id="campfire",    name="Campfire",      description="The only warm thing for miles.",      hue=35),
		Sticker(sticker_id="boulder",     name="Balanced Rock", description="It has not fallen yet.",              hue=25),
		Sticker(sticker_id="lizard",      name="Collared Lizard", description="Runs on two legs when startled.",   hue=70),
		Sticker(sticker_id="tumbleweed",  name="Tumbleweed",    description="Going wherever the wind goes.",       hue=40),
		Sticker(sticker_id="canyon",      name="Slot Canyon",   description="Sunlight reaches the floor at noon.", hue=10),
		Sticker(sticker_id="fossil",      name="Fossil",        description="Someone else walked here first.",     hue=45),
		Sticker(sticker_id="geode",       name="Geode",         description="Plain outside, ridiculous inside.",   hue=275),
		Sticker(sticker_id="dust_devil",  name="Dust Devil",    description="A tornado that means no harm.",       hue=50),
		Sticker(sticker_id="coyote",      name="Coyote",        description="Heard far more often than seen.",     hue=30),
		Sticker(sticker_id="sage",        name="Desert Sage",   description="Smells like rain before it rains.",   hue=130),
		Sticker(sticker_id="sunset",      name="Mesa Sunset",   description="Twenty minutes of pure orange.",      hue=350),
		Sticker(sticker_id="quarry",      name="Old Quarry",    description="Half a mountain, moved by hand.",     hue=200),
	]
	""" The sixteen stickers of the second spread. """

	SPREADS: ClassVar[list[Spread]] = [
		Spread(spread_id="tropics",  title="Textured Tropics", page=2, stickers=TROPICS),
		Spread(spread_id="plateaus", title="Patched Plateaus", page=3, stickers=PLATEAUS),
	]
	""" Every spread of the book, in page order. """

	SPACES: ClassVar[list[int]] = [-292, 38, 204, 17, 112, 128, 80]
	""" Space advances, in the order the \\ud000+n characters are assigned. """

	@staticmethod
	def sticker_char(spread_index: int, slot_index: int) -> str:
		""" Private use character carrying the artwork of one sticker. """
		return chr(0xE100 + spread_index * 0x20 + slot_index)

	@staticmethod
	def write_json(path: Path, value: object) -> None:
		""" Write a JSON file with escaped private use characters so the source stays readable. """
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

	@staticmethod
	def write_text(path: Path, value: str) -> None:
		""" Write a plain text file, always ending with a single newline. """
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(value.rstrip("\n") + "\n", encoding="utf-8")


class Textures:
	""" Placeholder artwork generation, kept obviously temporary so it invites replacement. """

	@staticmethod
	def hsv_to_rgb(hue: int, saturation: float, value: float) -> tuple[int, int, int]:
		""" Convert an HSV colour to 8 bit RGB. """
		import colorsys
		r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
		return (int(r * 255), int(g * 255), int(b * 255))

	@staticmethod
	def draw_glyph(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, color: tuple[int, int, int, int]) -> None:
		""" Stamp a short string using the 3x5 pixel font. """
		for index, character in enumerate(text):
			rows: list[str] = DIGITS[character]
			for row_index, row in enumerate(rows):
				for column_index, pixel in enumerate(row):
					if pixel == "1":
						draw.point((x + index * 4 + column_index, y + row_index), fill=color)

	@staticmethod
	def sticker(number: int, hue: int) -> Image.Image:
		""" A 26x26 die cut placeholder sticker showing its own slot number. """
		image: Image.Image = Image.new("RGBA", (26, 26), (0, 0, 0, 0))
		draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
		draw.rounded_rectangle((3, 4, 23, 24), radius=5, fill=(0, 0, 0, 60))
		draw.rounded_rectangle((2, 2, 23, 23), radius=5, fill=(255, 255, 255, 255))
		draw.rounded_rectangle((4, 4, 21, 21), radius=4, fill=(*Textures.hsv_to_rgb(hue, 0.62, 0.86), 255))
		draw.rounded_rectangle((4, 4, 21, 9), radius=4, fill=(*Textures.hsv_to_rgb(hue, 0.42, 0.97), 255))
		Textures.draw_glyph(draw, f"{number:02d}", 9, 12, (255, 255, 255, 255))
		return image

	@staticmethod
	def locked() -> Image.Image:
		""" A 26x26 empty slot: the greyed out state every sticker starts in. """
		image: Image.Image = Image.new("RGBA", (26, 26), (0, 0, 0, 0))
		draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
		draw.rounded_rectangle((2, 2, 23, 23), radius=5, outline=(120, 106, 88, 130))
		Textures.draw_glyph(draw, "?", 11, 10, (120, 106, 88, 110))
		return image


def build_textures() -> None:
	""" Draw the placeholder slot artwork; the book, tab and arrow art is authored by hand and left alone. """
	(RP / "textures" / "book").mkdir(parents=True, exist_ok=True)
	Textures.locked().save(RP / "textures" / "book" / "slot_locked.png")
	for spread in Data.SPREADS:
		(RP / "textures" / "sticker" / spread.spread_id).mkdir(parents=True, exist_ok=True)
		for slot, sticker in enumerate(spread.stickers, start=1):
			Textures.sticker(slot, sticker.hue).save(RP / "textures" / "sticker" / spread.spread_id / f"{sticker.sticker_id}.png")


def build_fonts() -> None:
	""" Emit the three fonts: page assets, toast background and the tall advancement text. """
	providers: list[dict[str, object]] = [
		{"type": "bitmap", "file": "sticker_book:book/cover.png", "ascent": 11, "height": 195, "chars": ["\ue000"]},
	]
	for index, spread in enumerate(Data.SPREADS):
		providers.append({"type": "bitmap", "file": f"sticker_book:book/{spread.spread_id}_page_left.png", "ascent": 11, "height": 195, "chars": [chr(0xE001 + index * 2)]})
		providers.append({"type": "bitmap", "file": f"sticker_book:book/{spread.spread_id}_page_right.png", "ascent": 11, "height": 195, "chars": [chr(0xE002 + index * 2)]})

	providers.append({"type": "bitmap", "file": "sticker_book:book/front_tab_selected.png", "ascent": -32, "height": 14, "chars": ["\ue010"]})
	providers.append({"type": "bitmap", "file": "sticker_book:book/front_tab_idle.png", "ascent": -32, "height": 14, "chars": ["\ue011"]})
	for index, spread in enumerate(Data.SPREADS):
		providers.append({"type": "bitmap", "file": f"sticker_book:book/{spread.spread_id}_tab_selected.png", "ascent": -32, "height": 14, "chars": [chr(0xE012 + index * 2)]})
		providers.append({"type": "bitmap", "file": f"sticker_book:book/{spread.spread_id}_tab_idle.png", "ascent": -32, "height": 14, "chars": [chr(0xE013 + index * 2)]})

	providers.append({"type": "bitmap", "file": "sticker_book:book/previous_page.png", "ascent": -12, "height": 16, "chars": ["\ue020"]})
	providers.append({"type": "bitmap", "file": "sticker_book:book/next_page.png", "ascent": -12, "height": 16, "chars": ["\ue021"]})
	providers.append({"type": "bitmap", "file": "sticker_book:book/next_page_gold.png", "ascent": -12, "height": 16, "chars": ["\ue022"]})
	providers.append({"type": "bitmap", "file": "sticker_book:book/completion_sticker.png", "ascent": 25, "height": 40, "chars": ["\ue023"]})
	providers.append({"type": "bitmap", "file": "sticker_book:book/slot_locked.png", "ascent": -1, "height": 26, "chars": ["\ue030"]})

	for spread_index, spread in enumerate(Data.SPREADS):
		for slot_index, sticker in enumerate(spread.stickers):
			providers.append({
				"type": "bitmap",
				"file": f"sticker_book:sticker/{spread.spread_id}/{sticker.sticker_id}.png",
				"ascent": -1,
				"height": 26,
				"chars": [Data.sticker_char(spread_index, slot_index)],
			})

	providers.append({"type": "space", "advances": {chr(0xD000 + index): value for index, value in enumerate(Data.SPACES)}})
	Data.write_json(RP / "font" / "assets.json", {"providers": providers})

	Data.write_json(RP / "font" / "toast.json", {"providers": [
		{"type": "bitmap", "file": "sticker_book:advancement/toast.png", "ascent": 25, "height": 32, "chars": ["abcdefghijklmnopqrst"]},
		{"type": "space", "advances": {"\ue0a0": -30, "\ue0a1": -123, "\ue0a2": -1}},
	]})

	# advancement_text.json is hand authored: it only wraps the tall ascii sheet used by the toasts


def space(index: int) -> str:
	""" Character of the n-th space advance declared in Data.SPACES. """
	return chr(0xD000 + index)


def build_lang() -> None:
	""" Emit en_us.json: every layout template and every piece of visible text. """
	lang: dict[str, str] = {
		"item.sticker_book.book": "Sticker Book",
		"gui.sticker_book.title": "Sticker Book",
		"gui.sticker_book.done": "Close",

		"gui.sticker_book.tooltip": "%1$s\n%2$s",

		"gui.sticker_book.page.cover": "\ue000\n\n\n%3$s\n\n\n\n\n\n\n\n\n\n\n%1$s\n%2$s\n\n\n\n",
		"gui.sticker_book.page.spread": f"%1$s{space(0)}%2$s\n\n\n\n%3$s{space(1)}%4$s\n\n\n\n\n\n%5$s{space(1)}%6$s\n\n\n\n\n%7$s\n%8$s\n\n\n\n",
		"gui.sticker_book.row": "%1$s%2$s%3$s%4$s",

		"gui.sticker_book.nav.both": f"%1$s{space(2)}%2$s",
		"gui.sticker_book.nav.left": f"%1$s{space(2)}{space(3)}",
		"gui.sticker_book.nav.right": f"{space(2)}{space(3)}%1$s",
		"gui.sticker_book.nav.front": f"{space(4)}%1$s",
		"gui.sticker_book.nav.previous": "Previous page",
		"gui.sticker_book.nav.next": "Next page",

		"gui.sticker_book.tabs": f"{space(5)}%1$s%2$s%3$s",
		"gui.sticker_book.tabs.front": "%1$s%2$s%3$s",
		"gui.sticker_book.tab.front.selected": "\ue010",
		"gui.sticker_book.tab.front.idle": "\ue011",
		"gui.sticker_book.tab.front.hover": "Cover",

		"gui.sticker_book.arrow.previous": "\ue020",
		"gui.sticker_book.arrow.next": "\ue021",
		"gui.sticker_book.arrow.next_gold": "\ue022",

		"gui.sticker_book.completion": f"\ue023{space(6)}",
		"gui.sticker_book.completion.hover": "Every single sticker found. Nicely done.",
		"gui.sticker_book.slot.locked": "\ue030",
		"gui.sticker_book.slot.locked.name": "???",
		"gui.sticker_book.slot.locked.hover": "Still out there somewhere.",

		"gui.sticker_book.toast.background": "\ue0a0a\ue0a2b\ue0a2c\ue0a2d\ue0a2e\ue0a2f\ue0a2g\ue0a2h\ue0a2i\ue0a2j\ue0a2k\ue0a2l\ue0a2m\ue0a2n\ue0a2o\ue0a2p\ue0a2q\ue0a2r\ue0a2s\ue0a1",
		"gui.sticker_book.toast.text": " Sticker found!",
		"advancements.sticker_book.all_stickers.title": "Stick To It",
		"advancements.sticker_book.all_stickers.description": "Find every sticker in the book",
	}

	for index, spread in enumerate(Data.SPREADS):
		lang[f"gui.sticker_book.page.{spread.spread_id}.left"] = chr(0xE001 + index * 2)
		lang[f"gui.sticker_book.page.{spread.spread_id}.right"] = chr(0xE002 + index * 2)
		lang[f"gui.sticker_book.tab.{spread.spread_id}.selected"] = chr(0xE012 + index * 2)
		lang[f"gui.sticker_book.tab.{spread.spread_id}.idle"] = chr(0xE013 + index * 2)
		lang[f"gui.sticker_book.tab.{spread.spread_id}.hover"] = spread.title
		for slot_index, sticker in enumerate(spread.stickers):
			lang[f"gui.sticker_book.sticker.{spread.spread_id}.{sticker.sticker_id}"] = Data.sticker_char(index, slot_index)
			lang[f"sticker.sticker_book.{spread.spread_id}.{sticker.sticker_id}"] = sticker.name
			lang[f"sticker.sticker_book.{spread.spread_id}.{sticker.sticker_id}.desc"] = sticker.description

	lang["subtitles.sticker_book.section_flip"] = "Multiple pages turn"
	Data.write_json(RP / "lang" / "en_us.json", lang)


def build_resource_pack_misc() -> None:
	""" Item model, block model and the sound definition for the book itself. """
	Data.write_json(RP / "items" / "sticker_book.json", {"model": {"type": "minecraft:model", "model": "sticker_book:item/sticker_book"}})
	Data.write_json(RP / "models" / "item" / "sticker_book.json", {"parent": "minecraft:item/generated", "textures": {"layer0": "sticker_book:item/sticker_book", "particle": "#layer0"}})
	Data.write_json(RP / "sounds.json", {"section_flip": {"sounds": [{"name": "sticker_book:section_flip", "volume": 0.5}], "subtitle": "subtitles.sticker_book.section_flip"}})


def build_advancements() -> None:
	""" One advancement per sticker: it is both the saved unlock flag and the toast. """
	Data.write_json(DP / "advancement" / "root.json", {
		"criteria": {"requirement": {"trigger": "minecraft:impossible"}},
	})
	for spread in Data.SPREADS:
		for sticker in spread.stickers:
			Data.write_json(DP / "advancement" / "sticker" / spread.spread_id / f"{sticker.sticker_id}.json", {
				"parent": "sticker_book:root",
				"display": {
					"title": [
						{"translate": "gui.sticker_book.toast.background", "font": "sticker_book:toast"},
						{"translate": "gui.sticker_book.toast.text", "font": "sticker_book:advancement_text", "color": "#4d7d9b"},
					],
					"icon": {"id": "minecraft:poisonous_potato", "components": {"minecraft:item_model": "sticker_book:sticker_book"}},
					"description": "",
					"announce_to_chat": False,
				},
				"criteria": {"requirement": {"trigger": "minecraft:impossible"}},
				"rewards": {"function": "sticker_book:on_sticker_found"},
			})

	Data.write_json(DP / "advancement" / "all_stickers.json", {
		"parent": "sticker_book:root",
		"display": {
			"title": {"translate": "advancements.sticker_book.all_stickers.title"},
			"description": {"translate": "advancements.sticker_book.all_stickers.description"},
			"icon": {"id": "minecraft:poisonous_potato", "components": {"minecraft:item_model": "sticker_book:sticker_book"}},
			"frame": "challenge",
			"announce_to_chat": False,
		},
		"criteria": {"requirement": {"trigger": "minecraft:impossible"}},
		"rewards": {"function": "sticker_book:on_book_complete"},
	})


def slot_component(spread: Spread, sticker: Sticker) -> str:
	""" Text component of an unlocked slot, stored as a macro friendly single quoted string. """
	key: str = f"{spread.spread_id}.{sticker.sticker_id}"
	return (
		"{"
		f"translate:'gui.sticker_book.sticker.{key}',"
		"hover_event:{action:'show_text',value:{translate:'gui.sticker_book.tooltip',with:["
		f"{{translate:'sticker.sticker_book.{key}',color:'gold'}},"
		f"{{translate:'sticker.sticker_book.{key}.desc',color:'gray'}}"
		"]}}"
		"}"
	)


def build_page_functions() -> None:
	""" Per page check functions, which decide the state of every slot before showing the dialog. """
	for spread in Data.SPREADS:
		lines: list[str] = [
			"# Start from a fully locked page, then reveal only what this player has already found",
			"data modify storage sticker_book:temp page set from storage sticker_book:const locked_page",
			"",
		]
		for slot, sticker in enumerate(spread.stickers, start=1):
			condition: str = f"@s[advancements={{sticker_book:sticker/{spread.spread_id}/{sticker.sticker_id}=true}}]"
			lines.append(f'execute if entity {condition} run data modify storage sticker_book:temp page.slot_{slot} set value "{slot_component(spread, sticker)}"')
		lines += [
			"",
			f"function sticker_book:page/{spread.page}/dialog with storage sticker_book:temp page",
		]
		Data.write_text(DP / "function" / "page" / str(spread.page) / "check.mcfunction", "\n".join(lines))


def build_const_function() -> None:
	""" Load time storage holding the locked slot component, copied into every page. """
	locked: str = (
		"{"
		"translate:'gui.sticker_book.slot.locked',"
		"hover_event:{action:'show_text',value:{translate:'gui.sticker_book.tooltip',with:["
		"{translate:'gui.sticker_book.slot.locked.name',color:'dark_gray'},"
		"{translate:'gui.sticker_book.slot.locked.hover',color:'gray'}"
		"]}}"
		"}"
	)
	slots: str = ",".join(f'slot_{index}:"{locked}"' for index in range(1, 17))
	Data.write_text(DP / "function" / "const.mcfunction", "\n".join([
		"# Every slot of a page starts locked, so a page check only has to overwrite the ones that are unlocked",
		f"data modify storage sticker_book:const locked_page set value {{{slots}}}",
	]))


def build_counting() -> None:
	""" The total number of stickers, written where the datapack can compare against it. """
	total: int = sum(len(spread.stickers) for spread in Data.SPREADS)
	Data.write_text(DP / "function" / "on_sticker_found.mcfunction", "\n".join([
		"# Run by every sticker advancement the first time it is granted, never again afterwards",
		"scoreboard players add @s sticker_book.found 1",
		"",
		"playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6",
		"",
		f"execute if score @s sticker_book.found matches {total}.. run advancement grant @s only sticker_book:all_stickers",
	]))


def main() -> None:
	""" Rewrite only the derived files, so a stale sticker never survives a rename. """
	shutil.rmtree(DP / "advancement" / "sticker", ignore_errors=True)
	shutil.rmtree(RP / "textures" / "sticker", ignore_errors=True)
	build_textures()
	build_fonts()
	build_lang()
	build_resource_pack_misc()
	build_advancements()
	build_page_functions()
	build_const_function()
	build_counting()
	print("generated")


main()

