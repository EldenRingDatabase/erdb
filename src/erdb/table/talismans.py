from erdb.typing.models.talisman import Talisman
from erdb.typing.models.effect import Effect
from erdb.typing.models import NonEmptyStr
from erdb.effect_parser import parse_effects
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


class TalismanTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Talisman,
    }

    main_param_retriever = ParamDictRetriever("EquipParamAccessory", ItemIDFlag.ACCESSORIES)

    predicates: list[RowPredicate] = [
        lambda row: 1000 <= row.index < 999999,
    ]

    param_retrievers = {
        "effects": ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE, id_min=310000, id_max=400000)
    }

    msg_retrievers = {
        "names": MsgsRetriever("AccessoryName"),
        "summaries": MsgsRetriever("AccessoryInfo"),
        "descriptions": MsgsRetriever("AccessoryCaption")
    }

    @classmethod
    def _find_conflicts(cls, data: RetrieverData, group: int) -> list[NonEmptyStr]:
        def valid(row: ParamRow) -> bool:
            return row["accessoryGroup"].as_int == group and row.index < 9999999
        return [NonEmptyStr(cls.parse_name(data.msgs["names"][row.index])) for row in data.main_param.values() if valid(row)]

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        effects = data.params["effects"]

        return Talisman(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            weight=row["weight"].as_float,
            effects=[Effect(**eff) for eff in parse_effects(row, effects, "refId")],
            conflicts=cls._find_conflicts(data, row["accessoryGroup"].as_int),
        )