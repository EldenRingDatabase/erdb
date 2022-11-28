import re
from functools import total_ordering
from pathlib import Path
from typing import Any, Generator, NamedTuple, Self


@total_ordering
class GameVersion(NamedTuple):
    major: str
    minor: str
    patch: str
    nums: list[int]

    @classmethod
    def from_nums(cls, major_int: int, minor_int: int, patch_int: int) -> Self:
        major = str(major_int)
        minor = f"{minor_int:02}"
        patch = str(patch_int)

        assert len(major) == 1
        assert len(minor) == 2
        assert len(patch) == 1

        return cls(major, minor, patch, [major_int, minor_int, patch_int])

    @classmethod
    def from_string(cls, version: str) -> Self:
        parts = version.split(".")
        assert len(parts) == 3, "Invalid version string given"
        assert len(parts[1]) >= 2, "Minor part must be at least 2 digits"

        nums = [int(parts[0]), int(parts[1]), int(parts[2])]
        return cls(parts[0], parts[1], parts[2], nums)

    @classmethod
    def from_any(cls, obj: Any) -> Self:
        if isinstance(obj, GameVersion):
            return obj

        if isinstance(obj, str):
            return GameVersion.from_string(obj)

        if isinstance(obj, Path):
            with open(obj, "r") as f:
                data = f.read()
            return GameVersion.from_string(data)

        if isinstance(obj, list):
            assert len(obj) == 3 and all(isinstance(elem, int) for elem in obj)
            return GameVersion.from_nums(obj[0], obj[1], obj[2])

        assert False, "Cannot parse GameVersion"

    @classmethod
    def min(cls) -> Self:
        return cls("0", "00", "0", [0, 0, 0])

    @classmethod
    def max(cls) -> Self:
        return cls("99999", "99999", "99999", [99999, 99999, 99999])

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

    def iterate(self, versions: list[GameVersion]) -> Generator[GameVersion, None, None]:
        for version in versions:
            if version in self:
                yield version

    @classmethod
    def from_version(cls, version: GameVersion) -> Self:
        return cls(version, GameVersion.max(), only=True)

    @classmethod
    def from_string(cls, string: str) -> Self:
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

class GameVersionInstance(NamedTuple):
    application: GameVersion
    regulation: GameVersion

    @property
    def effective(self) -> GameVersion:
        return max(self.application, self.regulation)

    @classmethod
    def construct(cls, application: Any, regulation: Any) -> Self:
        return cls(GameVersion.from_any(application), GameVersion.from_any(regulation))

    def __str__(self) -> str:
        return f"(app: {self.application}, regulation: {self.regulation})"
