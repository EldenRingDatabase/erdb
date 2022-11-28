from erdb.typing.models.armament import Armament, AffinityProperties, Guard, CorrectionCalcID, Scaling
from erdb.typing.models.common import Damage, StatRequirements
from erdb.typing.models.effect import Effect, StatusEffects
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import Affinity, AttackCondition, ItemIDFlag, AshOfWarMountType, AttackAttribute, ArmamentUpgradeMaterial
from erdb.typing.categories import ArmamentCategory
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import find_offset_indices, remove_nulls
from erdb.effect_parser import parse_effects, parse_status_effects, parse_weapon_effects
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


_BEHAVIOR_EFFECTS_FIELDS: list[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]
_RESIDENT_EFFECTS_FIELDS: list[str] = ["residentSpEffectId", "residentSpEffectId1", "residentSpEffectId2"]

def _get_attack_attributes(row: ParamRow) -> list[AttackAttribute]:
    attributes = {AttackAttribute.from_id(row[field].as_int) for field in ["atkAttribute", "atkAttribute2"]}
    return sorted(list(attributes))

def _get_upgrade_costs(row: ParamRow, reinforces: ParamDict) -> list[int]:
    reinforcement_id = row["reinforceTypeId"].as_int

    reinforcement = reinforces[reinforcement_id]
    base_price = row["reinforcePrice"].as_int

    indices, _ = find_offset_indices(reinforcement.index, reinforces, possible_maxima=[0, 10, 25])
    next(indices) # ignore first index

    return [round(base_price * reinforces[i]["reinforcePriceRate"].as_float) for i in indices]

def _get_correction_calc_ids(row: ParamRow) -> CorrectionCalcID:
    return CorrectionCalcID(
        physical=row["correctType_Physics"].as_int,
        magic=row["correctType_Magic"].as_int,
        fire=row["correctType_Fire"].as_int,
        lightning=row["correctType_Thunder"].as_int,
        holy=row["correctType_Dark"].as_int,
        poison=row["correctType_Poison"].as_int,
        bleed=row["correctType_Blood"].as_int,
        sleep=row["correctType_Sleep"].as_int,
        madness=row["correctType_Madness"].as_int
    )

def _get_requirements(row: ParamRow) -> StatRequirements:
    data = {
        "strength": row["properStrength"].get_int(null_value=0),
        "dexterity": row["properAgility"].get_int(null_value=0),
        "intelligence": row["properMagic"].get_int(null_value=0),
        "faith": row["properFaith"].get_int(null_value=0),
        "arcane": row["properLuck"].get_int(null_value=0),
    }

    return StatRequirements(**remove_nulls(data))

def _get_damages(row: ParamRow) -> Damage:
    data = {
        "physical": row["attackBasePhysics"].get_int(null_value=0),
        "magic": row["attackBaseMagic"].get_int(null_value=0),
        "fire": row["attackBaseFire"].get_int(null_value=0),
        "lightning": row["attackBaseThunder"].get_int(null_value=0),
        "holy": row["attackBaseDark"].get_int(null_value=0),
        "stamina": row["attackBaseStamina"].get_int(null_value=0),
    }

    return Damage(**remove_nulls(data))

def _get_scalings(row: ParamRow) -> Scaling:
    formatter = lambda x: x / 100.
    data = {
        "strength": row["correctStrength"].get_float(null_value=0, formatter=formatter),
        "dexterity": row["correctAgility"].get_float(null_value=0, formatter=formatter),
        "intelligence": row["correctMagic"].get_float(null_value=0, formatter=formatter),
        "faith": row["correctFaith"].get_float(null_value=0, formatter=formatter),
        "arcane": row["correctLuck"].get_float(null_value=0, formatter=formatter),
    }

    return Scaling(**remove_nulls(data))

def _get_guards(row: ParamRow) -> Guard:
    data = {
        "physical": row["physGuardCutRate"].get_float(null_value=0),
        "magic": row["magGuardCutRate"].get_float(null_value=0),
        "fire": row["fireGuardCutRate"].get_float(null_value=0),
        "lightning": row["thunGuardCutRate"].get_float(null_value=0),
        "holy": row["darkGuardCutRate"].get_float(null_value=0),
        "guard_boost": row["staminaGuardDef"].get_float(null_value=0),
    }

    return Guard(**remove_nulls(data))

def _get_resistances(row: ParamRow) -> StatusEffects:
    data = {
        "poison": row["poisonGuardResist"].get_int(null_value=0),
        "scarlet_rot": row["diseaseGuardResist"].get_int(null_value=0),
        "frostbite": row["freezeGuardResist"].get_int(null_value=0),
        "bleed": row["bloodGuardResist"].get_int(null_value=0),
        "sleep": row["sleepGuardResist"].get_int(null_value=0),
        "madness": row["madnessGuardResist"].get_int(null_value=0),
        "death_blight": row["curseGuardResist"].get_int(null_value=0),
    }

    return StatusEffects(**remove_nulls(data))

