from erdb.shop import Material
from erdb.typing.models.effect import Effect
from erdb.typing.models.armor import Armor, Absorptions, Resistances
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.categories import ArmorCategory
from erdb.effect_parser import parse_effects
from erdb.utils.common import strip_invalid_name
from erdb.generators._base import GeneratorDataBase


def _get_absorptions(row: ParamRow) -> Absorptions:
    def parse(val: float):
        return round((1 - val) * 100, 1)

    return Absorptions(
        physical=parse(row.get_float("neutralDamageCutRate")),
        strike=parse(row.get_float("blowDamageCutRate")),
        slash=parse(row.get_float("slashDamageCutRate")),
        pierce=parse(row.get_float("thrustDamageCutRate")),
        magic=parse(row.get_float("magicDamageCutRate")),
        fire=parse(row.get_float("fireDamageCutRate")),
        lightning=parse(row.get_float("thunderDamageCutRate")),
        holy=parse(row.get_float("darkDamageCutRate")),
    )

def _get_resistances(row: ParamRow) -> Resistances:
    def check_equal(*values: int):
        ret = values[0]
        for val in values:
            if ret != val:
                print(f"WARNING: Values mismatch for {row.name} resistances ({ret} != {val}), displaying the latter.", flush=True)
            ret = val
        return ret

    return Resistances(
        immunity=check_equal(row.get_int("resistPoison"), row.get_int("resistDisease")),
        robustness=check_equal(row.get_int("resistFreeze"), row.get_int("resistBlood")),
        focus=check_equal(row.get_int("resistSleep"), row.get_int("resistMadness")),
        vitality=check_equal(row.get_int("resistCurse")),
        poise=round(row.get_float("toughnessCorrectRate") * 1000)
    )

class ArmorGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "armor.json"

    @staticmethod # override
    def element_name() -> str:
        return "ArmorPieces"

    @staticmethod # override
    def model() -> Armor:
        return Armor

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamProtector", ItemIDFlag.PROTECTORS)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE)
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("ProtectorName"),
        "summaries": Base.MsgsRetriever("ProtectorInfo"),
        "descriptions": Base.MsgsRetriever("ProtectorCaption")
    }

    lookup_retrievers = {
        "armor_lookup": Base.LookupRetriever(
            shop_lineup_id_min=110000, shop_lineup_id_max=112000,
            material_set_id_min=900100, material_set_id_max=901000,
        )
    }

    def main_param_iterator(self, armor: ParamDict):
        for row in armor.values():
            if row.index >= 40000 and len(row.name) > 0:
                yield row

    def construct_object(self, row: ParamRow) -> Armor:
        names = self.msgs["names"]
        effects = self.params["effects"]
        armor_lookup = self.lookups["armor_lookup"]

        material = Material(row.index, Material.Category.PROTECTOR)
        lineups = armor_lookup.get_lineups_from_material(material)
        assert len(lineups) in [0, 2], "Each armor should have either none or self-/boc-made alterations"
        altered = "" if len(lineups) == 0 else strip_invalid_name(names[lineups[0].product.index])

        armor_effects = parse_effects(row, effects, "residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3")

        return Armor(
            **self.get_fields_item(row, summary=False),
            **self.get_fields_user_data(row, "locations", "remarks"),
            category=ArmorCategory.from_row(row),
            altered=altered,
            weight=row.get_float("weight"),
            absorptions=_get_absorptions(row),
            resistances=_get_resistances(row),
            effects=[Effect(**eff) for eff in armor_effects]
        )