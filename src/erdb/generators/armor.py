from erdb.shop import Material
from erdb.typing.models.effect import Effect
from erdb.typing.models.armor import Armor, Absorptions, Resistances
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.categories import ArmorCategory
from erdb.typing.api_version import ApiVersion
from erdb.effect_parser import parse_effects
from erdb.generators._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData, ShopRetriever
from erdb.generators._common import RowPredicate, TableSpecContext


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

class ArmorTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Armor,
    }

    main_param_retriever = ParamDictRetriever("EquipParamProtector", ItemIDFlag.PROTECTORS)

    predicates: list[RowPredicate] = [
        lambda row: row.index >= 40000,
        lambda row: len(row.name) > 0,
    ]

    param_retrievers = {
        "effects": ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
    }

    msg_retrievers = {
        "names": MsgsRetriever("ProtectorName"),
        "summaries": MsgsRetriever("ProtectorInfo"),
        "descriptions": MsgsRetriever("ProtectorCaption"),
    }

    shop_retrievers = {
        "armor_shop": ShopRetriever(
            shop_lineup_id_min=110000, shop_lineup_id_max=112000,
            material_set_id_min=900100, material_set_id_max=901000,
        )
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        names = data.msgs["names"]
        effects = data.params["effects"]
        armor_shop = data.shops["armor_shop"]

        material = Material(row.index, Material.Category.PROTECTOR)
        lineups = armor_shop.get_lineups_from_material(material)
        assert len(lineups) in [0, 2], "Each armor should have either none or self-/boc-made alterations"
        altered = "" if len(lineups) == 0 else cls.parse_name(names[lineups[0].product.index])

        armor_effects = parse_effects(row, effects, "residentSpEffectId", "residentSpEffectId2", "residentSpEffectId3")

        return Armor(
            **cls.make_item(data, row, summary=False),
            **cls.make_contrib(data, row, "locations", "remarks"),
            category=ArmorCategory.from_row(row),
            altered=altered,
            weight=row.get_float("weight"),
            absorptions=_get_absorptions(row),
            resistances=_get_resistances(row),
            effects=[Effect(**eff) for eff in armor_effects]
        )