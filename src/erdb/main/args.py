from inspect import Parameter, signature
from argparse import ArgumentParser, BooleanOptionalAction, Action
from pathlib import Path
from typing import Any, Callable, NamedTuple, Sequence, Self

from erdb.table import Table
from erdb.loaders import GAME_VERSIONS
from erdb.utils.changelog import FormatterBase
from erdb.typing.game_version import GameVersion, GameVersionRange


def _parse_all_tables(tables: list[Table], all_effective_tables) -> list[Table]:
    table_set = set(tables)

    if Table.ALL in table_set:
        table_set.update(all_effective_tables)
        table_set.remove(Table.ALL)

    return list(table_set)

def _infer_annotation(type: Any, **kwargs) -> Any:
    if kwargs.get("action") in ["store_true", BooleanOptionalAction]:
        return bool
    
    assert type is not None, "Annotation cannot be deduced if no type is provided."

    if "default" in kwargs:
        if kwargs["default"] == None:
            return type | None

        if isinstance(kwargs["default"], list):
            return list[type]

    return type

class _TablesAction(Action):
    def __call__(self, parser, namespace, values: list[Table], option_string=None):
        setattr(namespace, self.dest, _parse_all_tables(values, Table))

class _GamedataAction(Action):
    def __call__(self, parser, namespace, values: list[str], option_string=None):
        setattr(namespace, self.dest, GameVersionRange.from_string(" ".join(values)))

class _ItemTypesAction(Action):
    def __call__(self, parser, namespace, values: list[Table], option_string=None):
        setattr(namespace, self.dest, _parse_all_tables(values, _ItemTypesAction.choices()))

    @staticmethod
    def choices() -> list[Table]:
        return [Table.ALL] + [tb for tb in Table.effective() if tb.spec.has_icons()]

class _Argument(NamedTuple):
    names: tuple
    param: Parameter
    kwargs: dict

    @classmethod
    def make(cls, *names: str, type: Any | None = None, annotation: Any | None = None, **kwargs) -> Self:
        assert len(names) > 0, "No names given to _Argument."
        param_name = names[0].removeprefix("--").replace("-", "_")

        if annotation is None:
            annotation = _infer_annotation(type, **kwargs)

        return cls(
            names,
            Parameter(param_name, Parameter.POSITIONAL_OR_KEYWORD, annotation=annotation),
            kwargs | ({} if type is None else {"type": type}) 
        )

    @classmethod
    def outputs_file(cls) -> list[Self]:
        return [
            cls.make("--out", "-o", type=Path, default=None, help="Optional output path.")
        ]

    @classmethod
    def outputs_json(cls) -> list[Self]:
        return [
            cls.make("--minimize", action="store_true", help="Output minimized JSON when generating data.")
        ] + cls.outputs_file()

    @classmethod
    def parses_gamedata(cls) -> list[Self]:
        default = GameVersionRange.from_version(GAME_VERSIONS[0]) if len(GAME_VERSIONS) > 0 else None
        return [
            cls.make(
                "--gamedata", "-g", annotation=GameVersionRange, default=default, nargs="+",
                action=_GamedataAction, help="Game version range to source the data from."
            )
        ]

    @classmethod
    def sources_gamedata(cls) -> list[Self]:
        return [
            cls.make("--game-dir", type=Path, required=True, help="Path to ELDEN RING's \"Game\" directory, where the binary is located."),
            cls.make("--ignore-checksum", action=BooleanOptionalAction, help="Ignore MD5 verification of thirdparty tools."),
            cls.make("--keep-cache", action=BooleanOptionalAction, help="Keep the unpacked files, if any."),
        ]

class _Subcommand(NamedTuple):
    command: str
    summary: str
    aliases: list[str] = []
    arguments: list[_Argument] = []

    @classmethod
    def iterate(cls):
        yield from iter(cls.__subclasses__())

    @classmethod
    def get_parameters(cls) -> list[Parameter]:
        return [arg.param for arg in cls.arguments]

class Generate(_Subcommand):
    command = "generate"
    summary = "Generates JSON data for specified gamedata items."
    aliases = ["gen"]
    arguments = [
        _Argument.make("tables", type=Table, default=[], choices=list(Table), nargs="+", action=_TablesAction, help="Specify any or all tables.")
    ] + _Argument.parses_gamedata() + _Argument.outputs_json()

