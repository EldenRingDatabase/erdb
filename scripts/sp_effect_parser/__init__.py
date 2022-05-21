import sp_effect_parser.attribute_fields as attrib_fields
import sp_effect_parser.effect_parsers as parse
import sp_effect_parser.hardcoded_effects as hardcoded_effects
from sp_effect_parser.effect_aggregator import aggregate_effects
from typing import List, Dict, Optional
from er_params import ParamRow, ParamDict
from er_params.enums import SpEffectType
from sp_effect_parser.effect_typing import SchemaEffect

_REFERENCE_EFFECT_PARAMS = ["cycleOccurrenceSpEffectId", "applyIdOnGetSoul"]

def get_effects(sp_effect: ParamRow, triggeree: Optional[ParamRow]=None) -> List[SchemaEffect]:
    effects = hardcoded_effects.get(sp_effect.index)

    for field, attrib_field in attrib_fields.get().items():
        if sp_effect.get(field) == str(attrib_field.default_value):
            continue

        effect = SchemaEffect.from_attribute_field(sp_effect.get_float(field), attrib_field)
        effect.conditions = parse.conditions(sp_effect, triggeree)
        effect.tick_interval = parse.interval(sp_effect)
        effect.value_pvp = parse.value_pvp(sp_effect, field, attrib_fields.get())

        effects.append(effect)

    return effects

def get_effects_nested(sp_effect: ParamRow, sp_effects: ParamDict) -> List[SchemaEffect]:
    effects = get_effects(sp_effect)
    sp_effect_type = SpEffectType(sp_effect.get("stateInfo"))

    for ref_id in (sp_effect.get(ref_field) for ref_field in _REFERENCE_EFFECT_PARAMS):
        if ref_sp_effect := sp_effects.get(ref_id):
            effects += get_effects(ref_sp_effect, sp_effect)

    if ref_offset := sp_effect_type.get_reference_offset():
        ref_sp_effect = sp_effects.get(str(sp_effect.index + ref_offset))
        effects += get_effects(ref_sp_effect, sp_effect)

    return effects

def parse_effects(row: ParamRow, sp_effects: ParamDict, *effect_referencing_fields: str) -> List[Dict]:
    effects = []

    for effect_id in (row.get(ref_field) for ref_field in effect_referencing_fields):
        if effect_id in sp_effects:
            effects += get_effects_nested(sp_effects[effect_id], sp_effects)

    return [e.to_dict() for e in aggregate_effects(effects)]