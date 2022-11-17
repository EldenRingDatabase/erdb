from typing import Dict, Iterator, Tuple

import erdb.loaders.schema as schema
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag
from erdb.utils.common import strip_invalid_name, update_optional
from erdb.generators._base import GeneratorDataBase


def _get_magic_type(behavior_type: str) -> str:
    return {"0": "Sorcery", "1": "Incantation"}[behavior_type]

def _get_spell_requirements(row: ParamRow) -> Dict[str, int]:
    requirements = {}
    requirements = update_optional(requirements, "intelligence", row.get_int("requirementIntellect"), 0)
    requirements = update_optional(requirements, "faith", row.get_int("requirementFaith"), 0)
    requirements = update_optional(requirements, "arcane", row.get_int("requirementLuck"), 0)
    return requirements

class SpellGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "spells.json"

    @staticmethod # override
    def schema_file() -> str:
        return "spells.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Spells"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    # Spells are defined in Goods and Magic tables, correct full hex IDs are calculated from Goods
    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {
        "magic": Base.ParamDictRetriever("Magic", ItemIDFlag.NON_EQUIPABBLE)
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GoodsName"),
        "summaries": Base.MsgsRetriever("GoodsInfo"),
        "descriptions": Base.MsgsRetriever("GoodsCaption")
    }

    lookup_retrievers = {}

    @staticmethod
    def schema_retriever() -> Tuple[Dict, Dict[str, Dict]]:
        properties, store = schema.load_properties(
            "item/properties",
            "item/definitions/ItemUserData/properties",
            "spells/definitions/Spell/properties")
        store.update(schema.load_enums("spell-names"))
        return properties, store

    def main_param_iterator(self, spells: ParamDict) -> Iterator[ParamRow]:
        T = GoodsType
        for row in spells.values():
            if row.get("goodsType") in [T.SORCERY_1, T.INCANTATION_1, T.SORCERY_2, T.INCANTATION_2] \
            and self.msgs["names"].get(row.index, "[ERROR]") not in ["[ERROR]", "%null%"]:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        row_magic = self.params["magic"][str(row.index)]

        fp_cost = row_magic.get_int("mp")
        fp_extra = row_magic.get_int("mp_charge")

        sp_cost = row_magic.get_int("stamina")
        sp_extra = row_magic.get_int("stamina_charge")

        hold_action = "None" if fp_extra == 0 else "Charge"
        hold_action = hold_action if row_magic.get_int("consumeLoopMP_forMenu") == -1 else "Continuous"

        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "fp_cost": fp_cost,
            "fp_cost_extra": fp_extra - fp_cost if hold_action == "Charge" else fp_extra,
            "sp_cost": sp_cost,
            "sp_cost_extra": sp_extra - sp_cost if hold_action == "Charge" else sp_extra,
            "type": _get_magic_type(row_magic.get("ezStateBehaviorType")),
            "slots_used": row_magic.get_int("slotLength"),
            "hold_action": hold_action,
            "is_weapon_buff": row_magic.get_bool("isEnchant"),
            "is_shield_buff": row_magic.get_bool("isShieldEnchant"),
            "is_horseback_castable": row_magic.get_bool("enableRiding"),
            "requirements": _get_spell_requirements(row_magic)
        }