class FindValues(_Subcommand):
    command = "find-values"
    summary = "Find all possible values of a field per param name."
    aliases = ["vals"]
    arguments = [
        _Argument.make("param", type=str, help="Name of the parameter table, ex. SpEffectParam"),
        _Argument.make("field", type=str, help="Name of the field of the table, ex. slashDamageCutRate"),
        _Argument.make("--limit", "-l", type=int, default=8, metavar="NUM", help="Limit of examples shown for each value (default 8)."),
    ] + _Argument.parses_gamedata()

class CalculateAR(_Subcommand):
    command = "calculate-ar"
    summary = "Calculate attack power of an armament"
    aliases = ["ar"]
    arguments = [
        _Argument.make("attribs", type=str, help="Player attributes in format \"str,dex,int,fth,arc\"."),
        _Argument.make("armament", type=str, help="Name of the armament."),
        _Argument.make("affinity", type=str, help="Affinity of the armament."),
        _Argument.make("level", type=int, help="Upgrade level of the armament."),
        _Argument.make("--data-path", type=Path, required=True, help="Location of the generated data."),
    ]

class Changelog(_Subcommand):
    command = "changelog"
    summary = "Create a changelog of erdb-detectable differences between specified versions."
    aliases = []
    arguments = [
        _Argument.make("version", type=GameVersion.from_string, annotation=GameVersion, help="Version to generate the changelog of."),
        _Argument.make("--from-version", type=GameVersion.from_string, annotation=GameVersion | None, default=None, help="Optional starting version of the changelog, previous if not specified."),
        _Argument.make("--formatter", "-f", type=str, default=FormatterBase.identifiers()[0], choices=FormatterBase.identifiers(), help="Format to output the changelog in."),
    ] + _Argument.outputs_file()

class Source(_Subcommand):
    command = "source"
    summary = "Extract gamedata from an UXM-unpacked Elden Ring installation (Windows only)."
    aliases = []
    arguments = [
        _Argument.make("--version", "-v", type=GameVersion.from_string, annotation=GameVersion | None, default=None, help="Version directory storing the extracted files, overrides autodetection."),
    ] + _Argument.sources_gamedata()

class Map(_Subcommand):
    command = "map"
    summary = "Extract world map image from an UXM-unpacked Elden Ring installation (Windows only)."
    aliases = []
    arguments = [
        _Argument.make("--lod", "-l", type=int, default=0, help="Level of detail of the map, 0 is highest."),
        _Argument.make("--underground", action=BooleanOptionalAction, help="Specifies whether to extract the underground map instead of the overworld."),
    ] + _Argument.sources_gamedata() + _Argument.outputs_file()

class Icons(_Subcommand):
    command = "icons"
    summary = "Extract item images from an UXM-unpacked Elden Ring installation (Windows only)."
    aliases = []
    arguments = [
        _Argument.make("types", type=Table, default=[], nargs="+", choices=_ItemTypesAction.choices(), action=_ItemTypesAction, help="Specify item types to export images for."),
        _Argument.make("--size", "-s", type=int, default=1024, choices=range(1, 1025), metavar="[1-1024]", help="Size in pixels of images to be exported, resized from maximum quality in game files (1024x1024)."),
    ] + _Argument.sources_gamedata() + _Argument.outputs_file()

class ServeAPI(_Subcommand):
    command = "serve-api"
    summary = "Being serving the API web server."
    aliases = ["api"]
    arguments = [
        _Argument.make("--port", "-p", type=int, required=True, help="Port number to listen on."),
        _Argument.make("--bind", "-b", type=str, default="0.0.0.0", help="Address to bind the server on."),
        _Argument.make("--precache", action=BooleanOptionalAction, help="Pregenerate all data instead of lazy loading."),
    ]

def parse_args(argv: Sequence[str], handlers: dict[str, Callable]) -> dict[str, Any]:
    parser = ArgumentParser(description="Interface for ERDB operations.")
    subs = parser.add_subparsers(title="subcommands", required=True)

    for cmd in _Subcommand.iterate():
        assert cmd.command in handlers, f"No handler found for \"{cmd.command}\" subcommand"
        handler = handlers[cmd.command]

        sig = signature(handler)
        assert sig.return_annotation == int, f"Handler for \"{cmd.command}\" must return an int"
        assert cmd.get_parameters() == list(sig.parameters.values()), f"Parameter mismatch for \"{cmd.command}\" handler"

        p = subs.add_parser(cmd.command, help=cmd.summary, aliases=cmd.aliases)

        for arg in cmd.arguments:
            p.add_argument(*arg.names, **arg.kwargs)

        p.set_defaults(handler=handler)

    return vars(parser.parse_args(argv))