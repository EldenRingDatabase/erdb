import erdb.effect_parser.attribute_fields as attrib_fields
import erdb.effect_parser.parsers as parse
import erdb.effect_parser.hardcoded as hardcoded_effects
from erdb.effect_parser.aggregator import aggregate_effects
from erdb.typing.models.effect import StatusEffects
from erdb.typing.params import ParamRow, ParamDict
from erdb.typing.enums import SpEffectType, AttackCondition
from erdb.typing.effects import SchemaEffect


_REFERENCE_EFFECT_PARAMS: list[str] = ["cycleOccurrenceSpEffectId", "applyIdOnGetSoul"]

_SP_EFFECT_TO_FIELD: dict[SpEffectType, str] = {
    SpEffectType.HEMORRHAGE: "bloodAttackPower",
    SpEffectType.FROSTBITE: "freezeAttackPower",
    SpEffectType.POISON: "poizonAttackPower",
    SpEffectType.SCARLET_ROT: "diseaseAttackPower",
    SpEffectType.SLEEP: "sleepAttackPower",
    SpEffectType.MADNESS: "madnessAttackPower",
    SpEffectType.BLIGHT: "curseAttackPower",
}

_SP_EFFECT_TO_STR: dict[SpEffectType, str] = {
    SpEffectType.HEMORRHAGE: "bleed",
    SpEffectType.FROSTBITE: "frostbite",
    SpEffectType.POISON: "poison",
    SpEffectType.SCARLET_ROT: "scarlet_rot",
    SpEffectType.SLEEP: "sleep",
    SpEffectType.MADNESS: "madness",
    SpEffectType.BLIGHT: "death_blight",
}

def get_effects(sp_effect: ParamRow, sp_effect_type: SpEffectType, triggeree: ParamRow | None = None, init_conditions: list[str] | None = None) -> list[SchemaEffect]:
    effects = hardcoded_effects.get(sp_effect.index, sp_effect_type)

    for field, attrib_field in attrib_fields.get().items():
        if sp_effect[field] == str(attrib_field.default_value):
            continue

        effect = SchemaEffect.from_attribute_field(sp_effect[field].as_float, attrib_field)

        effect.conditions = init_conditions
        if conds := parse.conditions(sp_effect, triggeree):
            effect.conditions = conds if effect.conditions is None else effect.conditions + conds

        effect.tick_interval = parse.interval(sp_effect)
        effect.value_pvp = parse.value_pvp(sp_effect, field, attrib_fields.get())

        effects.append(effect)

    return effects

def get_effects_nested(sp_effect: ParamRow, sp_effects: ParamDict, add_condition: AttackCondition | None) -> list[SchemaEffect]:
    sp_effect_type = SpEffectType(sp_effect["stateInfo"])
    effects = get_effects(sp_effect, sp_effect_type, init_conditions=[str(add_condition)] if add_condition else None)

    for ref_id in (sp_effect[ref_field].as_int for ref_field in _REFERENCE_EFFECT_PARAMS):
        if ref_sp_effect := sp_effects.get(ref_id):
            if ref_sp_effect.index > 0:
                effects += get_effects(ref_sp_effect, sp_effect_type, sp_effect)

    for condition_offset in hardcoded_effects.get_conditions(sp_effect.index):
        ref_sp_effect = sp_effects[sp_effect.index + condition_offset.offset]
        init_conditions = None if condition_offset.condition is None else [str(condition_offset.condition)]
        effects += get_effects(ref_sp_effect, sp_effect_type, sp_effect, init_conditions)

    return effects

def get_status_effect(sp_effect: ParamRow) -> tuple[str, int]:
    # NOTE: not identifying effects by values, relying on `stateInfo` to be correct at all times
    etype = SpEffectType(sp_effect["stateInfo"])
    return _SP_EFFECT_TO_STR[etype], sp_effect[_SP_EFFECT_TO_FIELD[etype]].as_int

def parse_effects(row: ParamRow, sp_effects: ParamDict, *effect_referencing_fields: str, add_condition: AttackCondition | None = None) -> list[dict]:
    effects: list[SchemaEffect] = []

    for effect_id in (row[ref_field].as_int for ref_field in effect_referencing_fields):
        if effect_id in hardcoded_effects.get_status_effect_ranges():
            continue

        if effect_id in sp_effects:
            effects += get_effects_nested(sp_effects[effect_id], sp_effects, add_condition)

    return [e.to_dict() for e in aggregate_effects(effects)]

def parse_status_effects(effect_ids: list[int], sp_effects: ParamDict) -> StatusEffects:
    # Getting 0th effect if value no found, bug with Antspur Rapier -- get anything to return a 0 status effect
    effects = [sp_effects.get(i, sp_effects[0]) for i in effect_ids if i != -1]
    status_effects = hardcoded_effects.get_status_effect_ranges()
    return StatusEffects(**dict([get_status_effect(e) for e in effects if e.index in status_effects]))

def parse_weapon_effects(weapon: ParamRow) -> list[dict]:
    effects: list[SchemaEffect] = []

    for field, attrib_field in attrib_fields.get(weapon=True).items():
        if weapon[field] != str(attrib_field.default_value):
            effects.append(SchemaEffect.from_attribute_field(weapon[field].as_float, attrib_field))

    return [e.to_dict() for e in effects]