from enum import Enum
from typing import Self

from erdb.typing.enums import GoodsSortGroupID, GoodsType
from erdb.typing.params import ParamRow


class _CategoryBase(str, Enum):
    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        assert False, "not implemented"

    @classmethod
    def from_row(cls, row: ParamRow) -> Self:
        if cat := cls.get(row):
            return cat
        raise KeyError

class AmmoCategory(_CategoryBase):
    ARROW = "Arrow"
    GREATARROW = "Greatarrow"
    BOLT = "Bolt"
    GREATBOLT = "Greatbolt"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        return {
            81: AmmoCategory.ARROW,
            83: AmmoCategory.GREATARROW,
            85: AmmoCategory.BOLT,
            86: AmmoCategory.GREATBOLT,
        }.get(row["wepType"].as_int)

class ArmamentCategory(_CategoryBase):
    DAGGER = "Dagger"
    STRAIGHT_SWORD = "Straight Sword"
    GREATSWORD = "Greatsword"
    COLOSSAL_SWORD = "Colossal Sword"
    CURVED_SWORD = "Curved Sword"
    CURVED_GREATSWORD = "Curved Greatsword"
    KATANA = "Katana"
    TWINBLADE = "Twinblade"
    THRUSTING_SWORD = "Thrusting Sword"
    HEAVY_THRUSTING_SWORD = "Heavy Thrusting Sword"
    AXE = "Axe"
    GREATAXE = "Greataxe"
    HAMMER = "Hammer"
    GREAT_HAMMER = "Great Hammer"
    FLAIL = "Flail"
    SPEAR = "Spear"
    GREAT_SPEAR = "Great Spear"
    HALBERD = "Halberd"
    REAPER = "Reaper"
    FIST = "Fist"
    CLAW = "Claw"
    WHIP = "Whip"
    COLOSSAL_WEAPON = "Colossal Weapon"
    LIGHT_BOW = "Light Bow"
    BOW = "Bow"
    GREATBOW = "Greatbow"
    CROSSBOW = "Crossbow"
    BALLISTA = "Ballista"
    GLINTSTONE_STAFF = "Glintstone Staff"
    SACRED_SEAL = "Sacred Seal"
    SMALL_SHIELD = "Small Shield"
    MEDIUM_SHIELD = "Medium Shield"
    GREATSHIELD = "Greatshield"
    TORCH = "Torch"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        return _ARMAMENT_CATEGORY_IDS.get(row["wepType"].as_int)

    @property
    def ingame(self) -> str:
        return _ARMAMENT_CATEGORY_INGAME[self]

class ArmorCategory(_CategoryBase):
    HEAD = "Head"
    BODY = "Body"
    ARMS = "Arms"
    LEGS = "Legs"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        return {
            0: ArmorCategory.HEAD,
            1: ArmorCategory.BODY,
            2: ArmorCategory.ARMS,
            3: ArmorCategory.LEGS,
        }.get(row["protectorCategory"].as_int)

class BolsteringMaterialCategory(_CategoryBase):
    FLASK = "Flask"
    SMITHING_STONE = "Smithing Stone"
    SOMBER_SMITHING_STONE = "Somber Smithing Stone"
    GLOVEWORT = "Glovewort"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        G = GoodsSortGroupID
        B = BolsteringMaterialCategory
        return {
            G.GROUP_1: B.FLASK,
            G.GROUP_2: B.SMITHING_STONE,
            G.GROUP_3: B.SOMBER_SMITHING_STONE,
            G.GROUP_4: B.GLOVEWORT,
        }.get(G(row["sortGroupId"].as_int))

class CraftingMaterialCategory(_CategoryBase):
    FAUNA = "Fauna"
    FLORA = "Flora"
    OBJECT = "Object"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        G = GoodsSortGroupID
        B = CraftingMaterialCategory
        return {
            G.GROUP_1: B.FAUNA,
            G.GROUP_2: B.FLORA,
            G.GROUP_3: B.OBJECT,
        }.get(G(row["sortGroupId"].as_int))