def get_status_effect_overlay(row: ParamRow, effects: ParamDict, reinforces: ParamDict, reinforcement_id: int) -> list[StatusEffects]:
    if (reinforcement := reinforces.get(reinforcement_id + 1)) is None:
        return []

    effect_fields = ["spEffectId1", "spEffectId2", "spEffectId3"]
    effect_fields = [f for f in effect_fields if reinforcement[f].as_int > 0]

    assert len(effect_fields) <= 1, "Up to one effect field can have offset added"

    if len(effect_fields) == 0:
        return []

    assert (reinforcement_id + 25) in reinforces, "Only +25 reinforcements upgrade status effects"

    weapfield = {
        "spEffectId1": "spEffectBehaviorId0",
        "spEffectId2": "spEffectBehaviorId1",
        "spEffectId3": "spEffectBehaviorId2",
    }[effect_fields[0]]

    effect_ids = [row[weapfield].as_int + offset for offset in range(0, 26)]
    return [parse_status_effects([i], effects) for i in effect_ids]

def _get_affinity_properties(row: ParamRow, effects: ParamDict, reinforces: ParamDict) -> AffinityProperties:
    reinforcement_id = row["reinforceTypeId"].as_int
    return AffinityProperties(
        full_hex_id=row.index_hex,
        id=row.index,
        reinforcement_id=reinforcement_id,
        correction_attack_id=row["attackElementCorrectId"].as_int,
        correction_calc_id=_get_correction_calc_ids(row),
        damage=_get_damages(row),
        scaling=_get_scalings(row),
        guard=_get_guards(row),
        resistance=_get_resistances(row),
        status_effects=parse_status_effects([row[f].as_int for f in _BEHAVIOR_EFFECTS_FIELDS], effects),
        status_effect_overlay=get_status_effect_overlay(row, effects, reinforces, reinforcement_id),
    )

def _get_affinities(row: ParamRow, armaments: ParamDict, effects: ParamDict, reinforces: ParamDict, allow_ash_of_war: bool) -> dict[Affinity, AffinityProperties]:
    possible_maxima = [0, 12] if allow_ash_of_war else [0]
    indices, levels = find_offset_indices(row.index, armaments, possible_maxima, increment=100)
    affinities: list[Affinity] = [Affinity.from_id(round(l / 100)) for l in levels]
    return {a: _get_affinity_properties(armaments[i], effects, reinforces) for i, a in zip(indices, affinities)}

class ArmamentTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Armament,
    }

    main_param_retriever = ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS, id_min=1000000, id_max=49000000)

    predicates: list[RowPredicate] = [
        lambda row: row.index % 10000 == 0,
        lambda row: len(row.name) > 0,
    ]

    param_retrievers = {
        "effects": ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
        "reinforces": ParamDictRetriever("ReinforceParamWeapon", ItemIDFlag.NON_EQUIPABBLE),
    }

    msg_retrievers = {
        "names": MsgsRetriever("WeaponName"),
        "descriptions": MsgsRetriever("WeaponCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        effects = data.params["effects"]
        reinforces = data.params["reinforces"]

        upgrade_costs = _get_upgrade_costs(row, reinforces)
        upgrade_material = { # assuming nothing upgrades to +10 with regular stones
            0: ArmamentUpgradeMaterial.NONE,
            10: ArmamentUpgradeMaterial.SOMBER_SMITHING_STONE,
            25: ArmamentUpgradeMaterial.SMITHING_STONE,
        }[len(upgrade_costs)]

        weapon_effects = parse_weapon_effects(row) \
            + parse_effects(row, effects, *_RESIDENT_EFFECTS_FIELDS) \
            + parse_effects(row, effects, *_BEHAVIOR_EFFECTS_FIELDS, add_condition=AttackCondition.ON_HIT)

        allow_ash_of_war = AshOfWarMountType(row["gemMountType"]) == AshOfWarMountType.ALLOW_CHANGE

        return Armament(
            **cls.make_item(data, row, summary=False),
            **cls.make_contrib(data, row, "locations", "remarks"),
            behavior_variation_id=row["behaviorVariationId"].as_int,
            category=ArmamentCategory.from_row(row),
            weight=row["weight"].as_float,
            default_skill_id=row["swordArtsParamId"].as_int,
            allow_ash_of_war=allow_ash_of_war,
            is_buffable=row["isEnhance"].as_bool,
            is_l1_guard=row["enableGuard"].as_bool,
            upgrade_material=upgrade_material,
            upgrade_costs=upgrade_costs,
            attack_attributes=_get_attack_attributes(row),
            sp_consumption_rate=row["staminaConsumptionRate"].as_float,
            requirements=_get_requirements(row),
            effects=[Effect(**eff) for eff in weapon_effects],
            affinity=_get_affinities(row, data.main_param, effects, reinforces, allow_ash_of_war)
        )