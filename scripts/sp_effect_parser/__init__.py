import scripts.sp_effect_parser.attribute_fields as attrib_fields
import scripts.sp_effect_parser.effect_parsers as parse
import scripts.sp_effect_parser.hardcoded_effects as hardcoded_effects
from scripts.sp_effect_parser.effect_aggregator import aggregate_effects
from scripts.er_params import ParamRow, ParamDict
from scripts.er_params.enums import SpEffectType, AttackCondition
from scripts.sp_effect_parser.effect_typing import SchemaEffect
from typing import List, Dict, Optional, Tuple

_REFERENCE_EFFECT_PARAMS: List[str] = ["cycleOccurrenceSpEffectId", "applyIdOnGetSoul"]

_STATUS_EFFECT_FIELDS: Dict[SpEffectType, str] = {
    SpEffectType.HEMORRHAGE: "bloodAttackPower",
    SpEffectType.FROSTBITE: "freezeAttackPower",
    SpEffectType.POISON: "poizonAttackPower",
    SpEffectType.SCARLET_ROT: "diseaseAttackPower",
    SpEffectType.SLEEP: "sleepAttackPower",
    SpEffectType.MADNESS: "madnessAttackPower",
    SpEffectType.BLIGHT: "curseAttackPower",
}

_STATUS_EFFECT_PROPERTY_NAMES: Dict[SpEffectType, str] = {
    SpEffectType.HEMORRHAGE: "bleed",
    SpEffectType.FROSTBITE: "frostbite",
    SpEffectType.POISON: "poison",
    SpEffectType.SCARLET_ROT: "scarlet_rot",
    SpEffectType.SLEEP: "sleep",
    SpEffectType.MADNESS: "madness",
    SpEffectType.BLIGHT: "death_blight",
}

def get_effects(sp_effect: ParamRow, sp_effect_type: SpEffectType, triggeree: Optional[ParamRow]=None, init_conditions: Optional[List[str]]=None) -> List[SchemaEffect]:
    effects = hardcoded_effects.get(sp_effect.index, sp_effect_type)

    for field, attrib_field in attrib_fields.get().items():
        if sp_effect.get(field) == str(attrib_field.default_value):
            continue

        effect = SchemaEffect.from_attribute_field(sp_effect.get_float(field), attrib_field)

        effect.conditions = init_conditions
        if conds := parse.conditions(sp_effect, triggeree):
            effect.conditions = conds if effect.conditions is None else effect.conditions + conds

        effect.tick_interval = parse.interval(sp_effect)
        effect.value_pvp = parse.value_pvp(sp_effect, field, attrib_fields.get())

        effects.append(effect)

    return effects

def get_effects_nested(sp_effect: ParamRow, sp_effects: ParamDict, add_condition: Optional[AttackCondition]) -> List[SchemaEffect]:
    sp_effect_type = SpEffectType(sp_effect.get("stateInfo"))
    effects = get_effects(sp_effect, sp_effect_type, init_conditions=[str(add_condition)] if add_condition else None)

    for ref_id in (sp_effect.get(ref_field) for ref_field in _REFERENCE_EFFECT_PARAMS):
        if ref_sp_effect := sp_effects.get(ref_id):
            if ref_sp_effect.index > 0:
                effects += get_effects(ref_sp_effect, sp_effect_type, sp_effect)

    for condition_offset in hardcoded_effects.get_conditions(sp_effect.index):
        ref_sp_effect = sp_effects.get(str(sp_effect.index + condition_offset.offset))
        init_conditions =  None if condition_offset.condition is None else [str(condition_offset.condition)]
        effects += get_effects(ref_sp_effect, sp_effect_type, sp_effect, init_conditions)

    return effects

def get_status_effect(sp_effect: ParamRow) -> Tuple[str, int]:
    # NOTE: not identifying effects by values, relying on `stateInfo` to be correct at all times
    etype = SpEffectType(sp_effect.get("stateInfo"))
    return _STATUS_EFFECT_PROPERTY_NAMES[etype], sp_effect.get_int(_STATUS_EFFECT_FIELDS[etype])

def parse_effects(row: ParamRow, sp_effects: ParamDict, *effect_referencing_fields: str, add_condition: Optional[AttackCondition]=None) -> List[Dict]:
    effects: List[SchemaEffect] = []

    for effect_id in (row.get(ref_field) for ref_field in effect_referencing_fields):
        if effect_id in hardcoded_effects.get_status_effect_ranges():
            continue

        if effect_id in sp_effects:
            effects += get_effects_nested(sp_effects[effect_id], sp_effects, add_condition)

    return [e.to_dict() for e in aggregate_effects(effects)]

def parse_status_effects(effect_ids: List[str], sp_effects: ParamDict) -> Dict[str, int]:
    # Getting 0th effect if value no found, bug with Antspur Rapier -- get anything to return a 0 status effect
    effects = [sp_effects.get(i, sp_effects["0"]) for i in effect_ids if i != "-1"]
    status_effects = hardcoded_effects.get_status_effect_ranges()
    return dict([get_status_effect(e) for e in effects if e.index in status_effects])

def parse_weapon_effects(weapon: ParamRow) -> List[Dict]:
    effects: List[SchemaEffect] = []

    for field, attrib_field in attrib_fields.get(weapon=True).items():
        if weapon.get(field) != str(attrib_field.default_value):
            effects.append(SchemaEffect.from_attribute_field(weapon.get_float(field), attrib_field))

    return [e.to_dict() for e in effects]