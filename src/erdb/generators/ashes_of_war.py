from erdb.typing.models.ash_of_war import AshOfWar
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag, Affinity
from erdb.typing.categories import ArmamentCategory
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_categories(row: ParamRow) -> list[ArmamentCategory]:
    return [a for a in list(ArmamentCategory) if row.get_bool(f"canMountWep_{a.ingame}")]

def _get_affinities(row: ParamRow) -> list[Affinity]:
    return [a for a in Affinity if row.get_bool(f"configurableWepAttr{str(a.id).zfill(2)}")]

class AshOfWarGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "ashes-of-war.json"

    @staticmethod # override
    def element_name() -> str:
        return "AshesOfWar"

    @staticmethod # override
    def model() -> AshOfWar:
        return AshOfWar

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamGem", ItemIDFlag.ACCESSORIES, id_min=10000)

    param_retrievers = {}

    msgs_retrievers = {
        "names": Base.MsgsRetriever("GemName"),
        "summaries": Base.MsgsRetriever("GemInfo"),
        "descriptions": Base.MsgsRetriever("GemCaption")
    }

    lookup_retrievers = {}

    def main_param_iterator(self, ashes_of_war: ParamDict):
        for row in ashes_of_war.values():
            yield row

    def construct_object(self, row: ParamRow) -> AshOfWar:
        return AshOfWar(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            armament_categories=_get_categories(row),
            default_affinity=Affinity.from_id(row.get_int("defaultWepAttr")),
            possible_affinities=_get_affinities(row),
            skill_id=row.get_int("swordArtsParamId"),
        )