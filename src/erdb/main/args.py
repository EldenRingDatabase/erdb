from inspect import Parameter, signature
from argparse import ArgumentParser, BooleanOptionalAction, Action, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Any, Callable, NamedTuple, Sequence, Self
from textwrap import wrap, dedent

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
    details: str
    aliases: list[str] = []
    examples: list[tuple[str, str]] = []
    arguments: list[_Argument] = []

    @classmethod
    def iterate(cls):
        yield from iter(cls.__subclasses__())

    @classmethod
    def get_parameters(cls) -> list[Parameter]:
        return [arg.param for arg in cls.arguments]

    @classmethod
    def get_description(cls) -> str:
        return "\n".join(wrap(dedent(cls.details), break_on_hyphens=False))

    @classmethod
    def get_epilog(cls) -> str:
        to_str = lambda x: f"[EXAMPLE] {x[0]}\n$ {x[1]}"
        return "\n\n".join(map(to_str, cls.examples))

class Generate(_Subcommand):
    command = "generate"
    summary = "Generate JSON data for specified tables."
    details = """\
    Parse extracted gamedata into a well-structured JSON output.
    The resulting data will be written to `{table}.json` files in a folder named after the `--out` argument, or cwd if not provided.
    This is a manual way of generating data, many other subcommands do this automatically.
    """

    aliases = ["gen"]

    examples = [
        (
            "Generate Armor data only for version 1.07.0",
            "erdb gen armor --gamedata only 1.07.0",
        ),
        (
            "Generate Talisman and Tool data for versions between 1.04.1 and 1.07.1 (including)",
            "erdb gen talismans tools --gamedata from 1.04.1 until 1.07.1",
        ),
        (
            "Generate all data for all versions from 1.06.0 (including), minimize the JSON output",
            "erdb gen all --gamedata until 1.06.0 --minimize",
        ),
    ]

    arguments = [
        _Argument.make("tables", type=Table, default=[], choices=list(Table), nargs="+", action=_TablesAction, help="Specify any or all tables.")
    ] + _Argument.parses_gamedata() + _Argument.outputs_json()

class FindValues(_Subcommand):
    command = "find-values"
    summary = "Find all possible values of a field per param name."
    details = """\
    Search for all possible values of a particular property in the specified game param.
    Unique values will be listed on each line, with example item/row names, or only their IDs if the name is blank.
    Useful for figuring out which properties are important and how the rows are grouped in relation to them.
    """

    aliases = ["vals"]

    examples = [
        (
            "Show unique values for \"sortGroupId\" property of \"EquipParamGoods\"",
            "erdb vals EquipParamGoods sortGroupId",
        ),
        (
            "Show weapon categories in \"EquipParamWeapon\", with up to 20 examples per category",
            "erdb vals EquipParamWeapon weaponCategory --limit 20",
        ),
    ]

    arguments = [
        _Argument.make("param", type=str, help="Name of the parameter table, ex. SpEffectParam"),
        _Argument.make("field", type=str, help="Name of the field of the table, ex. slashDamageCutRate"),
        _Argument.make("--limit", "-l", type=int, default=8, metavar="NUM", help="Limit of examples shown for each value (default 8)."),
    ] + _Argument.parses_gamedata()

class CalculateAR(_Subcommand):
    command = "calculate-ar"
    summary = "Calculate attack power of an armament"
    details = """\
    Calculate attack power and status effects of an armament of any affinity or level combination using the generated data.
    Provide the path to the data output directory from `erdb generate` via `--data-path`.
    Somber weapon levels are as-is, you must know the maximum level of the given weapon or wether the affinity is interchangable.
    Providing a level higher than maxiumum or an invalid affinity will result in an error.
    """

    aliases = ["ar"]

    examples = [
        (
            "Get AR and status effects for Poison Claymore +25 at 25 str, 30 dex, 10 int, 10 fth, 20 arc",
            "erdb ar 25,30,10,10,20 Claymore Poison 25 --data-path /path/to/generated/data/1.07.1/",
        ),
        (
            "Get AR for Standard Axe of Godfrey +8 at 50 str, 20 dex, 10 int, 10 fth, 10 arc",
            "erdb ar 50,20,10,10,10 \"Axe of Godfrey\" Standard 8 --data-path ./1.06.0",
        ),
    ]

    arguments = [
        _Argument.make("attribs", type=str, help="Player attributes in format \"str,dex,int,fth,arc\"."),
        _Argument.make("armament", type=str, help="Name of the armament."),
        _Argument.make("affinity", type=str, help="Affinity of the armament."),
        _Argument.make("level", type=int, help="Upgrade level of the armament."),
        _Argument.make("--data-path", type=Path, required=True, help="Location of the generated data."),
    ]

class Changelog(_Subcommand):
    command = "changelog"
    summary = "Create a changelog of ERDB-detectable differences between specified versions."
    details = """\
    Compare two generated data and create a human-readable list of updates.
    ERDB automatically finds the previous version from the one requested, but that can be overridden with an optional `--from-version` argument.
    Different formatters are available, using which the output will be written to stdout, or a specific file if `--out` is provided.
    """

    aliases = []

    examples = [
        (
            "Generate changelog from version 1.06.0 to 1.07.0 and write it to CHANGELOG.md using markdown format",
            "erdb changelog 1.07.0 --formatter markdown --out CHANGELOG.md",
        ),
        (
            "Print changelog from version 1.05.0 to 1.07.1 in a text format to stdout",
            "erdb changelog 1.07.1 --from-version 1.05.0 --formatter text",
        ),
    ]

    arguments = [
        _Argument.make("version", type=GameVersion.from_string, annotation=GameVersion, help="Version to generate the changelog of."),
        _Argument.make("--from-version", type=GameVersion.from_string, annotation=GameVersion | None, default=None, help="Optional starting version of the changelog, previous if not specified."),
        _Argument.make("--formatter", "-f", type=str, default=FormatterBase.identifiers()[0], choices=FormatterBase.identifiers(), help="Format to output the changelog in."),
    ] + _Argument.outputs_file()

