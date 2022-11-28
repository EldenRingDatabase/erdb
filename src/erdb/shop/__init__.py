from erdb.typing.params import ParamDict
from erdb.shop.shop_typing import Material, Lineup, Product


"""
Helper class for looking up any sort of item exchanges (purchases, alterations, crafting...)
"""
class Lookup(object):
    _shop_lineup: ParamDict
    _material_sets: ParamDict

    def __init__(self, shop_lineup: ParamDict, material_sets: ParamDict) -> None:
        self._shop_lineup = shop_lineup
        self._material_sets = material_sets

    def get_lineups_from_material(self, material: Material) -> list[Lineup]:
        lineups: list[Lineup] = []

        for lineup_param in self._shop_lineup.values():
            if mat_id := lineup_param["mtrlId"].get_int():
                lineup = Lineup.from_params(lineup_param, self._material_sets[mat_id])
                if material in lineup.materials.keys():
                    lineups.append(lineup)

        return lineups