from erdb.typing.models.spells import Spell
from erdb.typing.models.common import StatRequirements
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag, SpellHoldAction
from erdb.typing.categories import SpellCategory
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import remove_nulls
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def _get_spell_requirements(row: ParamRow) -> StatRequirements:
    data = {
        "intelligence": row["requirementIntellect"].get_int(null_value=0),
        "faith": row["requirementFaith"].get_int(null_value=0),
        "arcane": row["requirementLuck"].get_int(null_value=0),
    }

    return StatRequirements(**remove_nulls(data))

class SpellTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Spell,
    }

    # Spells are defined in Goods and Magic tables, correct full hex IDs are calculated from Goods
    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row["sortId"].as_int < 999999,
        lambda row: row["goodsType"] in [GoodsType.SORCERY_1, GoodsType.INCANTATION_1, GoodsType.SORCERY_2, GoodsType.INCANTATION_2],
    ]

    param_retrievers = {
        "magic": ParamDictRetriever("Magic", ItemIDFlag.NON_EQUIPABBLE)
    }

    msg_retrievers = {
        "names": MsgsRetriever("GoodsName"),
        "summaries": MsgsRetriever("GoodsInfo"),
        "descriptions": MsgsRetriever("GoodsCaption")
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        row_magic = data.params["magic"][row.index]

        fp_cost = row_magic["mp"].as_int
        fp_extra = row_magic["mp_charge"].as_int

        sp_cost = row_magic["stamina"].as_int
        sp_extra = row_magic["stamina_charge"].as_int

        hold_action = SpellHoldAction.NONE if fp_extra == 0 else SpellHoldAction.CHARGE
        hold_action = SpellHoldAction.CONTINUOUS if row_magic["consumeLoopMP_forMenu"].get_int() else hold_action 

        return Spell(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            fp_cost=fp_cost,
            fp_cost_extra=fp_extra - fp_cost if hold_action == "Charge" else fp_extra,
            sp_cost=sp_cost,
            sp_cost_extra=sp_extra - sp_cost if hold_action == "Charge" else sp_extra,
            category=SpellCategory.from_row(row_magic),
            slots_used=row_magic["slotLength"].as_int,
            hold_action=hold_action,
            is_weapon_buff=row_magic["isEnchant"].as_bool,
            is_shield_buff=row_magic["isShieldEnchant"].as_bool,
            is_horseback_castable=row_magic["enableRiding"].as_bool,
            requirements=_get_spell_requirements(row_magic),
        )