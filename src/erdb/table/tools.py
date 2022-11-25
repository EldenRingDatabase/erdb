from erdb.typing.models.tool import Tool
from erdb.typing.models.effect import Effect
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsSortGroupID, GoodsType, ItemIDFlag, ToolAvailability
from erdb.typing.categories import ToolCategory
from erdb.typing.api_version import ApiVersion
from erdb.effect_parser import parse_effects
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def _get_availability(row: ParamRow) -> ToolAvailability:
    T = ToolAvailability

    if row.get_bool("disable_offline"):
        return T.MULTIPLAYER

    return T.ALWAYS if row.get_bool("enable_multi") else T.SINGLEPLAYER

def _is_note_item(name: str) -> bool:
    # 2 Weathered Maps defined in-game, one is NORMAL_ITEM
    return name.startswith("Note: ") or name == "Weathered Map"

class ToolTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Tool,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row.get_int("sortId") < 999999,
        lambda row: row.get_int("sortGroupId") != GoodsSortGroupID.GESTURES,
        lambda row: row.get("goodsType") in [GoodsType.NORMAL_ITEM, GoodsType.REMEMBRANCE, GoodsType.WONDROUS_PHYSICK_TEAR, GoodsType.GREAT_RUNE],
        lambda row: not _is_note_item(row.name),
    ]

    param_retrievers = {
        "effects": ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        effects = data.params["effects"]

        return Tool(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=ToolCategory.from_row(row),
            availability=_get_availability(row),
            fp_cost=row.get_int("consumeMP"),
            is_consumed=row.get_bool("isConsume"),
            is_ladder_usable=row.get_bool("enable_Ladder"),
            is_horseback_usable=row.get_bool("enableRiding"),
            effects=[Effect(**eff) for eff in parse_effects(row, effects, "refId_default")],
        )