from enum import Enum
from typing import Self

from erdb.generators._base import GeneratorDataBase
from erdb.generators.armaments import ArmamentGeneratorData
from erdb.generators.armor import ArmorGeneratorData
from erdb.generators.ashes_of_war import AshOfWarGeneratorData
from erdb.generators.correction_attack import CorrectionAttackGeneratorData
from erdb.generators.correction_graph import CorrectionGraphGeneratorData
from erdb.generators.reinforcements import ReinforcementGeneratorData
from erdb.generators.spirit_ashes import SpiritAshGeneratorData
from erdb.generators.talismans import TalismanGeneratorData
from erdb.generators.spells import SpellGeneratorData
from erdb.generators.tools import ToolGeneratorData
from erdb.generators.crafting_materials import CraftingMaterialGeneratorData
from erdb.generators.bolstering_materials import BolsteringMaterialGeneratorData
from erdb.generators.keys import KeyGeneratorData
from erdb.generators.ammo import AmmoGeneratorData
from erdb.generators.shop import ShopGeneratorData
from erdb.generators.info import InfoGeneratorData
from erdb.generators.gestures import GestureGeneratorData
from erdb.typing.game_version import GameVersion


class Table(str, Enum):
    ALL = "all"
    ARMAMENTS = "armaments"
    ARMOR = "armor"
    ASHES_OF_WAR = "ashes-of-war"
    CORRECTION_ATTACK = "correction-attack"
    CORRECTION_GRAPH = "correction-graph"
    REINFORCEMENTS = "reinforcements"
    SPIRIT_ASHES = "spirit-ashes"
    TALISMANS = "talismans"
    SPELLS = "spells"
    TOOLS = "tools"
    CRAFTING_MATERIALS = "crafting-materials"
    BOLSTERING_MATERIALS = "bolstering-materials"
    KEYS = "keys"
    AMMO = "ammo"
    SHOP = "shop"
    INFO = "info"
    GESTURES = "gestures"

    def __str__(self):
        return self.value

    def __lt__(self, other: Self):
        assert isinstance(other, Table)
        return self.value < other.value

    @property
    def has_icons(self) -> bool:
        return self in (
            Table.ALL,
            Table.ARMAMENTS,
            Table.ARMOR,
            Table.ASHES_OF_WAR,
            Table.SPIRIT_ASHES,
            Table.TALISMANS,
            Table.SPELLS,
            Table.TOOLS,
            Table.CRAFTING_MATERIALS,
            Table.BOLSTERING_MATERIALS,
            Table.KEYS,
            Table.AMMO,
            Table.SHOP,
            Table.INFO,
            Table.GESTURES,
        )

    @property
    def title(self) -> str:
        return str(self).replace("-", " ").title()

    @property
    def stem(self) -> str:
        return {
            Table.ARMAMENTS: "EquipParamWeapon",
            Table.ARMOR: "EquipParamProtector",
            Table.ASHES_OF_WAR: "EquipParamGem",
            Table.CORRECTION_ATTACK: "AttackElementCorrectParam",
            Table.CORRECTION_GRAPH: "CalcCorrectGraph",
            Table.REINFORCEMENTS: "ReinforceParamWeapon",
            Table.SPIRIT_ASHES: "EquipParamGoods",
            Table.TALISMANS: "EquipParamAccessory",
            Table.SPELLS: "EquipParamGoods",
            Table.TOOLS: "EquipParamGoods",
            Table.CRAFTING_MATERIALS: "EquipParamGoods",
            Table.BOLSTERING_MATERIALS: "EquipParamGoods",
            Table.KEYS: "EquipParamGoods",
            Table.AMMO: "EquipParamWeapon",
            Table.SHOP: "EquipParamGoods",
            Table.INFO: "EquipParamGoods",
            Table.GESTURES: "EquipParamGoods",
        }[self]

    @property
    def id_range(self) -> tuple[int, int] | None:
        return {
            Table.SPIRIT_ASHES: (200000, 300000),
        }.get(self)

    @property
    def generator(self) -> GeneratorDataBase:
        return {
            Table.ARMAMENTS: ArmamentGeneratorData,
            Table.ARMOR: ArmorGeneratorData,
            Table.ASHES_OF_WAR: AshOfWarGeneratorData,
            Table.CORRECTION_ATTACK: CorrectionAttackGeneratorData,
            Table.CORRECTION_GRAPH: CorrectionGraphGeneratorData,
            Table.REINFORCEMENTS: ReinforcementGeneratorData,
            Table.SPIRIT_ASHES: SpiritAshGeneratorData,
            Table.TALISMANS: TalismanGeneratorData,
            Table.SPELLS: SpellGeneratorData,
            Table.TOOLS: ToolGeneratorData,
            Table.CRAFTING_MATERIALS: CraftingMaterialGeneratorData,
            Table.BOLSTERING_MATERIALS: BolsteringMaterialGeneratorData,
            Table.KEYS: KeyGeneratorData,
            Table.AMMO: AmmoGeneratorData,
            Table.SHOP: ShopGeneratorData,
            Table.INFO: InfoGeneratorData,
            Table.GESTURES: GestureGeneratorData,
        }[self]

    def make_generator(self, version: GameVersion) -> GeneratorDataBase:
        return self.generator.construct(version)

    @staticmethod
    def effective() -> list[Self]:
        s = set(Table)
        s.remove(Table.ALL)
        return list(s)