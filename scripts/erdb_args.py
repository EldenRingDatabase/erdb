import argparse
import scripts.config as cfg
from pathlib import Path
from typing import List
from scripts.changelog import FormatterBase
from scripts.erdb_generators import GameParam
from scripts.game_version import GameVersion, GameVersionRange

def _parse_all_game_params(game_params: List[GameParam], all_effective_game_params) -> List[GameParam]:
    game_params = set(game_params)

    if GameParam.ALL in game_params:
        game_params.update(all_effective_game_params)
        game_params.remove(GameParam.ALL)

    return list(game_params)

class _GeneratorsAction(argparse.Action):
    def __call__(self, parser, namespace, values: List[GameParam], option_string=None):
        setattr(namespace, self.dest, _parse_all_game_params(values, GameParam))

class _ItemTypesAction(argparse.Action):
    def __call__(self, parser, namespace, values: List[GameParam], option_string=None):
        setattr(namespace, self.dest, _parse_all_game_params(values, _ItemTypesAction.choices()))

    @staticmethod
    def choices() -> List[GameParam]:
        return [gp for gp in GameParam if gp.has_icons]

class _GamedataAction(argparse.Action):
    def __call__(self, parser, namespace, values: List[str], option_string=None):
        setattr(namespace, self.dest, GameVersionRange.from_string(" ".join(values)))

def parse_args(on_generate, on_find_values, on_calculate_ar, on_changelog, on_source, on_map, on_icons, on_fetch_calc_data):
    parser = argparse.ArgumentParser(description="Interface for ERDB operations.")

    outputs_json = argparse.ArgumentParser(add_help=False)
    outputs_json.add_argument("--minimize", action="store_true", help="Output minimized JSON when generating data.")

    sources_data = argparse.ArgumentParser(add_help=False)
    default_gamedata = GameVersionRange.from_version(cfg.VERSIONS[0]) if len(cfg.VERSIONS) > 0 else None
    sources_data.add_argument("--gamedata", "-g", nargs="+", default=default_gamedata, action=_GamedataAction, help="Game version range to source the data from.")

    exports_data = argparse.ArgumentParser(add_help=False)
    exports_data.add_argument("--game-dir", "-g", type=Path, required=True, help="Path to Elden Ring's \"Game\" directory, where the binary is located.")
    exports_data.add_argument("--ignore-checksum", action=argparse.BooleanOptionalAction, help="Ignore MD5 verification of thirdparty tools.")
    exports_data.add_argument("--keep-cache", action=argparse.BooleanOptionalAction, help="Keep the unpacked files, if any.")

    subs = parser.add_subparsers(title="subcommands", required=True)

    gen = subs.add_parser("generate", aliases=["gen"], help="List of items to generate.", parents=[sources_data, outputs_json])
    gen.add_argument("generators", type=GameParam, default=[], choices=list(GameParam), nargs="+", action=_GeneratorsAction, help="Specify any or all generators.")
    gen.set_defaults(func=lambda args: on_generate(args.generators, args.gamedata, args.minimize))

    vals = subs.add_parser("find-values", aliases=["vals"], help="Find all possible values of a field per param name.", parents=[sources_data])
    vals.add_argument("param", type=str, help="Name of the parameter table, ex. SpEffectParam")
    vals.add_argument("field", type=str, help="Name of the field of the table, ex. slashDamageCutRate")
    vals.add_argument("--limit", "-l", type=int, default=8, required=False, help="Limit of examples shown for each value (default 8).", metavar="NUM")
    vals.set_defaults(func=lambda args: on_find_values(args.param, args.field, args.limit, args.gamedata))

    calc = subs.add_parser("calculate-ar", aliases=["ar"], help="Calculate attack power of an armament", parents=[sources_data])
    calc.add_argument("attribs", type=str, help="Player attributes in format \"str,dex,int,fth,arc\".")
    calc.add_argument("armament", type=str, help="Name of the armament.")
    calc.add_argument("affinity", type=str, help="Affinity of the armament.")
    calc.add_argument("level", type=str, help="Upgrade level of the armament.")
    calc.set_defaults(func=lambda args: on_calculate_ar(args.attribs, args.armament, args.affinity, args.level, args.gamedata))

    change = subs.add_parser("changelog", help="Create a changelog of erdb-detectable differences between specified versions.")
    change.add_argument("version", type=GameVersion.from_string, help="Version to generate the changelog of.")
    change.add_argument("--out", "-o", type=Path, default=None, help="Output path where changes should be written to, stdout if not specified.")
    change.add_argument("--formatter", "-f", type=str, default=FormatterBase.identifiers()[0], choices=FormatterBase.identifiers(), help="Format to output the changelog in.")
    change.add_argument("--from-version", type=GameVersion.from_string, default=None, help="Optional starting version of the changelog, previous if not specified.")
    change.set_defaults(func=lambda args: on_changelog(args.version, args.out, args.formatter, args.from_version))

    source = subs.add_parser("source", help="Extract gamedata from an UXM-unpacked Elden Ring installation (Windows only)", parents=[exports_data])
    source.add_argument("--version", "-v", type=GameVersion.from_string, required=True, help="Version to create from the extracted files.")
    source.set_defaults(func=lambda args: on_source(args.game_dir, args.version, args.ignore_checksum))

    pmap = subs.add_parser("map", help="Extract world map image from an UXM-unpacked Elden Ring installation (Windows only)", parents=[exports_data])
    pmap.add_argument("--out", "-o", type=Path, default=None, help="Output path where the file should be written to. If not specified, the map will be shown in a window. Use file extension to specify the image format. If a directory is provided, a JPEG file will be created with a default name. Parent directories will be created automatically.")
    pmap.add_argument("--lod", "-l", type=int, default=0, help="Level of detail of the map, 0 is highest.")
    pmap.add_argument("--underground", action=argparse.BooleanOptionalAction, help="Specifies whether to extract the underground map instead of the overworld.")
    pmap.set_defaults(func=lambda args: on_map(args.game_dir, args.out, args.lod, args.underground, args.ignore_checksum, args.keep_cache))

    icons = subs.add_parser("icons", help="Extract item images from an UXM-unpacked Elden Ring installation (Windows only)", parents=[exports_data])
    icons.add_argument("types", type=GameParam, default=[GameParam.ALL], choices=_ItemTypesAction.choices(), nargs="+", action=_ItemTypesAction, help="Specify item types to export images for.")
    icons.add_argument("--size", "-s", type=int, default=1024, choices=range(1, 1025), metavar="[1-1024]", help="Size in pixels of images to be exported, resized from maximum quality in game files (1024x1024).")
    icons.add_argument("--destination", "-d", type=Path, default=Path.cwd, help="Directory where the images should be exported to. If not specified, current working directory is used. Parent directories will be created automatically.")
    icons.set_defaults(func=lambda args: on_icons(args.game_dir, args.types, args.size, args.destination, args.ignore_checksum, args.keep_cache))

    fetch_data = subs.add_parser("fetch-calc-data", help="Fetch calculator test data from an online calculator.")
    fetch_data.add_argument("google_key", type=str, help="Path to JSON key from the service account with access to a Google Sheet calculator.")
    fetch_data.add_argument("--version", "-v", type=str, default=str(cfg.VERSIONS[0]) if len(cfg.VERSIONS) > 0 else "unknown", help="Game version to fetch the data from, used in finding Sheet name.")
    fetch_data.set_defaults(func=lambda args: on_fetch_calc_data(args.version, args.google_key))

    args = parser.parse_args()
    args.func(args)
