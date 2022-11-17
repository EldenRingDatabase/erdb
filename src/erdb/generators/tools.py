from typing import Dict, Iterator, Tuple

import erdb.loaders.schema as schema
from erdb.effect_parser import parse_effects
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_category(row: ParamRow) -> str:
    goods_type = row.get("goodsType")

    if goods_type == GoodsType.WONDROUS_PHYSICK_TEAR:
        return "Crystal Tear"

    if goods_type == GoodsType.GREAT_RUNE:
        return "Great Rune"

    G = GoodsSortGroupID
    return {
        G.GROUP_1: "Essential",
        G.GROUP_2: "Edible",
        G.GROUP_3: "Pot",
        G.GROUP_4: "Aromatic",
        G.GROUP_5: "Throwable",
        G.GROUP_6: "Offensive",
        G.GROUP_7: "Grease",
        G.GROUP_8: "Utility",
        G.GROUP_9: "Utility",
        G.GROUP_10: "Golden Rune",
        G.REMEMBERANCES: "Rememberance",
        G.ONLINE: "Online"
    }[row.get_int("sortGroupId")]

def _get_availability(row: ParamRow) -> str:
    if row.get_bool("disable_offline"):
        return "Multiplayer"
    return "Always" if row.get_bool("enable_multi") else "Singleplayer"

def _is_note_item(name: str) -> bool:
    #GoodsType.INFO_ITEM doesn't apply to all note items
    return name.startswith("Note: ")

class ToolGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "tools.json"

    @staticmethod # override
    def schema_file() -> str:
        return "tools.schema.json"

    @staticmethod # override
    def element_name() -> str:
        return "Tools"

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE)
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
            "tools/definitions/Tool/properties")
        store.update(schema.load_properties("effect")[1])
        store.update(schema.load_enums("item-names", "attribute-names", "attack-types", "effect-types", "health-conditions", "attack-conditions"))
        return properties, store

    def main_param_iterator(self, tools: ParamDict) -> Iterator[ParamRow]:
        T = GoodsType

        for row in tools.values():
            name = self.get_key_name(row) if row.index in self.msgs["names"] else ""
            if name == "" or _is_note_item(name) or name == "Weathered Map": # 2 defined in game, one is NORMAL_ITEM
                continue

            if 1 <= row.get_int("sortId") < 999999 \
            and row.get_int("sortGroupId") != GoodsSortGroupID.GESTURES \
            and row.get("goodsType") in [T.NORMAL_ITEM, T.REMEMBRANCE, T.WONDROUS_PHYSICK_TEAR, T.GREAT_RUNE]:
                yield row

    def construct_object(self, row: ParamRow) -> Dict:
        effects = self.params["effects"]

        return self.get_fields_item(row) | self.get_fields_user_data(row, "locations", "remarks") | {
            "category": _get_category(row),
            "availability": _get_availability(row),
            "fp_cost": row.get_int("consumeMP"),
            "is_consumed": row.get_bool("isConsume"),
            "is_ladder_usable": row.get_bool("enable_Ladder"),
            "is_horseback_usable": row.get_bool("enableRiding"),
            "effects": parse_effects(row, effects, "refId_default"),
        }