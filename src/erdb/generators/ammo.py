from typing import Dict, List, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.utils.common import strip_invalid_name, update_optional
from erdb.effect_parser import parse_status_effects, parse_weapon_effects
from erdb.generators._base import GeneratorDataBase


_BEHAVIOR_EFFECTS_FIELDS: List[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]

_AMMO_TYPES: Dict[int, str] = {
    81: "Arrow",
    83: "Greatarrow",
    85: "Bolt",
    86: "Greatbolt",
}

def _get_damages(row: ParamRow) -> Dict[str, int]:
    damages = {}
    damages = update_optional(damages, "physical", row.get_int("attackBasePhysics"), 0)
    damages = update_optional(damages, "magic", row.get_int("attackBaseMagic"), 0)
    damages = update_optional(damages, "fire", row.get_int("attackBaseFire"), 0)
    damages = update_optional(damages, "lightning", row.get_int("attackBaseThunder"), 0)
    damages = update_optional(damages, "holy", row.get_int("attackBaseDark"), 0)
    damages = update_optional(damages, "stamina", row.get_int("attackBaseStamina"), 0)
    return damages

class AmmoGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "ammo.json"

    @staticmethod # override
    def schema_file() -> str:
        return "ammo.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Ammo"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
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
            "ammo/definitions/Ammo/properties")
        store.update(schema.load_properties("effect")[1])
        store.update(schema.load_enums("ammo-names", "status-effect-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
        return properties, store

    def main_param_iterator(self, ammos: ParamDict):
        for row in ammos.values():
            if 1 <= row.get_int("sortId") < 9999999 \
            and row.get_int("wepType") in _AMMO_TYPES.keys():
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        effects = self.params["effects"]
        effect_ids = [row.get(f) for f in _BEHAVIOR_EFFECTS_FIELDS]

        return self.get_fields_item(row, summary=False) | self.get_fields_user_data(row, "locations", "remarks") | {
            "damage": _get_damages(row),
            "category": _AMMO_TYPES[row.get_int("wepType")],
            "effects": parse_weapon_effects(row),
            "status_effects": parse_status_effects(effect_ids, effects)
        }