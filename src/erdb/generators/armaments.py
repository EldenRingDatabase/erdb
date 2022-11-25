from erdb.typing.models.armament import Armament, AffinityProperties, Guard, CorrectionCalcID, Scaling
from erdb.typing.models.common import Damage, StatRequirements
from erdb.typing.models.effect import Effect, StatusEffects
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import Affinity, AttackCondition, ItemIDFlag, AshOfWarMountType, AttackAttribute, ArmamentUpgradeMaterial
from erdb.typing.categories import ArmamentCategory
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import find_offset_indices, update_optional
from erdb.effect_parser import parse_effects, parse_status_effects, parse_weapon_effects
from erdb.generators._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.generators._common import RowPredicate, TableSpecContext


_BEHAVIOR_EFFECTS_FIELDS: list[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]
_RESIDENT_EFFECTS_FIELDS: list[str] = ["residentSpEffectId", "residentSpEffectId1", "residentSpEffectId2"]

def _get_attack_attributes(row: ParamRow) -> list[AttackAttribute]:
    attributes = {AttackAttribute.from_id(row.get_int(field)) for field in ["atkAttribute", "atkAttribute2"]}
    return sorted(list(attributes))

def _get_upgrade_costs(row: ParamRow, reinforces: ParamDict) -> list[int]:
    reinforcement_id = row.get_int("reinforceTypeId")

    reinforcement = reinforces[str(reinforcement_id)]
    base_price = row.get_int("reinforcePrice")

    indices, _ = find_offset_indices(reinforcement.index, reinforces, possible_maxima=[0, 10, 25])
    next(indices) # ignore first index

    return [round(base_price * reinforces[str(i)].get_float("reinforcePriceRate")) for i in indices]

def _get_correction_calc_ids(row: ParamRow) -> CorrectionCalcID:
    return CorrectionCalcID(
        physical=row.get_int("correctType_Physics"),
        magic=row.get_int("correctType_Magic"),
        fire=row.get_int("correctType_Fire"),
        lightning=row.get_int("correctType_Thunder"),
        holy=row.get_int("correctType_Dark"),
        poison=row.get_int("correctType_Poison"),
        bleed=row.get_int("correctType_Blood"),
        sleep=row.get_int("correctType_Sleep"),
        madness=row.get_int("correctType_Madness")
    )

def _get_requirements(row: ParamRow) -> StatRequirements:
    requirements = {}
    requirements = update_optional(requirements, "strength", row.get_int("properStrength"), 0)
    requirements = update_optional(requirements, "dexterity", row.get_int("properAgility"), 0)
    requirements = update_optional(requirements, "intelligence", row.get_int("properMagic"), 0)
    requirements = update_optional(requirements, "faith", row.get_int("properFaith"), 0)
    requirements = update_optional(requirements, "arcane", row.get_int("properLuck"), 0)
    return StatRequirements(**requirements)

def _get_damages(row: ParamRow) -> Damage:
    damages = {}
    damages = update_optional(damages, "physical", row.get_int("attackBasePhysics"), 0)
    damages = update_optional(damages, "magic", row.get_int("attackBaseMagic"), 0)
    damages = update_optional(damages, "fire", row.get_int("attackBaseFire"), 0)
    damages = update_optional(damages, "lightning", row.get_int("attackBaseThunder"), 0)
    damages = update_optional(damages, "holy", row.get_int("attackBaseDark"), 0)
    damages = update_optional(damages, "stamina", row.get_int("attackBaseStamina"), 0)
    return Damage(**damages)

def _get_scalings(row: ParamRow) -> Scaling:
    scalings = {}
    scalings = update_optional(scalings, "strength", row.get_float("correctStrength") / 100.0, 0.0)
    scalings = update_optional(scalings, "dexterity", row.get_float("correctAgility") / 100.0, 0.0)
    scalings = update_optional(scalings, "intelligence", row.get_float("correctMagic") / 100.0, 0.0)
    scalings = update_optional(scalings, "faith", row.get_float("correctFaith") / 100.0, 0.0)
    scalings = update_optional(scalings, "arcane", row.get_float("correctLuck") / 100.0, 0.0)
    return Scaling(**scalings)

def _get_guards(row: ParamRow) -> Guard:
    guards = {}
    guards = update_optional(guards, "physical", row.get_float("physGuardCutRate"), 0.0)
    guards = update_optional(guards, "magic", row.get_float("magGuardCutRate"), 0.0)
    guards = update_optional(guards, "fire", row.get_float("fireGuardCutRate"), 0.0)
    guards = update_optional(guards, "lightning", row.get_float("thunGuardCutRate"), 0.0)
    guards = update_optional(guards, "holy", row.get_float("darkGuardCutRate"), 0.0)
    guards = update_optional(guards, "guard_boost", row.get_float("staminaGuardDef"), 0.0)
    return Guard(**guards)