class InfoCategory(_CategoryBase):
    PAINTING = "Painting"
    NOTE = "Note"
    TUTORIAL = "Tutorial"
    CLUE = "Clue"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        G = GoodsSortGroupID
        I = InfoCategory
        return {
            G.GROUP_1: I.PAINTING if "Painting" in row.name else I.NOTE if "Note" in row.name else I.CLUE,
            G.GROUP_2: I.TUTORIAL,
        }.get(G(row["sortGroupId"].as_int))

class KeyCategory(_CategoryBase):
    GREAT_RUNE = "Great Rune"
    MENDING_RUNE = "Mending Rune"
    CONTAINER = "Container"
    EXPLORATION = "Exploration"
    QUEST = "Quest"
    EXCHANGE = "Exchange"
    FEATURE = "Feature"
    WHETBLADE = "Whetblade"
    MAP = "Map"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        K = KeyCategory
        G = GoodsSortGroupID

        for custom in (K.GREAT_RUNE, K.MENDING_RUNE, K.WHETBLADE):
            if custom.value in row.name:
                return custom

        return {
            G.GROUP_3: K.CONTAINER,
            G.GROUP_4: K.EXPLORATION,
            G.GROUP_5: K.EXCHANGE if row["isConsume"].as_bool else K.QUEST,
            G.GROUP_6: K.FEATURE,
            G.GROUP_7: K.MAP,
        }.get(G(row["sortGroupId"].as_int))

class ShopCategory(_CategoryBase):
    COOKBOOK = "Cookbook"
    BELL_BEARING = "Bell Bearing"
    SPELLBOOK = "Spellbook"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        G = GoodsSortGroupID
        S = ShopCategory
        return {
            G.GROUP_6: S.COOKBOOK,
            G.GROUP_8: S.BELL_BEARING,
            G.GROUP_9: S.BELL_BEARING,
            G.GROUP_10: S.SPELLBOOK,
        }.get(G(row["sortGroupId"].as_int))

class SpellCategory(_CategoryBase):
    INCANTATION = "Incantation"
    SORCERY = "Sorcery"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        return {
            0: SpellCategory.SORCERY,
            1: SpellCategory.INCANTATION,
        }.get(row["ezStateBehaviorType"].as_int)

class ToolCategory(_CategoryBase):
    ESSENTIAL = "Essential"
    EDIBLE = "Edible"
    POT = "Pot"
    AROMATIC = "Aromatic"
    THROWABLE = "Throwable"
    OFFENSIVE = "Offensive"
    GREASE = "Grease"
    UTILITY = "Utility"
    GOLDEN_RUNE = "Golden Rune"
    GREAT_RUNE = "Great Rune"
    REMEMBERANCE = "Rememberance"
    CRYSTAL_TEAR = "Crystal Tear"
    ONLINE = "Online"

    @classmethod
    def get(cls, row: ParamRow) -> Self | None:
        G = GoodsSortGroupID
        T = ToolCategory

        goods_type = row["goodsType"]

        if goods_type == GoodsType.WONDROUS_PHYSICK_TEAR:
            return T.CRYSTAL_TEAR

        if goods_type == GoodsType.GREAT_RUNE:
            return T.GREAT_RUNE

        return {
            G.GROUP_1: T.ESSENTIAL,
            G.GROUP_2: T.EDIBLE,
            G.GROUP_3: T.POT,
            G.GROUP_4: T.AROMATIC,
            G.GROUP_5: T.THROWABLE,
            G.GROUP_6: T.OFFENSIVE,
            G.GROUP_7: T.GREASE,
            G.GROUP_8: T.UTILITY,
            G.GROUP_9: T.UTILITY,
            G.GROUP_10: T.GOLDEN_RUNE,
            G.REMEMBERANCES: T.REMEMBERANCE,
            G.ONLINE: T.ONLINE
        }.get(G(row["sortGroupId"].as_int))

