from erdb.typing.models.ammo import Ammo
from erdb.typing.models.common import Damage
from erdb.typing.models.effect import Effect
from erdb.typing.categories import AmmoCategory
from erdb.typing.enums import ItemIDFlag
from erdb.typing.params import ParamRow
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import remove_nulls
from erdb.effect_parser import parse_status_effects, parse_weapon_effects
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


_BEHAVIOR_EFFECTS_FIELDS: list[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]

def _get_damages(row: ParamRow) -> Damage:
    data = {
        "physical": row["attackBasePhysics"].get_int(null_value="0"),
        "magic": row["attackBaseMagic"].get_int(null_value="0"),
        "fire": row["attackBaseFire"].get_int(null_value="0"),
        "lightning": row["attackBaseThunder"].get_int(null_value="0"),
        "holy": row["attackBaseDark"].get_int(null_value="0"),
        "stamina": row["attackBaseStamina"].get_int(null_value="0"),
    }

    return Damage(**remove_nulls(data))

class AmmoTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Ammo,
    }

    main_param_retriever = ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row["sortId"].as_int < 9999999,
        lambda row: AmmoCategory.get(row) is not None,
    ]

    param_retrievers = {
        "effects": ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
    }

    msg_retrievers = {
        "names": MsgsRetriever("WeaponName"),
        "descriptions": MsgsRetriever("WeaponCaption"),
    }

    @classmethod
    def make_object(cls, api: ApiVersion, data: RetrieverData, row: ParamRow):
        effects = data.params["effects"]
        effect_ids = [row[f].as_int for f in _BEHAVIOR_EFFECTS_FIELDS]

        return Ammo(
            **cls.make_item(data, row, summary=False),
            **cls.make_contrib(data, row, "locations", "remarks"),
            damage=_get_damages(row),
            category=AmmoCategory.from_row(row),
            effects=[Effect(**eff) for eff in parse_weapon_effects(row)],
            status_effects=parse_status_effects(effect_ids, effects),
        )