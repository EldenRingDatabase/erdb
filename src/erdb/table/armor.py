from erdb.shop import Material
from erdb.typing.models.effect import Effect
from erdb.typing.models.armor import Armor, Absorptions, Resistances
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.typing.categories import ArmorCategory
from erdb.typing.api_version import ApiVersion
from erdb.effect_parser import parse_effects
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData, ShopRetriever
from erdb.table._common import RowPredicate, TableSpecContext


def _get_absorptions(row: ParamRow) -> Absorptions:
    def parse(val: float):
        return round((1 - val) * 100, 1)

    return Absorptions(
        physical=parse(row["neutralDamageCutRate"].as_float),
        strike=parse(row["blowDamageCutRate"].as_float),
        slash=parse(row["slashDamageCutRate"].as_float),
        pierce=parse(row["thrustDamageCutRate"].as_float),
        magic=parse(row["magicDamageCutRate"].as_float),
        fire=parse(row["fireDamageCutRate"].as_float),
        lightning=parse(row["thunderDamageCutRate"].as_float),
        holy=parse(row["darkDamageCutRate"].as_float),
    )

def _get_resistances(row: ParamRow) -> Resistances:
    def check_equal(val1: int, val2: int) -> int:
        if val1 != val2:
            print(f"WARNING: Values mismatch for {row.name} resistances ({val1} != {val2}), displaying the latter.", flush=True)
        return val2

    return Resistances(
        immunity=check_equal(row["resistPoison"].as_int, row["resistDisease"].as_int),
        robustness=check_equal(row["resistFreeze"].as_int, row["resistBlood"].as_int),
        focus=check_equal(row["resistSleep"].as_int, row["resistMadness"].as_int),
        vitality=row["resistCurse"].as_int,
        poise=round(row["toughnessCorrectRate"].as_float * 1000)
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
            weight=row["weight"].as_float,
            icon_fem=row["iconIdF"].as_int,
            absorptions=_get_absorptions(row),
            resistances=_get_resistances(row),
            effects=[Effect(**eff) for eff in armor_effects]
        )