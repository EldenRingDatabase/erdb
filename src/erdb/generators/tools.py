from erdb.typing.models.tool import Tool
from erdb.typing.models.effect import Effect
from erdb.effect_parser import parse_effects
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag, ToolAvailability
from erdb.typing.categories import ToolCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_availability(row: ParamRow) -> ToolAvailability:
    T = ToolAvailability

    if row.get_bool("disable_offline"):
        return T.MULTIPLAYER

    return T.ALWAYS if row.get_bool("enable_multi") else T.SINGLEPLAYER

def _is_note_item(name: str) -> bool:
    # GoodsType.INFO_ITEM doesn't apply to all note items
    return name.startswith("Note: ")

class ToolGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "tools.json"

    @staticmethod # override
    def element_name() -> str:
        return "Tools"

    @staticmethod # override
    def model() -> Tool:
        return Tool

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

    def main_param_iterator(self, tools: ParamDict):
        T = GoodsType

        for row in tools.values():
            name = self.get_key_name(row) if row.index in self.msgs["names"] else ""
            if name == "" or _is_note_item(name) or name == "Weathered Map": # 2 defined in game, one is NORMAL_ITEM
                continue

            if 1 <= row.get_int("sortId") < 999999 \
            and row.get_int("sortGroupId") != GoodsSortGroupID.GESTURES \
            and row.get("goodsType") in [T.NORMAL_ITEM, T.REMEMBRANCE, T.WONDROUS_PHYSICK_TEAR, T.GREAT_RUNE]:
                yield row

    def construct_object(self, row: ParamRow) -> Tool:
        effects = self.params["effects"]

        return Tool(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=ToolCategory.from_row(row),
            availability=_get_availability(row),
            fp_cost=row.get_int("consumeMP"),
            is_consumed=row.get_bool("isConsume"),
            is_ladder_usable=row.get_bool("enable_Ladder"),
            is_horseback_usable=row.get_bool("enableRiding"),
            effects=[Effect(**eff) for eff in parse_effects(row, effects, "refId_default")],
        )