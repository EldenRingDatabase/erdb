import math
from erdb.typing.params import ParamRow
from erdb.typing.enums import SpEffectType, AttackType
from erdb.typing.effects import AttributeField, EffectModel


_TRIGGER_FIELDS = [
    "stateInfo", "invocationConditionsStateChange1",
    "invocationConditionsStateChange2", "invocationConditionsStateChange3"
]

_CONDITION_FIELDS = [
    "magicSubCategoryChange1", "magicSubCategoryChange2", "magicSubCategoryChange3"
]

_PVE_TO_PVP = {
    "defEnemyDmgCorrectRate_Physics": "defPlayerDmgCorrectRate_Physics",
    "defEnemyDmgCorrectRate_Magic":   "defPlayerDmgCorrectRate_Magic",
    "defEnemyDmgCorrectRate_Fire":    "defPlayerDmgCorrectRate_Fire",
    "defEnemyDmgCorrectRate_Thunder": "defPlayerDmgCorrectRate_Thunder",
    "defEnemyDmgCorrectRate_Dark":    "defPlayerDmgCorrectRate_Dark",
    "atkEnemyDmgCorrectRate_Physics": "atkPlayerDmgCorrectRate_Physics",
    "atkEnemyDmgCorrectRate_Magic":   "atkPlayerDmgCorrectRate_Magic",
    "atkEnemyDmgCorrectRate_Fire":    "atkPlayerDmgCorrectRate_Fire",
    "atkEnemyDmgCorrectRate_Thunder": "atkPlayerDmgCorrectRate_Thunder",
    "atkEnemyDmgCorrectRate_Dark":    "atkPlayerDmgCorrectRate_Dark",
}

def _floor_decimal_2(value: float) -> float:
    value = round(value, 6) # do not floor cases like 1.89999999999
    return math.floor(value * 100) / 100.0

def conditions(sp_effect: ParamRow, triggeree: ParamRow | None = None) -> list[str] | None:
    conds = set()

    def _append_triggers(source: ParamRow):
        for trigger in _TRIGGER_FIELDS:
            effect_type = SpEffectType(source[trigger])

            if not effect_type.is_passive():
                conds.add(str(effect_type))

            if effect_type == SpEffectType.SPELL_POWER_BOOST:
                boostSorcery = ("magParamChange", "Affects Sorceries")
                boostIncantation = ("miracleParamChange", "Affects Incantations")
                for field, cond in [boostSorcery, boostIncantation]:
                    if sp_effect[field].as_bool:
                        conds.add(cond)

    def _append_conditions(source: ParamRow):
        for cond in _CONDITION_FIELDS:
            attack_type_str = source[cond]
            if (cond := AttackType(attack_type_str)) != AttackType.NONE:
                conds.add(str(cond))

    for field, direction in [("conditionHp", "below"), ("conditionHpRate", "above")]:
        if cond := sp_effect[field].get_int():
            conds.add(f"HP {direction} {cond}%")

    _append_triggers(sp_effect)
    _append_conditions(sp_effect)

    if triggeree:
        _append_triggers(triggeree)
        _append_conditions(triggeree)

    return None if len(conds) == 0 else sorted(list(conds))

def interval(sp_effect: ParamRow) -> float | None:
    interv = sp_effect["motionInterval"]
    return None if interv == "0" else float(interv)

def value_pvp(sp_effect: ParamRow, field_pve: str, attrib_fields: dict[str, AttributeField]) -> float | None:
    if not (field_pvp := _PVE_TO_PVP.get(field_pve, None)):
        return None

    attrib_field = attrib_fields[field_pve]
    val = sp_effect[field_pvp].as_float

    return attrib_field.parser(val, attrib_field.effect_model)

def generic(value: float, model: EffectModel) -> float:
    return value

def generic_inverse(value: float, model: EffectModel) -> float:
    """
    Some sp_effect fields are hardcoded to be subtractable/divisible. Because of this,
    their values are negative in the params. Specifying this parser will reverse
    these values on per effect basis to have them make more sense.

    Examples:
    - Blessed Dew Talisman's `changeHpPoint` is set to -2 when it should heal
    - Malenia - Scarlet Rot's `changeHpPoint` is set to 26 when it should damage
    """
    return -value if model == EffectModel.ADDITIVE else _floor_decimal_2(2 - value)

def generic_inverse_percentage(value: float, model: EffectModel) -> float:
    """
    Flat percentage value, but also inverse. Turn -10 into 1.1 (ex. Assassin's Crimson Dagger).
    """
    return 1 + (-value / 100.0)

def poise(value: float, model: EffectModel) -> float:
    """
    Poise value is given as a "poise damage absorption" value, eg. `0.75`.
    The actual poise increase that is shown in game is the inverse of that:
        1 / .75 -> +33% poise.
    """
    return math.floor(1 / value * 100) / 100.0

def item_discovery(value: float, model: EffectModel) -> float:
    return value * 100