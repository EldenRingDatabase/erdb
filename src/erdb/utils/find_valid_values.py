from collections import defaultdict

from erdb.loaders.params import load as load_params
from erdb.typing.params import ParamDict
from erdb.typing.enums import ItemIDFlag
from erdb.typing.game_version import GameVersion


def _get_values(effects: ParamDict, field: str, limit: int = 10) -> dict[str, list[str]]:
    values = defaultdict(list)

    for effect in effects.values():
        val = effect[field]
        case = str(effect.index) if len(effect.name) == 0 else effect.name

        if len(values[val]) < limit:
            values[val].append(case)

        elif len(values[val]) == limit:
            values[val].append("(...)")

    return values

def find_valid_values(param_name: str, version: str, field: str, limit: int = 8):
    """
    Interesting param.fields overview:
    * SpEffectParam:conditionHp                      -- trigger when HP below %
    * SpEffectParam:conditionHpRate                  -- trigger when HP above %
    * SpEffectParam:invocationConditionsStateChange1 -- seemingly the only differentiating field for Concealing Veil
    * SpEffectParam:invocationConditionsStateChange1/2/3
    * SpEffectParam:toughnessDamageCutRate           -- kinda like inverted poise
    * SpEffectParam:miracleConsumptionRate           -- FP consumption rate for incantations
    * SpEffectParam:shamanConsumptionRate            -- FP consumption rate for pyormancies (?)
    * SpEffectParam:magicConsumptionRate             -- FP consumption rate for sorceries
    * SpEffectParam:stateInfo                        -- a lot of unique effects seem to use this and this only
    * SpEffectParam:guardStaminaCutRate              -- Greatshield Talisman doesn't seem to use this
    * SpEffectParam:magicSubCategoryChange1/2/3      -- seem to specify conditions exclusively
    """

    params = load_params(param_name, GameVersion.from_string(version), ItemIDFlag.NON_EQUIPABBLE)
    values = _get_values(params, field, limit=8 if limit < 0 else limit)

    for value in sorted(values.keys(), key=float):
        cases = values[value]
        value = f"{value}".ljust(8)
        print(f">> {value}:", ', '.join(cases))