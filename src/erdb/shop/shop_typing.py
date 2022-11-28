from enum import IntEnum
from typing import Dict, List, NamedTuple, Self

from erdb.typing.params import ParamRow


class Material(NamedTuple):
    class Category(IntEnum):
        NONE = 0
        PROTECTOR = 1
        GOOD = 4
        UNKNOWN = 15
    
    index: int
    category: Category

    def __hash__(self) -> int:
        return hash((self.index, self.category))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Material):
            return False
        return self.index == __o.index and self.category == __o.category

class Product(NamedTuple):
    class Category(IntEnum):
        WEAPON = 0
        PROTECTOR = 1
        ACCESSORY = 2
        GOOD = 3
        ASHES = 4

    index: int
    category: Category

    def __hash__(self) -> int:
        return hash((self.index, self.category))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Product):
            return False
        return self.index == __o.index and self.category == __o.category

class Currency(IntEnum):
    RUNES = 0
    DRAGON_HEART = 1
    STARLIGHT_SHARD = 2
    UNKNOWN = 3
    LOST_ASHES_OF_WAR = 4

class MaterialSetParams(NamedTuple):
    index: str
    category: str
    quantity: str

_MATERIAL_SET_PARAM_LIST: List[MaterialSetParams] = [
    MaterialSetParams("materialId01", "materialCate01", "itemNum01"),
    MaterialSetParams("materialId02", "materialCate02", "itemNum02"),
    MaterialSetParams("materialId03", "materialCate03", "itemNum03"),
    MaterialSetParams("materialId04", "materialCate04", "itemNum04"),
    MaterialSetParams("materialId05", "materialCate05", "itemNum05"),
    MaterialSetParams("materialId06", "materialCate06", "itemNum06"),
]

class Lineup(NamedTuple):
    product: Product
    price: int=0
    materials: Dict[Material, int]={} # material -> quantity
    currency: Currency=Currency.RUNES

    @classmethod
    def from_params(cls, lineup_param: ParamRow, material_set: ParamRow) -> Self:
        product = Product(lineup_param["equipId"].as_int, Product.Category(lineup_param["equipType"].as_int))
        materials: Dict[Material, int] = {}

        for param in _MATERIAL_SET_PARAM_LIST:
            if mat_id := material_set[param.index].get_int():
                category = Material.Category(material_set[param.category].as_int)
                materials[Material(mat_id, category)] = material_set[param.quantity].as_int

        return cls(
            product=product,
            price=lineup_param["value"].as_int,
            materials=materials,
            currency=Currency(lineup_param["costType"].as_int)
        )