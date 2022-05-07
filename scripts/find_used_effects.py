import er_params
from er_params import sp_effect
from er_params.enums import ItemIDFlag
from typing import List

def get_base_effect_id(effect_id: str):
    assert len(effect_id) > 2, "Invalid effect_id or 0"
    return effect_id[:-2] + "00"

def get_effect_ids(talismans: er_params.ParamDict) -> List[str]:
    # TODO: Take resident (passive) sp_effects under consideration
    return list(set([row.get("refId") for row in talismans.values()]))

def get_changing_fields(effect_ids: List[str], effects: er_params.ParamDict) -> List[str]:
    changing_fields = set()
    null_effect = effects["2"] # IDs "0" and "1" seem to have some properties filled in

    for field in null_effect.keys:
        if field == "iconId":
            continue

        null_value = null_effect.get(field)
        items = []

        for i in effect_ids:
            if null_value != effects[i].get(field):
                items.append(effects[i].name)

        if len(items) > 0 and len(items) != len(effect_ids):
            name = sp_effect.details[field]["DisplayName"]
            changing_fields.add(f">> {name}: {', '.join(items)}")

    return list(changing_fields)

def main():
    talismans = er_params.load("EquipParamAccessory", "1.04.1", ItemIDFlag.ACCESSORIES)
    effects = er_params.load("SpEffectParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE)
    effect_ids = get_effect_ids(talismans)
    changing_fields = get_changing_fields(effect_ids, effects)

    for f in sorted(changing_fields):
        print(f)

if __name__ == "__main__":
    main()