import er_params
from er_params import ParamDict
from er_params.enums import ItemIDFlag
from typing import List, Dict

def get_values(effects: ParamDict, field: str, limit: int=10) -> Dict[str, List[str]]:
    values = {}

    for effect in effects.values():
        val = effect.get(field)
        if val not in values:
            values[val] = []

        case = str(effect.index) if len(effect.name) == 0 else effect.name

        if len(values[val]) < limit:
            values[val].append(case)

        elif len(values[val]) == limit:
            values[val].append("(...)")

    return values

def main():
    effects = er_params.load("SpEffectParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE)

    # short param overview:
    # conditionHp      -- trigger when HP below %
    # conditionHpRate  -- trigger when HP above %
    # invocationConditionsStateChange1 -- seemingly the only differentiating field for Concealing Veil
    # invocationConditionsStateChange1/2/3
    # toughnessDamageCutRate -- kinda like inverted poise
    # miracleConsumptionRate -- FP consumption rate for incantations
    # shamanConsumptionRate  -- FP consumption rate for pyormancies (?)
    # magicConsumptionRate   -- FP consumption rate for sorceries
    # stateInfo              -- a lot of unique effects seem to use this and this only
    # guardStaminaCutRate    -- Greatshield Talisman doesn't seem to use this

    values = get_values(effects, "guardStaminaCutRate", limit=30)

    for value in sorted(values.keys(), key=float):
        cases = values[value]
        value = f"{value}".ljust(8)
        print(f">> {value}:", ', '.join(cases))

if __name__ == "__main__":
    main()