from erdb.typing.models.spells import Spell
from erdb.typing.models.common import StatRequirements
from erdb.typing.params import ParamRow
from erdb.typing.enums import GoodsType, ItemIDFlag, SpellHoldAction
from erdb.typing.categories import SpellCategory
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import update_optional
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


def _get_spell_requirements(row: ParamRow) -> StatRequirements:
    requirements = {}
    requirements = update_optional(requirements, "intelligence", row.get_int("requirementIntellect"), 0)
    requirements = update_optional(requirements, "faith", row.get_int("requirementFaith"), 0)
    requirements = update_optional(requirements, "arcane", row.get_int("requirementLuck"), 0)
    return StatRequirements(**requirements)

class SpellTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Spell,
    }

    # Spells are defined in Goods and Magic tables, correct full hex IDs are calculated from Goods
    main_param_retriever = ParamDictRetriever("EquipParamGoods", ItemIDFlag.GOODS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row.get_int("sortId") < 999999,
        lambda row: row.get("goodsType") in [GoodsType.SORCERY_1, GoodsType.INCANTATION_1, GoodsType.SORCERY_2, GoodsType.INCANTATION_2],
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
        row_magic = data.params["magic"][str(row.index)]

        fp_cost = row_magic.get_int("mp")
        fp_extra = row_magic.get_int("mp_charge")

        sp_cost = row_magic.get_int("stamina")
        sp_extra = row_magic.get_int("stamina_charge")

        hold_action = SpellHoldAction.NONE if fp_extra == 0 else SpellHoldAction.CHARGE
        hold_action = hold_action if row_magic.get_int("consumeLoopMP_forMenu") == -1 else SpellHoldAction.CONTINUOUS

        return Spell(
            **cls.make_item(data, row),
            **cls.make_contrib(data, row, "locations", "remarks"),
            fp_cost=fp_cost,
            fp_cost_extra=fp_extra - fp_cost if hold_action == "Charge" else fp_extra,
            sp_cost=sp_cost,
            sp_cost_extra=sp_extra - sp_cost if hold_action == "Charge" else sp_extra,
            category=SpellCategory.from_row(row_magic),
            slots_used=row_magic.get_int("slotLength"),
            hold_action=hold_action,
            is_weapon_buff=row_magic.get_bool("isEnchant"),
            is_shield_buff=row_magic.get_bool("isShieldEnchant"),
            is_horseback_castable=row_magic.get_bool("enableRiding"),
            requirements=_get_spell_requirements(row_magic),
        )