def _get_resistances(row: ParamRow) -> StatusEffects:
    resistances = {}
    resistances = update_optional(resistances, "poison", row.get_int("poisonGuardResist"), 0)
    resistances = update_optional(resistances, "scarlet_rot", row.get_int("diseaseGuardResist"), 0)
    resistances = update_optional(resistances, "frostbite", row.get_int("freezeGuardResist"), 0)
    resistances = update_optional(resistances, "bleed", row.get_int("bloodGuardResist"), 0)
    resistances = update_optional(resistances, "sleep", row.get_int("sleepGuardResist"), 0)
    resistances = update_optional(resistances, "madness", row.get_int("madnessGuardResist"), 0)
    resistances = update_optional(resistances, "death_blight", row.get_int("curseGuardResist"), 0)
    return StatusEffects(**resistances)

def get_status_effect_overlay(row: ParamRow, effects: ParamDict, reinforces: ParamDict, reinforcement_id: int) -> list[StatusEffects]:
    if (reinforcement := reinforces.get(str(reinforcement_id + 1))) is None:
        return []

    effect_fields = ["spEffectId1", "spEffectId2", "spEffectId3"]
    effect_fields = [f for f in effect_fields if reinforcement.get_int(f) > 0]

    assert len(effect_fields) <= 1, "Up to one effect field can have offset added"

    if len(effect_fields) == 0:
        return []

    assert str(reinforcement_id + 25) in reinforces, "Only +25 reinforcements upgrade status effects"

    weapfield = {
        "spEffectId1": "spEffectBehaviorId0",
        "spEffectId2": "spEffectBehaviorId1",
        "spEffectId3": "spEffectBehaviorId2",
    }[effect_fields[0]]

    effect_ids = [row.get_int(weapfield) + offset for offset in range(0, 26)]
    return [parse_status_effects([str(i)], effects) for i in effect_ids]

def _get_affinity_properties(row: ParamRow, effects: ParamDict, reinforces: ParamDict) -> AffinityProperties:
    reinforcement_id = row.get_int("reinforceTypeId")
    return AffinityProperties(
        full_hex_id=row.index_hex,
        id=row.index,
        reinforcement_id=reinforcement_id,
        correction_attack_id=row.get_int("attackElementCorrectId"),
        correction_calc_id=_get_correction_calc_ids(row),
        damage=_get_damages(row),
        scaling=_get_scalings(row),
        guard=_get_guards(row),
        resistance=_get_resistances(row),
        status_effects=parse_status_effects([row.get(f) for f in _BEHAVIOR_EFFECTS_FIELDS], effects),
        status_effect_overlay=get_status_effect_overlay(row, effects, reinforces, reinforcement_id),
    )

def _get_affinities(row: ParamRow, armaments: ParamDict, effects: ParamDict, reinforces: ParamDict, allow_ash_of_war: bool) -> dict[Affinity, AffinityProperties]:
    possible_maxima = [0, 12] if allow_ash_of_war else [0]
    indices, levels = find_offset_indices(row.index, armaments, possible_maxima, increment=100)
    affinities: list[Affinity] = [Affinity.from_id(round(l / 100)) for l in levels]
    return {a: _get_affinity_properties(armaments[str(i)], effects, reinforces) for i, a in zip(indices, affinities)}

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

        allow_ash_of_war = AshOfWarMountType(row.get("gemMountType")) == AshOfWarMountType.ALLOW_CHANGE

        return Armament(
            **cls.make_item(data, row, summary=False),
            **cls.make_contrib(data, row, "locations", "remarks"),
            behavior_variation_id=row.get_int("behaviorVariationId"),
            category=ArmamentCategory.from_row(row),
            weight=row.get_float("weight"),
            default_skill_id=row.get_int("swordArtsParamId"),
            allow_ash_of_war=allow_ash_of_war,
            is_buffable=row.get_bool("isEnhance"),
            is_l1_guard=row.get_bool("enableGuard"),
            upgrade_material=upgrade_material,
            upgrade_costs=upgrade_costs,
            attack_attributes=_get_attack_attributes(row),
            sp_consumption_rate=row.get_float("staminaConsumptionRate"),
            requirements=_get_requirements(row),
            effects=[Effect(**eff) for eff in weapon_effects],
            affinity=_get_affinities(row, data.main_param, effects, reinforces, allow_ash_of_war)
        )