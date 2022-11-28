from typing import Any, NamedTuple, Self, overload
from erdb.typing.enums import ItemIDFlag


class ParamField(str):
    @property
    def as_str(self) -> str:
        return self

    @property
    def as_int(self) -> int:
        return int(self)

    @property
    def as_bool(self) -> bool:
        return self != "0"

    @property
    def as_float(self) -> float:
        return float(self)

    @overload
    def get_int(self, default: int, null_value: Any = "-1", formatter = lambda x: x) -> int: ...

    @overload
    def get_int(self, default: int | None = None, null_value: Any = "-1", formatter = lambda x: x) -> int | None: ...

    def get_int(self, default: int | None = None, null_value: Any = "-1", formatter = lambda x: x) -> int | None:
        return default if self == str(null_value) else formatter(int(self))

    @overload
    def get_float(self, default: float, null_value: Any = "-1", formatter = lambda x: x) -> float: ...

    @overload
    def get_float(self, default: float | None = None, null_value: Any = "-1", formatter = lambda x: x) -> float | None: ...

    def get_float(self, default: float | None = None, null_value: Any = "-1", formatter = lambda x: x) -> float | None:
        return default if self == str(null_value) else formatter(float(self))

class ParamRow(NamedTuple):
    index: int
    item_id_flag: ItemIDFlag
    name: str
    field_dict: dict[str, str]

    @property
    def index_hex(self) -> str:
        assert self.item_id_flag != ItemIDFlag.DISABLE_CHECK
        return f"{self.index + self.item_id_flag:08X}"

    @property
    def is_base_item(self) -> bool:
        """
        Retrieves whether the item is a non-upgraded version of itself. These usually differ by last two digits of the index.
        """
        return self.index % 100 == 0

    def __getitem__(self, key: str) -> ParamField:
        assert key in self.field_dict, f"\"{key}\" not found"
        return ParamField(self.field_dict[key])

    def __contains__(self, __x: object) -> bool:
        return __x in self.field_dict

    @classmethod
    def make(cls, field_dict: dict[str, str], item_id_flag: ItemIDFlag) -> Self:
        index = int(field_dict["Row ID"])
        return cls(
            index=index,
            item_id_flag=item_id_flag,
            name=field_dict["Row Name"],
            field_dict=field_dict,
        )

ParamDict = dict[int, ParamRow]