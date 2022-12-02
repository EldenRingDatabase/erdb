from erdb.typing.models.reinforcement import Reinforcement, ReinforcementLevel, DamageMultiplier, ScalingMultiplier, GuardMultiplier, ResistanceMultiplier
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import find_offset_indices
from erdb.table._retrievers import ParamDictRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def _get_damages(row: ParamRow) -> DamageMultiplier:
    return DamageMultiplier(
        physical=row["physicsAtkRate"].as_float,
        magic=row["magicAtkRate"].as_float,
        fire=row["fireAtkRate"].as_float,
        lightning=row["thunderAtkRate"].as_float,
        holy=row["darkAtkRate"].as_float,
        stamina=row["staminaAtkRate"].as_float,
    )

def _get_scalings(row: ParamRow) -> ScalingMultiplier:
    return ScalingMultiplier(
        strength=row["correctStrengthRate"].as_float,
        dexterity=row["correctAgilityRate"].as_float,
        intelligence=row["correctMagicRate"].as_float,
        faith=row["correctFaithRate"].as_float,
        arcane=row["correctLuckRate"].as_float,
    )

def _get_guards(row: ParamRow) -> GuardMultiplier:
    return GuardMultiplier(
        physical=row["physicsGuardCutRate"].as_float,
        magic=row["magicGuardCutRate"].as_float,
        fire=row["fireGuardCutRate"].as_float,
        lightning=row["thunderGuardCutRate"].as_float,
        holy=row["darkGuardCutRate"].as_float,
        guard_boost=row["staminaGuardDefRate"].as_float,
    )

def _get_resistances(row: ParamRow) -> ResistanceMultiplier:
    return ResistanceMultiplier(
        poison=row["poisonGuardResistRate"].as_float,
        scarlet_rot=row["diseaseGuardResistRate"].as_float,
        frostbite=row["freezeGuardDefRate"].as_float,
        bleed=row["bloodGuardResistRate"].as_float,
        sleep=row["sleepGuardDefRate"].as_float,
        madness=row["madnessGuardDefRate"].as_float,
        death_blight=row["curseGuardResistRate"].as_float,
    )

def _get_reinforcement_level(row: ParamRow, level: int) -> ReinforcementLevel:
    return ReinforcementLevel(
        level=level,
        damage=_get_damages(row),
        scaling=_get_scalings(row),
        guard=_get_guards(row),
        resistance=_get_resistances(row)
    )

class ReinforcementTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Reinforcement,
    }

    main_param_retriever = ParamDictRetriever("ReinforceParamWeapon", ItemIDFlag.NON_EQUIPABBLE)

    predicates: list[RowPredicate] = [
        lambda row: row.is_base_item,
        lambda row: len(row.name) > 0,
    ]

    @classmethod # override
    def get_pk(cls, data: RetrieverData, row: ParamRow) -> str:
        return str(row.index)

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        indices, offset = find_offset_indices(row.index, data.main_param, possible_maxima=[0, 10, 25])
        return Reinforcement([_get_reinforcement_level(data.main_param[i], lvl) for i, lvl in zip(indices, offset)])