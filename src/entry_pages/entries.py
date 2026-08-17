""" The field guide half of every sticker: the extra lines an entry page shows next to the artwork.

Names and descriptions are not repeated here. They already live in the lang file under
sticker.sticker_book.<spread>.<id>, and the plugin reads them back from there, so this table only
carries what an entry page adds. The order of the rows is the order of the slots in the book.
"""
# Imports
from dataclasses import dataclass
from typing import ClassVar


# Classes
@dataclass(frozen=True)
class Kind:
	""" A preset filling the two taxonomy lines that repeat across many entries. """
	kingdom: str
	rank: str


@dataclass(frozen=True)
class Entry:
	""" One page of the field guide, pointing at the sticker it documents. """
	spread: str
	sticker_id: str
	found_in: str
	kind: Kind
	family: str
	genus: str


# Functions
class Kinds:
	""" The handful of presets the 32 entries draw from. """
	PLANT: ClassVar[Kind] = Kind(kingdom="Plantae", rank="Magnoliopsida")
	BIRD: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Aves")
	FISH: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Actinopterygii")
	REPTILE: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Reptilia")
	MAMMAL: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Mammalia")
	SHELLED: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Malacostraca")
	STAR: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Asteroidea")
	CORAL: ClassVar[Kind] = Kind(kingdom="Animalia", rank="Anthozoa")
	MINERAL: ClassVar[Kind] = Kind(kingdom="Mineralia", rank="Silicata")
	WEATHER: ClassVar[Kind] = Kind(kingdom="Phenomena", rank="Atmospherica")
	PLACE: ClassVar[Kind] = Kind(kingdom="Geologica", rank="Formatio")
	MADE: ClassVar[Kind] = Kind(kingdom="Artefacta", rank="Sculpta")


class Entries:
	""" Every entry of the book, in slot order, first spread then second. """

	ALL: ClassVar[list[Entry]] = [
		Entry(spread="tropics", sticker_id="palm",      found_in="Coastline",     kind=Kinds.PLANT,   family="Arecaceae",     genus="Cocos"),
		Entry(spread="tropics", sticker_id="sun",       found_in="Overhead",      kind=Kinds.WEATHER, family="Luminaria",     genus="Sol"),
		Entry(spread="tropics", sticker_id="parrot",    found_in="Canopy",        kind=Kinds.BIRD,    family="Psittacidae",   genus="Ara"),
		Entry(spread="tropics", sticker_id="pineapple", found_in="Clearings",     kind=Kinds.PLANT,   family="Bromeliaceae",  genus="Ananas"),
		Entry(spread="tropics", sticker_id="fish",      found_in="Reef",          kind=Kinds.FISH,    family="Pomacentridae", genus="Amphiprion"),
		Entry(spread="tropics", sticker_id="shell",     found_in="Tide line",     kind=Kinds.SHELLED, family="Turbinidae",    genus="Turbo"),
		Entry(spread="tropics", sticker_id="crab",      found_in="Tide line",     kind=Kinds.SHELLED, family="Coenobitidae",  genus="Coenobita"),
		Entry(spread="tropics", sticker_id="turtle",    found_in="Open water",    kind=Kinds.REPTILE, family="Cheloniidae",   genus="Chelonia"),
		Entry(spread="tropics", sticker_id="coconut",   found_in="Under palms",   kind=Kinds.PLANT,   family="Arecaceae",     genus="Cocos"),
		Entry(spread="tropics", sticker_id="starfish",  found_in="Rock pools",    kind=Kinds.STAR,    family="Asteriidae",    genus="Asterias"),
		Entry(spread="tropics", sticker_id="hibiscus",  found_in="Hedgerows",     kind=Kinds.PLANT,   family="Malvaceae",     genus="Hibiscus"),
		Entry(spread="tropics", sticker_id="coral",     found_in="Reef",          kind=Kinds.CORAL,   family="Gorgoniidae",   genus="Gorgonia"),
		Entry(spread="tropics", sticker_id="dolphin",   found_in="Open water",    kind=Kinds.MAMMAL,  family="Delphinidae",   genus="Delphinus"),
		Entry(spread="tropics", sticker_id="lagoon",    found_in="Inner shore",   kind=Kinds.PLACE,   family="Litoralia",     genus="Lacuna"),
		Entry(spread="tropics", sticker_id="tiki",      found_in="Trailheads",    kind=Kinds.MADE,    family="Lignaria",      genus="Persona"),
		Entry(spread="tropics", sticker_id="wave",      found_in="Point break",   kind=Kinds.WEATHER, family="Undaria",       genus="Unda"),

		Entry(spread="plateaus", sticker_id="mesa",       found_in="Skyline",      kind=Kinds.PLACE,   family="Stratigraphia", genus="Mensa"),
		Entry(spread="plateaus", sticker_id="cactus",     found_in="Flats",        kind=Kinds.PLANT,   family="Cactaceae",     genus="Carnegiea"),
		Entry(spread="plateaus", sticker_id="hawk",       found_in="Thermals",     kind=Kinds.BIRD,    family="Accipitridae",  genus="Buteo"),
		Entry(spread="plateaus", sticker_id="arch",       found_in="Ridgelines",   kind=Kinds.PLACE,   family="Erosiva",       genus="Arcus"),
		Entry(spread="plateaus", sticker_id="campfire",   found_in="Camps",        kind=Kinds.MADE,    family="Ignaria",       genus="Focus"),
		Entry(spread="plateaus", sticker_id="boulder",    found_in="Talus slopes", kind=Kinds.PLACE,   family="Erosiva",       genus="Saxum"),
		Entry(spread="plateaus", sticker_id="lizard",     found_in="Sun rocks",    kind=Kinds.REPTILE, family="Crotaphytidae", genus="Crotaphytus"),
		Entry(spread="plateaus", sticker_id="tumbleweed", found_in="Roadsides",    kind=Kinds.PLANT,   family="Amaranthaceae", genus="Salsola"),
		Entry(spread="plateaus", sticker_id="canyon",     found_in="Washes",       kind=Kinds.PLACE,   family="Erosiva",       genus="Fauces"),
		Entry(spread="plateaus", sticker_id="fossil",     found_in="Exposed beds", kind=Kinds.MINERAL, family="Petrifacta",    genus="Vestigium"),
		Entry(spread="plateaus", sticker_id="geode",      found_in="Dry creeks",   kind=Kinds.MINERAL, family="Silicata",      genus="Geoda"),
		Entry(spread="plateaus", sticker_id="dust_devil", found_in="Open flats",   kind=Kinds.WEATHER, family="Vorticia",      genus="Turbo"),
		Entry(spread="plateaus", sticker_id="coyote",     found_in="Everywhere",   kind=Kinds.MAMMAL,  family="Canidae",       genus="Canis"),
		Entry(spread="plateaus", sticker_id="sage",       found_in="Benches",      kind=Kinds.PLANT,   family="Asteraceae",    genus="Artemisia"),
		Entry(spread="plateaus", sticker_id="sunset",     found_in="Due west",     kind=Kinds.WEATHER, family="Luminaria",     genus="Vesper"),
		Entry(spread="plateaus", sticker_id="quarry",     found_in="Old workings", kind=Kinds.MADE,    family="Fossoria",      genus="Lapicidina"),
	]
	""" One row per sticker, in the exact order the slots appear in the index pages. """