_ARMAMENT_CATEGORY_IDS: dict[int, ArmamentCategory] = {
    1: ArmamentCategory.DAGGER,
    3: ArmamentCategory.STRAIGHT_SWORD,
    5: ArmamentCategory.GREATSWORD,
    7: ArmamentCategory.COLOSSAL_SWORD,
    9: ArmamentCategory.CURVED_SWORD,
    11: ArmamentCategory.CURVED_GREATSWORD,
    13: ArmamentCategory.KATANA,
    14: ArmamentCategory.TWINBLADE,
    15: ArmamentCategory.THRUSTING_SWORD,
    16: ArmamentCategory.HEAVY_THRUSTING_SWORD,
    17: ArmamentCategory.AXE,
    19: ArmamentCategory.GREATAXE,
    21: ArmamentCategory.HAMMER,
    23: ArmamentCategory.GREAT_HAMMER,
    24: ArmamentCategory.FLAIL,
    25: ArmamentCategory.SPEAR,
    28: ArmamentCategory.GREAT_SPEAR,
    29: ArmamentCategory.HALBERD,
    31: ArmamentCategory.REAPER,
    35: ArmamentCategory.FIST,
    37: ArmamentCategory.CLAW,
    39: ArmamentCategory.WHIP,
    41: ArmamentCategory.COLOSSAL_WEAPON,
    50: ArmamentCategory.LIGHT_BOW,
    51: ArmamentCategory.BOW,
    53: ArmamentCategory.GREATBOW,
    55: ArmamentCategory.CROSSBOW,
    56: ArmamentCategory.BALLISTA,
    57: ArmamentCategory.GLINTSTONE_STAFF,
    61: ArmamentCategory.SACRED_SEAL,
    65: ArmamentCategory.SMALL_SHIELD,
    67: ArmamentCategory.MEDIUM_SHIELD,
    69: ArmamentCategory.GREATSHIELD,
    87: ArmamentCategory.TORCH,
}

_ARMAMENT_CATEGORY_INGAME: dict[ArmamentCategory, str] = {
    ArmamentCategory.DAGGER: "Dagger",
    ArmamentCategory.STRAIGHT_SWORD: "SwordNormal",
    ArmamentCategory.GREATSWORD: "SwordLarge",
    ArmamentCategory.COLOSSAL_SWORD: "SwordGigantic",
    ArmamentCategory.CURVED_SWORD: "SaberNormal",
    ArmamentCategory.CURVED_GREATSWORD: "SaberLarge",
    ArmamentCategory.KATANA: "katana", # yes, lowercase
    ArmamentCategory.TWINBLADE: "SwordDoubleEdge",
    ArmamentCategory.THRUSTING_SWORD: "SwordPierce",
    ArmamentCategory.HEAVY_THRUSTING_SWORD: "RapierHeavy",
    ArmamentCategory.AXE: "AxeNormal",
    ArmamentCategory.GREATAXE: "AxeLarge",
    ArmamentCategory.HAMMER: "HammerNormal",
    ArmamentCategory.GREAT_HAMMER: "HammerLarge",
    ArmamentCategory.FLAIL: "Flail",
    ArmamentCategory.SPEAR: "SpearNormal",
    # unused spear: "SpearLarge"
    ArmamentCategory.GREAT_SPEAR: "SpearHeavy",
    ArmamentCategory.HALBERD: "SpearAxe",
    ArmamentCategory.REAPER: "Sickle",
    ArmamentCategory.FIST: "Knuckle",
    ArmamentCategory.CLAW: "Claw",
    ArmamentCategory.WHIP: "Whip",
    ArmamentCategory.COLOSSAL_WEAPON: "AxhammerLarge",
    ArmamentCategory.LIGHT_BOW: "BowSmall",
    ArmamentCategory.BOW: "BowNormal",
    ArmamentCategory.GREATBOW: "BowLarge",
    ArmamentCategory.CROSSBOW: "ClossBow", # clossbow...
    ArmamentCategory.BALLISTA: "Ballista",
    ArmamentCategory.GLINTSTONE_STAFF: "Staff",
    # unused catalyst: "Sorcery"
    ArmamentCategory.SACRED_SEAL: "Talisman",
    ArmamentCategory.SMALL_SHIELD: "ShieldSmall",
    ArmamentCategory.MEDIUM_SHIELD: "ShieldNormal",
    ArmamentCategory.GREATSHIELD: "ShieldLarge",
    ArmamentCategory.TORCH: "Torch",
}