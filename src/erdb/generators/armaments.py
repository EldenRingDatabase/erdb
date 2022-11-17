from typing import Dict, List, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import Affinity, AttackCondition, ItemIDFlag, WeaponClass, AshOfWarMountType, AttackAttribute, ReinforcementType
from erdb.utils.common import find_offset_indices, update_optional, strip_invalid_name
from erdb.effect_parser import parse_effects, parse_status_effects, parse_weapon_effects
from erdb.generators._base import GeneratorDataBase


_BEHAVIOR_EFFECTS_FIELDS: List[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]
_RESIDENT_EFFECTS_FIELDS: List[str] = ["residentSpEffectId", "residentSpEffectId1", "residentSpEffectId2"]

def _get_attack_attributes(row: ParamRow) -> List[AttackAttribute]:
    attributes = {AttackAttribute(row.get(field)) for field in ["atkAttribute", "atkAttribute2"]}
    return sorted(list(attributes))

def _get_upgrade_costs(row: ParamRow, reinforces: ParamDict) -> List[int]:
    reinforcement_type = ReinforcementType(row.get("reinforceTypeId"))
    if reinforcement_type == ReinforcementType.NO_REINFORCEMENT:
        return []

    reinforcement = reinforces[reinforcement_type.value]
    base_price = row.get_int("reinforcePrice")

    indices, _ = find_offset_indices(reinforcement.index, reinforces, possible_maxima=[10, 25])
    next(indices) # ignore first index

    return [round(base_price * reinforces[str(i)].get_float("reinforcePriceRate")) for i in indices]

def _get_correction_calc_ids(row: ParamRow) -> Dict[str, str]:
    return {
        "physical": row.get("correctType_Physics"),
        "magic": row.get("correctType_Magic"),
        "fire": row.get("correctType_Fire"),
        "lightning": row.get("correctType_Thunder"),
        "holy": row.get("correctType_Dark"),
        "poison": row.get("correctType_Poison"),
        "bleed": row.get("correctType_Blood"),
        "sleep": row.get("correctType_Sleep"),
        "madness": row.get("correctType_Madness")
    }

def _get_requirements(row: ParamRow) -> Dict[str, int]:
    requirements = {}
    requirements = update_optional(requirements, "strength", row.get_int("properStrength"), 0)
    requirements = update_optional(requirements, "dexterity", row.get_int("properAgility"), 0)
    requirements = update_optional(requirements, "intelligence", row.get_int("properMagic"), 0)
    requirements = update_optional(requirements, "faith", row.get_int("properFaith"), 0)
    requirements = update_optional(requirements, "arcane", row.get_int("properLuck"), 0)
    return requirements

def _get_damages(row: ParamRow) -> Dict[str, int]:
    damages = {}
    damages = update_optional(damages, "physical", row.get_int("attackBasePhysics"), 0)
    damages = update_optional(damages, "magic", row.get_int("attackBaseMagic"), 0)
    damages = update_optional(damages, "fire", row.get_int("attackBaseFire"), 0)
    damages = update_optional(damages, "lightning", row.get_int("attackBaseThunder"), 0)
    damages = update_optional(damages, "holy", row.get_int("attackBaseDark"), 0)
    damages = update_optional(damages, "stamina", row.get_int("attackBaseStamina"), 0)
    return damages

def _get_scalings(row: ParamRow) -> Dict[str, float]:
    scalings = {}
    scalings = update_optional(scalings, "strength", row.get_float("correctStrength") / 100.0, 0.0)
    scalings = update_optional(scalings, "dexterity", row.get_float("correctAgility") / 100.0, 0.0)
    scalings = update_optional(scalings, "intelligence", row.get_float("correctMagic") / 100.0, 0.0)
    scalings = update_optional(scalings, "faith", row.get_float("correctFaith") / 100.0, 0.0)
    scalings = update_optional(scalings, "arcane", row.get_float("correctLuck") / 100.0, 0.0)
    return scalings

def _get_guards(row: ParamRow) -> Dict[str, float]:
    guards = {}
    guards = update_optional(guards, "physical", row.get_float("physGuardCutRate"), 0.0)
    guards = update_optional(guards, "magic", row.get_float("magGuardCutRate"), 0.0)
    guards = update_optional(guards, "fire", row.get_float("fireGuardCutRate"), 0.0)
    guards = update_optional(guards, "lightning", row.get_float("thunGuardCutRate"), 0.0)
    guards = update_optional(guards, "holy", row.get_float("darkGuardCutRate"), 0.0)
    guards = update_optional(guards, "guard_boost", row.get_float("staminaGuardDef"), 0.0)
    return guards

def _get_resistances(row: ParamRow) -> Dict[str, int]:
    resistances = {}
    resistances = update_optional(resistances, "poison", row.get_int("poisonGuardResist"), 0)
    resistances = update_optional(resistances, "scarlet_rot", row.get_int("diseaseGuardResist"), 0)
    resistances = update_optional(resistances, "frostbite", row.get_int("freezeGuardResist"), 0)
    resistances = update_optional(resistances, "bleed", row.get_int("bloodGuardResist"), 0)
    resistances = update_optional(resistances, "sleep", row.get_int("sleepGuardResist"), 0)
    resistances = update_optional(resistances, "madness", row.get_int("madnessGuardResist"), 0)
    resistances = update_optional(resistances, "death_blight", row.get_int("curseGuardResist"), 0)
    return resistances

