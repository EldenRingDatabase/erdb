from enum import Enum
from typing import Optional, Tuple
from scripts.erdb_generators._base import GeneratorDataBase
from scripts.erdb_generators.armaments import ArmamentGeneratorData
from scripts.erdb_generators.armor import ArmorGeneratorData
from scripts.erdb_generators.ashes_of_war import AshOfWarGeneratorData
from scripts.erdb_generators.correction_attack import CorrectionAttackGeneratorData
from scripts.erdb_generators.correction_graph import CorrectionGraphGeneratorData
from scripts.erdb_generators.reinforcements import ReinforcementGeneratorData
from scripts.erdb_generators.spirit_ashes import SpiritAshGeneratorData
from scripts.erdb_generators.talismans import TalismanGeneratorData
from scripts.game_version import GameVersion

ERDBGeneratorBase = GeneratorDataBase

class ERDBGenerator(Enum):
    ALL = "all"
    ARMAMENTS = "armaments"
    ARMOR = "armor"
    ASHES_OF_WAR = "ashes-of-war"
    CORRECTION_ATTACK = "correction-attack"
    CORRECTION_GRAPH = "correction-graph"
    REINFORCEMENTS = "reinforcements"
    SPIRIT_ASHES = "spirit-ashes"
    TALISMANS = "talismans"

    def __str__(self):
        return self.value

    @property
    def has_icons(self) -> bool:
        return self in (
            ERDBGenerator.ALL,
            ERDBGenerator.ARMAMENTS,
            ERDBGenerator.ARMOR,
            ERDBGenerator.ASHES_OF_WAR,
            ERDBGenerator.SPIRIT_ASHES,
            ERDBGenerator.TALISMANS,
        )

    @property
    def stem(self) -> str:
        return {
            ERDBGenerator.ARMAMENTS: "EquipParamWeapon",
            ERDBGenerator.ARMOR: "EquipParamProtector",
            ERDBGenerator.ASHES_OF_WAR: "EquipParamGem",
            ERDBGenerator.CORRECTION_ATTACK: "AttackElementCorrectParam",
            ERDBGenerator.CORRECTION_GRAPH: "CalcCorrectGraph",
            ERDBGenerator.REINFORCEMENTS: "ReinforceParamWeapon",
            ERDBGenerator.SPIRIT_ASHES: "EquipParamGoods",
            ERDBGenerator.TALISMANS: "EquipParamAccessory",
        }[self]

    @property
    def id_range(self) -> Optional[Tuple[int, int]]:
        return {
            ERDBGenerator.SPIRIT_ASHES: (200000, 300000),
        }.get(self)

    def construct(self, version: GameVersion) -> ERDBGeneratorBase:
        return {
            ERDBGenerator.ARMAMENTS: ArmamentGeneratorData,
            ERDBGenerator.ARMOR: ArmorGeneratorData,
            ERDBGenerator.ASHES_OF_WAR: AshOfWarGeneratorData,
            ERDBGenerator.CORRECTION_ATTACK: CorrectionAttackGeneratorData,
            ERDBGenerator.CORRECTION_GRAPH: CorrectionGraphGeneratorData,
            ERDBGenerator.REINFORCEMENTS: ReinforcementGeneratorData,
            ERDBGenerator.SPIRIT_ASHES: SpiritAshGeneratorData,
            ERDBGenerator.TALISMANS: TalismanGeneratorData,
        }[self].construct(version)