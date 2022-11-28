from collections import defaultdict

from erdb.loaders.params import load as load_params
from erdb.typing.params import ParamDict
from erdb.typing.enums import ItemIDFlag
from erdb.typing.game_version import GameVersion
from erdb.typing import sp_effect


_IGNORED_FIELDS = [
    "Row ID", "Row Name", "iconId", "lookAtTargetPosOffset", "targetPriority",
    "effectTargetSelf", "effectTargetFriend", "effectTargetEnemy", "effectTargetPlayer",
    "effectTargetAI", "effectTargetLive", "effectTargetGhost", "effectTargetAttacker",
    "vfxId", "vfxId1", "vfxId2", "vfxId3", "vfxId4", "vfxId5", "vfxId6", "vfxId7"
]

def get_effect_ids(rows: ParamDict, fields: list[str]) -> dict[int, set[str]]:
    ids = defaultdict(set)

    for row in rows.values():
        for field in fields:
            if i := row[field].get_int():
                ids[i].add(row.name)

    return ids

def get_changing_fields(effect_ids: dict[int, set[str]], effects: ParamDict) -> list[str]:
    changing_fields = set()
    null_effect = effects[2] # IDs 0 and 1 seem to have some properties filled in

    for field in null_effect.field_dict.keys():
        if field in _IGNORED_FIELDS:
            continue

        null_value = null_effect[field]
        items = []

        for i, item_names in effect_ids.items():
            if null_value != effects[i][field]:
                items += item_names

        if len(items) > 0 and len(items) != len(effect_ids):
            name = sp_effect.details[field]["DisplayName"]
            field_padded = f"{name} ({field})".ljust(64)
            changing_fields.add(f">> {field_padded}: {', '.join(items)}")

    return list(changing_fields)

def main():
    talismans = load_params("EquipParamAccessory", GameVersion.from_string("1.04.1"), ItemIDFlag.ACCESSORIES)
    # resident effects for talismans are conditials for attack increases
    effect_ids = get_effect_ids(talismans, ["refId"])

#    protectors = er_params.load("EquipParamProtector", "1.04.1", ItemIDFlag.PROTECTORS)
#    effect_ids = get_effect_ids(protectors, ["residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3"])

    effects = load_params("SpEffectParam", GameVersion.from_string("1.04.1"), ItemIDFlag.NON_EQUIPABBLE)
    changing_fields = get_changing_fields(effect_ids, effects)

    with open("out.txt", "w") as f:
        for field in sorted(changing_fields):
            f.write(f"{field}\n")

if __name__ == "__main__":
    main()