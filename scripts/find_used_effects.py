import er_params
from er_params import sp_effect
from er_params.enums import ItemIDFlag
from typing import Dict, List, Set

_IGNORED_FIELDS = [
    "Row ID", "Row Name", "iconId", "lookAtTargetPosOffset", "targetPriority",
    "effectTargetSelf", "effectTargetFriend", "effectTargetEnemy", "effectTargetPlayer",
    "effectTargetAI", "effectTargetLive", "effectTargetGhost", "effectTargetAttacker",
    "vfxId", "vfxId1", "vfxId2", "vfxId3", "vfxId4", "vfxId5", "vfxId6", "vfxId7"
]

def get_effect_ids(rows: er_params.ParamDict, fields: List[str]) -> Dict[str, Set[str]]:
    ids = {}

    for row in rows.values():
        for field in fields:
            i = row.get(field)
            if i == "-1":
                continue

            if i not in ids:
                ids[i] = set()

            ids[i].add(row.name)

    return ids

def get_changing_fields(effect_ids: Dict[str, Set[str]], effects: er_params.ParamDict) -> List[str]:
    changing_fields = set()
    null_effect = effects["2"] # IDs "0" and "1" seem to have some properties filled in

    for field in null_effect.keys:
        if field in _IGNORED_FIELDS:
            continue

        null_value = null_effect.get(field)
        items = []

        for i, item_names in effect_ids.items():
            if null_value != effects[i].get(field):
                items += item_names

        if len(items) > 0 and len(items) != len(effect_ids):
            name = sp_effect.details[field]["DisplayName"]
            field_padded = f"{name} ({field})".ljust(64)
            changing_fields.add(f">> {field_padded}: {', '.join(items)}")

    return list(changing_fields)

def main():
    talismans = er_params.load("EquipParamAccessory", "1.04.1", ItemIDFlag.ACCESSORIES)
    # resident effects for talismans are conditials for attack increases
    effect_ids = get_effect_ids(talismans, ["refId"])

#    protectors = er_params.load("EquipParamProtector", "1.04.1", ItemIDFlag.PROTECTORS)
#    effect_ids = get_effect_ids(protectors, ["residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3"])

    effects = er_params.load("SpEffectParam", "1.04.1", ItemIDFlag.NON_EQUIPABBLE)
    changing_fields = get_changing_fields(effect_ids, effects)

    with open("out.txt", "w") as f:
        for field in sorted(changing_fields):
            f.write(f"{field}\n")

if __name__ == "__main__":
    main()