def get_status_effect_overlay(row: ParamRow, effects: ParamDict, reinforces: ParamDict, reinforcement_type: ReinforcementType) -> Dict[str, List[int]]:
    if reinforcement_type == ReinforcementType.NO_REINFORCEMENT:
        return {}

    effect_fields = ["spEffectId1", "spEffectId2", "spEffectId3"]
    reinforcement = reinforces[str(int(reinforcement_type.value) + 1)]
    effect_fields = [f for f in effect_fields if reinforcement.get_int(f) > 0]

    assert len(effect_fields) <= 1, "Up to one effect field can have offset added"

    if len(effect_fields) == 0:
        return {}

    assert str(int(reinforcement_type.value) + 25) in reinforces, "Only +25 reinforcements upgrade status effects"

    weapfield = {
        "spEffectId1": "spEffectBehaviorId0",
        "spEffectId2": "spEffectBehaviorId1",
        "spEffectId3": "spEffectBehaviorId2",
    }[effect_fields[0]]

    effect_ids = [row.get_int(weapfield) + offset for offset in range(0, 26)]
    status_effects = [parse_status_effects([str(i)], effects) for i in effect_ids]

    name = next(iter(status_effects[0]))
    return {name: [e.get(name, 0) for e in status_effects]}

def _get_affinity_properties(row: ParamRow, effects: ParamDict, reinforces: ParamDict) -> Dict:
    reinforcement_type = ReinforcementType(row.get("reinforceTypeId"))
    return {
        "full_hex_id": row.index_hex,
        "id": row.index,
        "reinforcement_type": str(reinforcement_type),
        "correction_attack_id": row.get("attackElementCorrectId"),
        "correction_calc_id": _get_correction_calc_ids(row),
        "damage": _get_damages(row),
        "scaling": _get_scalings(row),
        "guard": _get_guards(row),
        "resistance": _get_resistances(row),
        "status_effects": parse_status_effects([row.get(f) for f in _BEHAVIOR_EFFECTS_FIELDS], effects),
        "status_effect_overlay": get_status_effect_overlay(row, effects, reinforces, reinforcement_type),
    }

def _get_affinities(row: ParamRow, armaments: ParamDict, effects: ParamDict, reinforces: ParamDict, allow_ash_of_war: bool) -> Dict:
    possible_maxima = [0, 12] if allow_ash_of_war else [0]
    indices, levels = find_offset_indices(row.index, armaments, possible_maxima, increment=100)
    affinities = [Affinity(str(round(l / 100))) for l in levels]
    return {str(a): _get_affinity_properties(armaments[str(i)], effects, reinforces) for i, a in zip(indices, affinities)}

class ArmamentGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "armaments.json"

    @staticmethod # override
    def schema_file() -> str:
        return "armaments.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Armaments"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS, id_min=1000000, id_max=49000000)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
        "reinforces": Base.ParamDictRetriever("ReinforceParamWeapon", ItemIDFlag.NON_EQUIPABBLE),
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("WeaponName"),
        "descriptions": Base.MsgsRetriever("WeaponCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = schema.load_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "armaments/definitions/Armament/properties")
        store.update(schema.load_properties("effect")[1])
        store.update(schema.load_enums("armament-names", "armament-class-names", "status-effect-names", "affinity-names", "reinforcement-names"))
        store.update(schema.load_enums("attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
        return properties, store

    def main_param_iterator(self, armaments: ParamDict):
        for row in armaments.values():
            if row.index % 10000 == 0 and len(row.name) > 0:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        effects = self.params["effects"]
        reinforces = self.params["reinforces"]

        upgrade_costs = _get_upgrade_costs(row, reinforces)
        upgrade_material = { # assuming nothing upgrades to +10 with regular stones
            0: "None",
            10: "Somber Smithing Stone",
            25: "Smithing Stone",
        }[len(upgrade_costs)]

        weapon_effects = parse_weapon_effects(row) \
            + parse_effects(row, effects, *_RESIDENT_EFFECTS_FIELDS) \
            + parse_effects(row, effects, *_BEHAVIOR_EFFECTS_FIELDS, add_condition=AttackCondition.ON_HIT)

        allow_ash_of_war = AshOfWarMountType(row.get("gemMountType")) == AshOfWarMountType.ALLOW_CHANGE

        return self.get_fields_item(row, summary=False) | self.get_fields_user_data(row, "locations", "remarks") | {
            "behavior_variation_id": row.get_int("behaviorVariationId"),
            "class": str(WeaponClass.from_id(row.get("wepType"))),
            "weight": row.get_float("weight"),
            "default_skill_id": row.get_int("swordArtsParamId"),
            "allow_ash_of_war": allow_ash_of_war,
            "is_buffable": row.get_bool("isEnhance"),
            "is_l1_guard": row.get_bool("enableGuard"),
            "upgrade_material": upgrade_material,
            "upgrade_costs": upgrade_costs,
            "attack_attributes": [*map(str, _get_attack_attributes(row))],
            "sp_consumption_rate": row.get_float("staminaConsumptionRate"),
            "requirement": _get_requirements(row),
            "effects": weapon_effects,
            "affinity": _get_affinities(row, self.main_param, effects, reinforces, allow_ash_of_war)
        }