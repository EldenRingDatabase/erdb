import re
from functools import total_ordering
from pathlib import Path
from typing import List, NamedTuple

@total_ordering
class GameVersion(NamedTuple):
    major: str
    minor: str
    patch: str
    nums: List[int]

    @classmethod
    def from_string(cls: "GameVersion", version: str) -> "GameVersion":
        parts = version.split(".")
        assert len(parts) == 3, "Invalid version string given"
        assert len(parts[1]) >= 2, "Minor part must be at least 2 digits"

        nums = [int(parts[0]), int(parts[1]), int(parts[2])]
        return cls(parts[0], parts[1], parts[2], nums)

    @classmethod
    def min(cls) -> "GameVersion":
        return cls("0", "00", "0", [0, 0, 0])

    @classmethod
    def max(cls) -> "GameVersion":
        return cls("99999", "99999", "99999", [99999, 99999, 99999])

    @staticmethod
    def match_path(path: Path) -> bool:
        return re.search(r"^[0-9\.]+$", path.name)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, GameVersion):
            return False
        return self.major == __o.major and self.minor == __o.minor and self.patch == __o.patch

    def __lt__(self, __o: "GameVersion") -> bool:
        assert isinstance(__o, GameVersion)
        for this_num, other_num in zip(self.nums, __o.nums):
            if this_num != other_num:
                return this_num < other_num
        return False

class GameVersionRange(NamedTuple):
    begin: GameVersion # including
    end: GameVersion   # excluding
    only: bool=False   # only `begin`

    @classmethod
    def from_string(cls: "GameVersionRange", string: str) -> "GameVersionRange":
        """
        Corresponds to /schema/userdata/version-range-pattern.schema.json
        """
        def _ver(match: re.Match[str]) -> GameVersion:
            return GameVersion.from_string(match.group(1))

        if string == "any version":
            return cls(GameVersion.min(), GameVersion.max())

        if search_only := re.search(r"only (\d+\.\d\d+\.\d+)", string):
            return cls(_ver(search_only), GameVersion.max(), only=True)

        search_begin = re.search(r"from (\d+\.\d\d+\.\d+)", string)
        search_end = re.search(r"until (\d+\.\d\d+\.\d+)", string)
        assert search_begin or search_end, "Invalid version range string"

        begin = _ver(search_begin) if search_begin else GameVersion.min()
        end = _ver(search_end) if search_end else GameVersion.max()

        assert begin < end, "Invalid version range string"
        return cls(begin, end)

    def __contains__(self, version: GameVersion) -> bool:
        assert isinstance(version, GameVersion)
        return self.begin == version if self.only \
            else self.begin <= version and version < self.end