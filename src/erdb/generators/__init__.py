from enum import StrEnum
from typing import Any, Self, NamedTuple

from erdb.generators._retrievers import RetrieverData
from erdb.generators._common import TableSpec
from erdb.generators.ammo import AmmoTableSpec
from erdb.generators.armaments import ArmamentTableSpec
from erdb.generators.armor import ArmorTableSpec
from erdb.generators.ashes_of_war import AshOfWarTableSpec
from erdb.generators.bolstering_materials import BolsteringMaterialTableSpec
from erdb.generators.correction_attack import CorrectionAttackTableSpec
from erdb.generators.correction_graph import CorrectionGraphTableSpec
from erdb.generators.crafting_materials import CraftingMaterialTableSpec
from erdb.generators.gestures import GestureTableSpec
from erdb.generators.info import InfoTableSpec
from erdb.generators.keys import KeyTableSpec
from erdb.generators.reinforcements import ReinforcementTableSpec
from erdb.generators.shop import ShopTableSpec
from erdb.generators.spells import SpellTableSpec
from erdb.generators.spirit_ashes import SpiritAshTableSpec
from erdb.generators.talismans import TalismanTableSpec
from erdb.generators.tools import ToolTableSpec
from erdb.typing.game_version import GameVersion
from erdb.typing.api_version import ApiVersion
from erdb.typing.params import ParamRow


class Generator(NamedTuple):
    spec: TableSpec
    data: RetrieverData

    def generate(self, api: ApiVersion | None = None) -> dict:
        api = self.spec.latest_api() if api is None else api

        def key(row: ParamRow) -> Any:
            return self.spec.get_pk(self.data, row)

        def value(row: ParamRow) -> Any:
            return self.spec.make_object(api, self.data, row)

        def valid(row: ParamRow) -> bool:
            return all(pred(row) for pred in self.spec.predicates)

        rows = self.data.main_param.values()
        return {key(row): value(row) for row in rows if valid(row)}

    @classmethod
    def create(cls, spec: TableSpec, version: GameVersion) -> Self:
        def retrieve_dict(retrievers: dict):
            return {field: retrievers[field].get(version) for field in retrievers.keys()}

        return cls(
            spec,
            RetrieverData(
                spec.main_param_retriever.get(version),
                retrieve_dict(spec.param_retrievers),
                retrieve_dict(spec.msg_retrievers),
                retrieve_dict(spec.shop_retrievers),
                spec.contrib_retriever.get(spec.title(), version),
            )
        )

class Table(StrEnum):
    ALL = "all"
    AMMO = "ammo"
    ARMAMENTS = "armaments"
    ARMOR = "armor"
    ASHES_OF_WAR = "ashes-of-war"
    BOLSTERING_MATERIALS = "bolstering-materials"
    CORRECTION_ATTACK = "correction-attack"
    CORRECTION_GRAPH = "correction-graph"
    CRAFTING_MATERIALS = "crafting-materials"
    GESTURES = "gestures"
    INFO = "info"
    KEYS = "keys"
    REINFORCEMENTS = "reinforcements"
    SHOP = "shop"
    SPELLS = "spells"
    SPIRIT_ASHES = "spirit-ashes"
    TASLISMANS = "talismans"
    TOOLS = "tools"

    def __str__(self):
        return self.value

    def __lt__(self, other: Self):
        assert isinstance(other, Table)
        return self.value < other.value

    def make_generator(self, version: GameVersion) -> Generator:
        return Generator.create(self.spec, version)

    @property
    def spec(self) -> TableSpec:
        return {
            Table.AMMO: AmmoTableSpec,
            Table.ARMAMENTS: ArmamentTableSpec,
            Table.ARMOR: ArmorTableSpec,
            Table.ASHES_OF_WAR: AshOfWarTableSpec,
            Table.BOLSTERING_MATERIALS: BolsteringMaterialTableSpec,
            Table.CORRECTION_ATTACK: CorrectionAttackTableSpec,
            Table.CORRECTION_GRAPH: CorrectionGraphTableSpec,
            Table.CRAFTING_MATERIALS: CraftingMaterialTableSpec,
            Table.GESTURES: GestureTableSpec,
            Table.INFO: InfoTableSpec,
            Table.KEYS: KeyTableSpec,
            Table.REINFORCEMENTS: ReinforcementTableSpec,
            Table.SHOP: ShopTableSpec,
            Table.SPELLS: SpellTableSpec,
            Table.SPIRIT_ASHES: SpiritAshTableSpec,
            Table.TASLISMANS: TalismanTableSpec,
            Table.TOOLS: ToolTableSpec,
        }[self]

    @property
    def id_range(self) -> tuple[int, int] | None:
        return {
            Table.SPIRIT_ASHES: (200000, 300000),
        }.get(self)

    @property
    def param_name(self) -> str:
        return self.spec.main_param_retriever.param_name

    @property
    def title(self) -> str:
        return str(self).replace("-", " ").title()

    @classmethod
    def effective(cls) -> list[Self]:
        s = set(Table)
        s.remove(Table.ALL)
        return list(s)