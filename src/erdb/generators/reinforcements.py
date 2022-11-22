from erdb.typing.models.reinforcement import Reinforcement, ReinforcementLevel, DamageMultiplier, ScalingMultiplier, GuardMultiplier, ResistanceMultiplier
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.utils.common import find_offset_indices
from erdb.generators._base import GeneratorDataBase


def _is_base_index(index: int) -> bool:
    return index == 0 or index % 100 == 0

def _get_damages(row: ParamRow) -> DamageMultiplier:
    return DamageMultiplier(
        physical=row.get_float("physicsAtkRate"),
        magic=row.get_float("magicAtkRate"),
        fire=row.get_float("fireAtkRate"),
        lightning=row.get_float("thunderAtkRate"),
        holy=row.get_float("darkAtkRate"),
        stamina=row.get_float("staminaAtkRate"),
    )

def _get_scalings(row: ParamRow) -> ScalingMultiplier:
    return ScalingMultiplier(
        strength=row.get_float("correctStrengthRate"),
        dexterity=row.get_float("correctAgilityRate"),
        intelligence=row.get_float("correctMagicRate"),
        faith=row.get_float("correctFaithRate"),
        arcane=row.get_float("correctLuckRate"),
    )

def _get_guards(row: ParamRow) -> GuardMultiplier:
    return GuardMultiplier(
        physical=row.get_float("physicsGuardCutRate"),
        magic=row.get_float("magicGuardCutRate"),
        fire=row.get_float("fireGuardCutRate"),
        lightning=row.get_float("thunderGuardCutRate"),
        holy=row.get_float("darkGuardCutRate"),
        guard_boost=row.get_float("staminaGuardDefRate"),
    )

def _get_resistances(row: ParamRow) -> ResistanceMultiplier:
    return ResistanceMultiplier(
        poison=row.get_float("poisonGuardResistRate"),
        scarlet_rot=row.get_float("diseaseGuardResistRate"),
        frostbite=row.get_float("freezeGuardDefRate"),
        bleed=row.get_float("bloodGuardResistRate"),
        sleep=row.get_float("sleepGuardDefRate"),
        madness=row.get_float("madnessGuardDefRate"),
        death_blight=row.get_float("curseGuardResistRate"),
    )

def _get_reinforcement_level(row: ParamRow, level: int) -> ReinforcementLevel:
    return ReinforcementLevel(
        level=level,
        damage=_get_damages(row),
        scaling=_get_scalings(row),
        guard=_get_guards(row),
        resistance=_get_resistances(row)
    )

class ReinforcementGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "reinforcements.json"

    @staticmethod # override
    def element_name() -> str:
        return "Reinforcements"

    @staticmethod # override
    def model() -> Reinforcement:
        return Reinforcement

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return str(row.index)

    main_param_retriever = Base.ParamDictRetriever("ReinforceParamWeapon", ItemIDFlag.NON_EQUIPABBLE)

    param_retrievers = {}
    msgs_retrievers = {}
    lookup_retrievers = {}

    def main_param_iterator(self, reinforcements: ParamDict):
        for row in reinforcements.values():
            if _is_base_index(row.index) and len(row.name) > 0: # NOTE: Paramdex coupling (row.name)
                yield row

    def construct_object(self, row: ParamRow) -> Reinforcement:
        indices, offset = find_offset_indices(row.index, self.main_param, possible_maxima=[0, 10, 25])
        return [_get_reinforcement_level(self.main_param[str(i)], lvl) for i, lvl in zip(indices, offset)]