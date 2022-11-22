from erdb.typing.models.talisman import Talisman
from erdb.typing.models.effect import Effect
from erdb.effect_parser import parse_effects
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


class TalismanGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod
    def output_file() -> str:
        return "talismans.json"

    @staticmethod
    def element_name() -> str:
        return "Talismans"

    @staticmethod
    def model() -> Talisman:
        return Talisman

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    def _find_conflicts(self, group: int, accessories: ParamDict) -> list[str]:
        return [self.get_key_name(t) for t in accessories.values() if t.get_int("accessoryGroup") == group and t.index < 9999999]

    main_param_retriever = Base.ParamDictRetriever("EquipParamAccessory", ItemIDFlag.ACCESSORIES)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE, id_min=310000, id_max=400000)
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("AccessoryName"),
        "summaries": Base.MsgsRetriever("AccessoryInfo"),
        "descriptions": Base.MsgsRetriever("AccessoryCaption")
    }

    lookup_retrievers = {}

    def main_param_iterator(self, talismans: ParamDict):
        for row in talismans.values():
            if row.index >= 1000 and row.index < 999999:
                yield row

    def construct_object(self, row: ParamRow) -> Talisman:
        talismans = self.main_param
        effects = self.params["effects"]

        return Talisman(
            **self.get_fields_item(row),
            **self.get_fields_user_data(row, "locations", "remarks"),
            weight=row.get_float("weight"),
            effects=[Effect(**eff) for eff in parse_effects(row, effects, "refId")],
            conflicts=self._find_conflicts(row.get_int("accessoryGroup"), talismans),
        )