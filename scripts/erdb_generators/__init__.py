from enum import Enum
from typing import List, Optional, Tuple
from scripts.erdb_generators._base import GeneratorDataBase
from scripts.erdb_generators.armaments import ArmamentGeneratorData
from scripts.erdb_generators.armor import ArmorGeneratorData
from scripts.erdb_generators.ashes_of_war import AshOfWarGeneratorData
from scripts.erdb_generators.correction_attack import CorrectionAttackGeneratorData
from scripts.erdb_generators.correction_graph import CorrectionGraphGeneratorData
from scripts.erdb_generators.reinforcements import ReinforcementGeneratorData
from scripts.erdb_generators.spirit_ashes import SpiritAshGeneratorData
from scripts.erdb_generators.talismans import TalismanGeneratorData
from scripts.erdb_generators.spells import SpellGeneratorData
from scripts.erdb_generators.tools import ToolGeneratorData
from scripts.game_version import GameVersion

class GameParam(Enum):
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

    def __str__(self):
        return self.value

    def __lt__(self, other: "GameParam"):
        assert isinstance(other, GameParam)
        return self.value < other.value

    @property
    def has_icons(self) -> bool:
        return self in (
            GameParam.ALL,
            GameParam.ARMAMENTS,
            GameParam.ARMOR,
            GameParam.ASHES_OF_WAR,
            GameParam.SPIRIT_ASHES,
            GameParam.TALISMANS,
            GameParam.SPELLS,
            GameParam.TOOLS,
        )

    @property
    def title(self) -> str:
        return str(self).replace("-", " ").title()

    @property
    def stem(self) -> str:
        return {
            GameParam.ARMAMENTS: "EquipParamWeapon",
            GameParam.ARMOR: "EquipParamProtector",
            GameParam.ASHES_OF_WAR: "EquipParamGem",
            GameParam.CORRECTION_ATTACK: "AttackElementCorrectParam",
            GameParam.CORRECTION_GRAPH: "CalcCorrectGraph",
            GameParam.REINFORCEMENTS: "ReinforceParamWeapon",
            GameParam.SPIRIT_ASHES: "EquipParamGoods",
            GameParam.TALISMANS: "EquipParamAccessory",
            GameParam.SPELLS: "EquipParamGoods",
            GameParam.TOOLS: "EquipParamGoods",
        }[self]

    @property
    def id_range(self) -> Optional[Tuple[int, int]]:
        return {
            GameParam.SPIRIT_ASHES: (200000, 300000),
        }.get(self)

    def generator(self, version: GameVersion) -> GeneratorDataBase:
        return {
            GameParam.ARMAMENTS: ArmamentGeneratorData,
            GameParam.ARMOR: ArmorGeneratorData,
            GameParam.ASHES_OF_WAR: AshOfWarGeneratorData,
            GameParam.CORRECTION_ATTACK: CorrectionAttackGeneratorData,
            GameParam.CORRECTION_GRAPH: CorrectionGraphGeneratorData,
            GameParam.REINFORCEMENTS: ReinforcementGeneratorData,
            GameParam.SPIRIT_ASHES: SpiritAshGeneratorData,
            GameParam.TALISMANS: TalismanGeneratorData,
            GameParam.SPELLS: SpellGeneratorData,
            GameParam.TOOLS: ToolGeneratorData,
        }[self].construct(version)

    @staticmethod
    def effective() -> List["GameParam"]:
        s = set(GameParam)
        s.remove(GameParam.ALL)
        return list(s)