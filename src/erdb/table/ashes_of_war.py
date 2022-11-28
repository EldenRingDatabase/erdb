from erdb.typing.models.ash_of_war import AshOfWar
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag, Affinity
from erdb.typing.categories import ArmamentCategory
from erdb.typing.api_version import ApiVersion
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import TableSpecContext


def _get_categories(row: ParamRow) -> list[ArmamentCategory]:
    return [a for a in list(ArmamentCategory) if row[f"canMountWep_{a.ingame}"].as_bool]

def _get_affinities(row: ParamRow) -> list[Affinity]:
    return [a for a in Affinity if row[f"configurableWepAttr{str(a.id).zfill(2)}"].as_bool]

class AshOfWarTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: AshOfWar,
    }

    main_param_retriever = ParamDictRetriever("EquipParamGem", ItemIDFlag.ACCESSORIES, id_min=10000)

    msg_retrievers = {
        "names": MsgsRetriever("GemName"),
        "summaries": MsgsRetriever("GemInfo"),
        "descriptions": MsgsRetriever("GemCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        return AshOfWar(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            armament_categories=_get_categories(row),
            default_affinity=Affinity.from_id(row["defaultWepAttr"].as_int),
            possible_affinities=_get_affinities(row),
            skill_id=row["swordArtsParamId"].as_int,
        )