class Source(_Subcommand):
    command = "source"
    summary = "Extract gamedata from an UXM-unpacked ELDEN RING installation (Windows only)."
    details = """\
    Parse an UXM-unpacked installation of ELDEN RING and collect data to ERDB package resources.
    In order to extract the files beyond UXM, third-party tools will be downloaded, verified and executed.
    The version of the game is automatically detected but can be overridden for any purpose, ex. modded version.
    This version can then be used in other ERDB subcommands, like generating tables or calculating AR.
    """

    aliases = []

    examples = [
        (
            "Source a game folder and autodetect its version",
            "erdb source --game-dir \"/path/to/ELDEN RING/Game\"",
        ),
        (
            "Source a game folder, specifying custom version and keep whatever was additionally extracted",
            "erdb source --game-dir \"/path/to/ELDEN RING/Game\" --keep-cache --version 1.99.0",
        ),
    ]

    arguments = [
        _Argument.make("--version", "-v", type=GameVersion.from_string, annotation=GameVersion | None, default=None, help="Version directory storing the extracted files, overrides autodetection."),
    ] + _Argument.sources_gamedata()

class Map(_Subcommand):
    command = "map"
    summary = "Extract world map image from an UXM-unpacked ELDEN RING installation (Windows only)."
    details = """\
    Parse an UXM-unpacked installation of ELDEN RING and extract the world map tiles.
    Tiles are combined into an image and written to the specified file or directory using the `--out` argument.
    Provide a file extension to automatically convert it to that format.
    """

    aliases = []

    examples = [
        (
            "Write the full quality map to er_map.jpeg",
            "erdb map --game-dir \"/path/to/ELDEN RING/Game\" -o er_map.jpeg",
        ),
        (
            "Write the LOD 2 quality map of underground to a default filename and extension",
            "erdb map --game-dir \"/path/to/ELDEN RING/Game\" --lod 2 --underground",
        ),
    ]

    arguments = [
        _Argument.make("--lod", "-l", type=int, default=0, help="Level of detail of the map, 0 is highest."),
        _Argument.make("--underground", action=BooleanOptionalAction, help="Specifies whether to extract the underground map instead of the overworld."),
    ] + _Argument.sources_gamedata() + _Argument.outputs_file()

class Icons(_Subcommand):
    command = "icons"
    summary = "Extract item images from an UXM-unpacked ELDEN RING installation (Windows only)."
    details = """\
    Parse an UXM-unpacked installation of ELDEN RING and extract the item icons.
    Accepts list of tables similar to `erdb generate` but only ones that actually are in-game items.
    Item icons are output in directories with the same name as their respective table, parented by the `--out` argument, or cwd if not provided.
    `--file-format` can be used to name them in a custom way and provide a specific extension to automatically format images to.
    """

    aliases = []

    examples = [
        (
            "Extract icons for tools and keys in specific file names and as ICO format",
            "erdb icons tools keys --game-dir \"/path/to/ELDEN RING/Game\" --file-format \"{icon_id} - {name}.ico\"",
        ),
        (
            "Extract all icons in a small file size",
            "erdb icons all --game-dir \"/path/to/ELDEN RING/Game\" --size 128",
        ),
    ]

    arguments = [
        _Argument.make("types", type=Table, default=[], nargs="+", choices=_ItemTypesAction.choices(), action=_ItemTypesAction, help="Specify item types to export images for."),
        _Argument.make("--size", "-s", type=int, default=1024, choices=range(1, 1025), metavar="[1-1024]", help="Size in pixels of images to be exported, resized from maximum quality in game files (1024x1024)."),
        _Argument.make("--file-format", "-f", type=str, default="{icon_id}.png", help="Specify the formatting for file names, including extension. Available fields: {icon_id}, {name}, {table}. NOTE: multiple items can share {icon_id}, therefore {name} alone is not exhaustive and only one will be used."),
    ] + _Argument.sources_gamedata() + _Argument.outputs_file()

class ServeAPI(_Subcommand):
    command = "serve-api"
    summary = "Begin serving the API web server."
    details = """\
    Start a web server providing a REST API for every table and for all available game versions.
    Data is served from memory, and is generated lazily unless `--precache` is provided.
    The full documentation is available under `/v{api_version}/docs` or `/v{api_version}/redoc` endpoints.
    Higher level endpoints, `/docs` and `/redoc` outline all API versions there are thus far.
    """

    aliases = ["api"]

    examples = [
        (
            "Serve the REST API on port 8080 and pracache all the tables",
            "erdb serve-api --port 8080 --precache",
        ),
    ]

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

        p = subs.add_parser(cmd.command, help=cmd.summary, description=cmd.get_description(), aliases=cmd.aliases, epilog=cmd.get_epilog(), formatter_class=RawDescriptionHelpFormatter)

        for arg in cmd.arguments:
            p.add_argument(*arg.names, **arg.kwargs)

        p.set_defaults(handler=handler)

    return vars(parser.parse_args(argv))