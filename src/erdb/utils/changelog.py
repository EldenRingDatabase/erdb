from io import TextIOBase
from enum import Enum
from sys import stdout
from typing import Any, NamedTuple, OrderedDict, Self
from pathlib import Path
from difflib import Differ
from operator import methodcaller
from deepdiff import DeepDiff
from contextlib import suppress
from collections import defaultdict

from erdb.table import Table
from erdb.utils.common import as_str
from erdb.typing.game_version import GameVersion
from erdb.typing.effects import SchemaEffect


class ChangelogFormatter(Enum):
    MARKDOWN = "markdown"
    DISCORD = "discord"

class _ChangeType(Enum):
    VALUE = "value"
    ADDED = "added"
    REMOVED = "removed"

    @classmethod
    def get(cls, report_type: str) -> Self:
        if report_type == "values_changed": return _ChangeType.VALUE
        if report_type.endswith("added"):   return _ChangeType.ADDED
        if report_type.endswith("removed"): return _ChangeType.REMOVED
        assert False, f"Unsupported report type: {report_type}"

class _Change(NamedTuple):
    Collection = dict[str, set[Self]] # item name -> set of changes

    change_type: _ChangeType
    property_path: list
    indices_change: bool

    @property
    def display(self) -> str:
        return " > ".join(map(as_str, self.property_path))

    def __hash__(self) -> int:
        return hash((self.display))

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, _Change) and self.display == __o.display

    def navigate(self, data: dict | None) -> Any:
        def _get_any(obj: Any, prop: Any) -> Any:
            if isinstance(obj, list) or isinstance(obj, dict):
                with suppress(KeyError):
                    return obj[prop]
            return getattr(obj, prop, None)

        assert len(self.property_path) > 0, "got a zero-length property_path"
        out = data

        for p in self.property_path:
            if (out := _get_any(out, p)) is None:
                return None

        if self.property_path[-1] == "effects":
            # treat "effects" field in a special way
            return [str(SchemaEffect.from_obj(elem)) for elem in out] # type: ignore

        # TODO: changelog will fail if there is another field
        #       besides "effects" that is a list of objects

        return out

    @classmethod
    def create(cls, change_type: _ChangeType, path: list) -> Self:
        assert len(path) > 0, "Invalid change path"

        if isinstance(path[-1], int):
            assert len(path) > 1, "Invalid change path"
            return cls(change_type, path[:-1], indices_change=True)

        else:
            return cls(change_type, path, indices_change=False)

class FormatterBase:
    _section    = "{value}"
    _header     = "{value}"
    _prop       = "{value}"
    _begin_diff = ""
    _end_diff   = ""
    _begin_list = ""
    _elem_list  = "- "
    _end_list   = ""

    _data: dict[str, list[str]]
    _last_section: str

    def __init__(self) -> None:
        self._data = OrderedDict()

    def _append(self, line: str):
        self._data[self._last_section].append(line)

    def section(self, section: str):
        self._data[section] = list()
        self._last_section = section

    def header(self, header: str):
        self._append(self._header.format(value=header))

    def prop(self, prop: str):
        self._append(self._prop.format(value=prop))

    def begin_diff(self):
        self._append(self._begin_diff)

    def end_diff(self):
        self._append(self._end_diff)

    def add_list(self, elems: list[str]):
        self._append(self._begin_list)
        [self._append(self._elem_list + elem) for elem in elems]
        self._append(self._end_list)

    def line(self, *args: Any):
        self._append(" ".join(map(str, args)))

    def table_of_contents(self, sections: list[str], out: TextIOBase):
        pass

    def write(self, out: TextIOBase):
        data = {section: lines for section, lines in self._data.items() if len(lines) > 0}

        if len(data) == 0:
            return

        self.table_of_contents(list(data.keys()), out)

        for section, lines in data.items():
            out.write(self._section.format(value=section) + "\n")
            out.write("\n".join(lines))

    @classmethod
    def _get_identifier(cls) -> str:
        return cls.__name__.removeprefix("Formatter").lower()

    @classmethod
    def identifiers(cls) -> list[str]:
        return [*map(methodcaller("_get_identifier"), cls.__subclasses__())]

    @classmethod
    def create(cls, identifier) -> Self:
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
    _elem_list  = "* "

    def table_of_contents(self, sections: list[str], out: TextIOBase):
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

def _get_item_changes(old_data: dict, new_data: dict) -> tuple[list[str], list[str], _Change.Collection]:
    diff = DeepDiff(old_data, new_data, view="tree")

    def pop_toplevel(change_type: str) -> list[str]:
        return [c.path(output_format="list")[0] for c in diff.pop(change_type, [])]

    item_changes = defaultdict(set)
    added = pop_toplevel("dictionary_item_added")
    removed = pop_toplevel("dictionary_item_removed")

    for report_type, changes in diff.items():
        change_type = _ChangeType.get(report_type)

        for change in changes:
            item_name, *change_path = change.path(output_format="list")
            item_changes[item_name].add(_Change.create(change_type, change_path))

    return added, removed, item_changes

def generate(from_version: GameVersion, version: GameVersion, out: Path | None, formatter_id: str = "markdown"):
    formatter = FormatterBase.create(formatter_id)
    print(f"Generating changelog from {from_version} to {version}...", flush=True)

    for tb in sorted(Table.effective()):
        print(f"Generating changelog for {tb}...", flush=True)

        new_data = tb.make_generator(version).generate()
        old_data = tb.make_generator(from_version).generate()

        added, removed, item_changes = _get_item_changes(old_data, new_data)

        formatter.section(tb.title)

        if len(added) > 0:
            formatter.header(f"New items added")
            formatter.add_list(added)

        if len(removed) > 0:
            formatter.header(f"Items removed")
            formatter.add_list(removed)

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

    if out is None:
        formatter.write(stdout) # type: ignore

    else:
        with open(out, mode="w", encoding="utf-8") as f:
            formatter.write(f)