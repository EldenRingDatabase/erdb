from enum import Enum
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