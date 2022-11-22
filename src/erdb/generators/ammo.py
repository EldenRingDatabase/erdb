from erdb.typing.models.ammo import Ammo
from erdb.typing.models.common import Damage
from erdb.typing.models.effect import Effect
from erdb.typing.categories import AmmoCategory
from erdb.typing.params import ParamDict, ParamRow
from erdb.typing.enums import ItemIDFlag
from erdb.utils.common import strip_invalid_name, update_optional
from erdb.effect_parser import parse_status_effects, parse_weapon_effects
from erdb.generators._base import GeneratorDataBase


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

class AmmoGeneratorData(GeneratorDataBase):
    Base = GeneratorDataBase

    @staticmethod # override
    def output_file() -> str:
        return "ammo.json"

    @staticmethod # override
    def element_name() -> str:
        return "Ammo"

    @staticmethod # override
    def model() -> Ammo:
        return Ammo

    # override
    def get_key_name(self, row: ParamRow) -> str:
        return strip_invalid_name(self.msgs["names"][row.index])

    main_param_retriever = Base.ParamDictRetriever("EquipParamWeapon", ItemIDFlag.WEAPONS)

    param_retrievers = {
        "effects": Base.ParamDictRetriever("SpEffectParam", ItemIDFlag.NON_EQUIPABBLE),
    }

    msgs_retrievers = {
        "names": Base.MsgsRetriever("WeaponName"),
        "descriptions": Base.MsgsRetriever("WeaponCaption")
    }

    lookup_retrievers = {}

    def main_param_iterator(self, ammos: ParamDict):
        for row in ammos.values():
            if 1 <= row.get_int("sortId") < 9999999 \
            and AmmoCategory.get(row) is not None:
                yield row

    def construct_object(self, row: ParamRow) -> Ammo:
        effects = self.params["effects"]
        effect_ids = [row.get(f) for f in _BEHAVIOR_EFFECTS_FIELDS]

        return Ammo(
            **self.get_fields_item(row, summary=False),
            **self.get_fields_user_data(row, "locations", "remarks"),
            damage=_get_damages(row),
            category=AmmoCategory.from_row(row),
            effects=[Effect(**eff) for eff in parse_weapon_effects(row)],
            status_effects=parse_status_effects(effect_ids, effects),
        )