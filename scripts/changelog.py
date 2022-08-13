from io import TextIOBase
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, OrderedDict, Set
from pathlib import Path
from difflib import Differ
from operator import methodcaller, eq
from deepdiff import DeepDiff
from collections import defaultdict
from scripts.erdb_generators import GameParam
from scripts.game_version import GameVersion

class ChangelogFormatter(Enum):
    MARKDOWN = "markdown"
    DISCORD = "discord"

class _ChangeType(Enum):
    VALUE = "value"
    ADDED = "added"
    REMOVED = "removed"

    @staticmethod
    def get(report_type: str) -> "_ChangeType":
        if report_type == "values_changed": return _ChangeType.VALUE
        if report_type.endswith("added"):   return _ChangeType.ADDED
        if report_type.endswith("removed"): return _ChangeType.REMOVED
        assert False, f"Unsupported report type: {report_type}"

class _Change(NamedTuple):
    change_type: _ChangeType
    property_path: List[str]
    indices_change: bool

    @property
    def display(self) -> str:
        return " > ".join(self.property_path)

    def __hash__(self) -> int:
        return hash((self.display))

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, _Change) and self.display == __o.display

    def navigate(self, data: Optional[Dict]) -> Any:
        out = data

        for p in self.property_path:
            if (out := out.get(p)) is None:
                return None

        return out

    @classmethod
    def create(cls, change_type: _ChangeType, path: List) -> "_Change":
        assert len(path) > 0, "Invalid change path"

        if isinstance(path[-1], int):
            assert len(path) > 1, "Invalid change path"
            return cls(change_type, path[:-1], indices_change=True)

        else:
            return cls(change_type, path, indices_change=False)

class FormatterBase():
    _section    = "{value}"
    _header     = "{value}"
    _prop       = "{value}"
    _begin_diff = ""
    _end_diff   = ""

    _data: Dict[str, List[str]]
    _last_section: str

    def __init__(self) -> None:
        self._data = OrderedDict()

    def section(self, section: str):
        self._data[section] = list()
        self._last_section = section

    def header(self, header: str):
        self._data[self._last_section].append(self._header.format(value=header))

    def prop(self, prop: str):
        self._data[self._last_section].append(self._prop.format(value=prop))

    def begin_diff(self):
        self._data[self._last_section].append(self._begin_diff)

    def end_diff(self):
        self._data[self._last_section].append(self._end_diff)

    def line(self, *args: Any):
        self._data[self._last_section].append(" ".join(map(str, args)))

    def table_of_contents(self, sections: List[str], out: TextIOBase):
        pass

    def write(self, out: TextIOBase):
        data = {section: lines for section, lines in self._data.items() if len(lines) > 0}

        if len(data) == 0:
            return

        self.table_of_contents(data.keys(), out)

        for section, lines in data.items():
            out.write(self._section.format(value=section) + "\n")
            out.write("\n".join(lines))

    @classmethod
    def _get_identifier(cls) -> str:
        return cls.__name__.removeprefix("Formatter").lower()

    @classmethod
    def identifiers(cls) -> List[str]:
        return [*map(methodcaller("_get_identifier"), cls.__subclasses__())]

    @classmethod
    def create(cls, identifier) -> "FormatterBase":
        for subcls in cls.__subclasses__():
            if identifier == subcls._get_identifier():
                return subcls()

        assert False, f"Formatter not found for {identifier}."

class FormatterMarkdown(FormatterBase):
    _section    = "# {value} [[^](#contents)]"
    _header     = "### {value}"
    _prop       = "`{value}`"
    _begin_diff = "```diff"
    _end_diff   = "```"

    def table_of_contents(self, sections: List[str], out: TextIOBase):
        out.write("# Contents\n")

        for section in sections:
            anchor = section.replace(' ', '-')
            out.write(f"* [{section}](#{anchor}-)\n")

        out.write("***\n")

class FormatterDiscord(FormatterBase):
    _section    = "\n\n>> **{value}**\n"
    _header     = "**{value}**"
    _prop       = "> {value}"
    _begin_diff = "```diff"
    _end_diff   = "```"

class FormatterText(FormatterBase):
    _section    = "\n\n{value}\n"
    _header     = "\n{value}"
    _prop       = "{value}"
    _begin_diff = "---"
    _end_diff   = "---"

def _get_item_changes(old_data: Dict, new_data: Dict) -> Dict[str, Set[_Change]]:
    diff = DeepDiff(old_data, new_data, view="tree")
    item_changes = defaultdict(set)

    for report_type, changes in diff.items():
        change_type = _ChangeType.get(report_type)

        for change in changes:
            item_name, *change_path = change.path(output_format="list")
            item_changes[item_name].add(_Change.create(change_type, change_path))

    return item_changes

def generate(from_version: GameVersion, version: GameVersion, out: Path, formatter_id: str="markdown"):
    formatter = FormatterBase.create(formatter_id)

    for gen_factory in sorted(GameParam.effective()):
        print(f"Generating changelog for {gen_factory}...", flush=True)

        new_data = gen_factory.construct(version).generate()
        old_data = gen_factory.construct(from_version).generate()

        item_changes = _get_item_changes(old_data, new_data)

        formatter.section(gen_factory.title)

        for item_name, changes in item_changes.items():
            formatter.header(item_name)

            for change in changes:
                formatter.prop(change.display)
                formatter.begin_diff()

                old_value = change.navigate(old_data[item_name])
                new_value = change.navigate(new_data[item_name])

                if change.indices_change:
                    for line in Differ().compare(old_value, new_value):
                        if not line.startswith("?"):
                            formatter.line(line)

                else:
                    if change.change_type in [_ChangeType.VALUE, _ChangeType.REMOVED]:
                        formatter.line("-", old_value)

                    if change.change_type in [_ChangeType.VALUE, _ChangeType.ADDED]:
                        formatter.line("+", new_value)

                formatter.end_diff()
                formatter.line("")

    with open(out, mode="w") as f:
        formatter.write(f)