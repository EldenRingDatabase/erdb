from erdb.typing.enums import ItemIDFlag


class ParamRow(object):
    def __init__(self, row: dict[str, str], item_id_flag: ItemIDFlag) -> None:
        self._index = int(row["Row ID"])
        self._item_id_flag = item_id_flag
        self._index_hex = f"{self._index + item_id_flag:08X}"
        self._name = row["Row Name"]
        self._row = row

    @property
    def index(self) -> int:
        return self._index

    @property
    def item_id_flag(self) -> ItemIDFlag:
        return self._item_id_flag

    @property
    def index_hex(self) -> str:
        return self._index_hex

    @property
    def name(self) -> str:
        return self._name

    @property
    def keys(self) -> list[str]:
        return list(self._row.keys())

    def get(self, field: str) -> str:
        assert field in self._row
        return self._row[field]

    def get_int(self, field: str) -> int:
        return int(self.get(field))

    def get_float(self, field: str) -> float:
        return float(self.get(field))

    def get_bool(self, field: str) -> bool:
        return int(self.get(field)) != 0

    def get_int_corrected(self, field: str) -> int:
        """
        Elden Ring uses -1 for "null" int values, correct this to 0.
        """
        val = self.get_int(field)
        return 0 if val == -1 else val

    def is_base_item(self) -> bool:
        """
        Retrieves whether the item is a non-upgraded version of itself. These usually differ by last two digits of the index.
        """
        return self._index % 100 == 0

ParamDict = dict[str, ParamRow]