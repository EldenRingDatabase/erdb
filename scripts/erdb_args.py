import argparse
import scripts.config as cfg
from pathlib import Path
from typing import List
from scripts.erdb_generators import ERDBGenerator
from scripts.game_version import GameVersion, GameVersionRange

class _GeneratorsAction(argparse.Action):
    def __call__(self, parser, namespace, values: List[ERDBGenerator], option_string=None):
        generators = set(values)

        if ERDBGenerator.ALL in generators:
            generators.update(ERDBGenerator)
            generators.remove(ERDBGenerator.ALL)

        setattr(namespace, self.dest, list(generators))

class _GamedataAction(argparse.Action):
    def __call__(self, parser, namespace, values: List[str], option_string=None):
        setattr(namespace, self.dest, GameVersionRange.from_string(" ".join(values)))

def parse_args(on_generate, on_find_values, on_calculate_ar, on_source, on_fetch_calc_data):
    parser = argparse.ArgumentParser(description="Interface for ERDB operations.")

    outputs_json = argparse.ArgumentParser(add_help=False)
    outputs_json.add_argument("--minimize", action="store_true", help="Output minimized JSON when generating data.")

    sources_data = argparse.ArgumentParser(add_help=False)
    default_gamedata = GameVersionRange.from_version(cfg.VERSIONS[0])
    sources_data.add_argument("--gamedata", "-g", nargs="+", default=default_gamedata, action=_GamedataAction, help="Game version range to source the data from.")

    subs = parser.add_subparsers(title="subcommands", required=True)

    gen = subs.add_parser("generate", aliases=["gen"], help="List of items to generate.", parents=[sources_data, outputs_json])
    gen.add_argument("generators", type=ERDBGenerator, default=[], choices=list(ERDBGenerator), nargs="+", action=_GeneratorsAction, help="Specify any or all generators.")
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

    source = subs.add_parser("source", help="Extract gamedata from an UXM-unpacked Elden Ring installation (Windows only)")
    source.add_argument("--game-dir", "-g", type=Path, required=True, help="Path to Elden Ring's \"Game\" directory, where the binary is located.")
    source.add_argument("--version", "-v", type=GameVersion.from_string, required=True, help="Version to create from the extracted files.")
    source.add_argument("--ignore-checksum", action=argparse.BooleanOptionalAction, help="Ignore MD5 verification of thirdparty tools.")
    source.set_defaults(func=lambda args: on_source(args.game_dir, args.version, args.ignore_checksum))

    fetch_data = subs.add_parser("fetch-calc-data", help="Fetch calculator test data from an online calculator.")
    fetch_data.add_argument("google_key", type=str, help="Path to JSON key from the service account with access to a Google Sheet calculator.")
    fetch_data.add_argument("--version", "-v", type=str, default=str(cfg.VERSIONS[0]), help="Game version to fetch the data from, used in finding Sheet name.")
    fetch_data.set_defaults(func=lambda args: on_fetch_calc_data(args.version, args.google_key))

    args = parser.parse_args()
    args.func(args)
