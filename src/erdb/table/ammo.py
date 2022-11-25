from erdb.typing.models.ammo import Ammo
from erdb.typing.models.common import Damage
from erdb.typing.models.effect import Effect
from erdb.typing.categories import AmmoCategory
from erdb.typing.enums import ItemIDFlag
from erdb.typing.params import ParamRow
from erdb.typing.api_version import ApiVersion
from erdb.utils.common import update_optional
from erdb.effect_parser import parse_status_effects, parse_weapon_effects
from erdb.table._retrievers import ParamDictRetriever, MsgsRetriever, RetrieverData
from erdb.table._common import RowPredicate, TableSpecContext


_BEHAVIOR_EFFECTS_FIELDS: list[str] = ["spEffectBehaviorId0", "spEffectBehaviorId1", "spEffectBehaviorId2"]

def _get_damages(row: ParamRow) -> Damage:
    damages = {}
    damages = update_optional(damages, "physical", row.get_int("attackBasePhysics"), 0)
    damages = update_optional(damages, "magic", row.get_int("attackBaseMagic"), 0)
    damages = update_optional(damages, "fire", row.get_int("attackBaseFire"), 0)
    damages = update_optional(damages, "lightning", row.get_int("attackBaseThunder"), 0)
    damages = update_optional(damages, "holy", row.get_int("attackBaseDark"), 0)
    damages = update_optional(damages, "stamina", row.get_int("attackBaseStamina"), 0)
    return Damage(**damages)

class AmmoTableSpec(TableSpecContext):
    model = {
        ApiVersion.VER_1: Ammo,
    }

    main_param_retriever = ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS)

    predicates: list[RowPredicate] = [
        lambda row: 1 <= row.get_int("sortId") < 9999999,
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
        effect_ids = [row.get(f) for f in _BEHAVIOR_EFFECTS_FIELDS]

        return Ammo(
            **cls.make_item(data, row, summary=False),
            **cls.make_contrib(data, row, "locations", "remarks"),
            damage=_get_damages(row),
            category=AmmoCategory.from_row(row),
            effects=[Effect(**eff) for eff in parse_weapon_effects(row)],
            status_effects=parse_status_effects(effect_ids, effects),
        )