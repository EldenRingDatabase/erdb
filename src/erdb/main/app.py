import json
from pathlib import Path
from typing import Sequence

from erdb.main.args import parse_args
from erdb.table import Table
from erdb.loaders import GAME_VERSIONS
from erdb.app_api.main import serve as serve_app_api
from erdb.utils.attack_power import Attributes, CalculatorData, ArmamentCalculator
from erdb.utils.changelog import generate as generate_changelog
from erdb.utils.find_valid_values import find_valid_values
from erdb.utils.sourcer import source_gamedata, source_map, source_icons
from erdb.utils.common import pydantic_encoder_no_nulls
from erdb.typing.game_version import GameVersion, GameVersionRange


class App:
    args: dict

    def __init__(self, argv: Sequence[str]) -> None:
        self.args = parse_args(argv, handlers={
            "generate": self.generate,
            "find-values": self.find_values,
            "calculate-ar": self.calculate_ar,
            "changelog": self.changelog,
            "source": self.source,
            "map": self.source_map,
            "icons": self.source_icons,
            "serve-api": self.serve_api,
        })

    def run(self) -> int:
        handler = self.args.pop("handler")
        return handler(**self.args)

    @staticmethod
    def generate(tables: list[Table], gamedata: GameVersionRange, minimize: bool, out: Path | None) -> int:
        if out is None:
            out = Path.cwd()
        else:
            out = out.resolve()

        for version in gamedata.iterate(GAME_VERSIONS):
            destination = out / str(version)
            destination.mkdir(parents=True, exist_ok=True)

            for tb, gen in ((tb, tb.make_generator(version)) for tb in tables):
                print(f"\n>>> Generating \"{tb}\" from version {version}", flush=True)

                output_file = destination / f"{tb}.json"
                print(f"Output file: {output_file}", flush=True)

                if output_file.exists():
                    print(f"Output file exists and will be overridden", flush=True)

                data = gen.generate()
                print(f"Generated {len(data)} elements", flush=True)

                with open(output_file, mode="w", encoding="utf-8") as f:
                    kwargs = {"separators": (",", ":")} if minimize else {"indent": 4}
                    json.dump(data, f, ensure_ascii=False, default=pydantic_encoder_no_nulls, allow_nan=False, **kwargs)

        return 0

    @staticmethod
    def find_values(param: str, field: str, limit: int, gamedata: GameVersionRange) -> int:
        for game_version in gamedata.iterate(GAME_VERSIONS):
            print(f"\n>>> Finding values for version {game_version}")
            find_valid_values(param, str(game_version), field, limit)

        return 0

    @staticmethod
    def calculate_ar(attribs: str, armament: str, affinity: str, level: int, data_path: Path) -> int:
        print(f"\n>>> Calculating AR for {affinity} {armament} +{level} at {attribs}")

        data = CalculatorData.create(data_path)
        calc = ArmamentCalculator(data, armament, affinity, level)
        attr = Attributes.from_string(attribs)

        for attack_type, value in calc.attack_power(attr).items():
            print(f"{attack_type}: {value.base} +{value.scaling} ({value.total})")

        for effect_type, value in calc.status_effects(attr).items():
            print(f"{effect_type}: {value.base} +{value.scaling} ({value.total})")

        return 0

    @staticmethod
    def changelog(version: GameVersion, from_version: GameVersion | None, formatter: str, out: Path | None) -> int:
        assert version in GAME_VERSIONS, f"No {version} version found"
        assert from_version is None or from_version in GAME_VERSIONS, f"No {from_version} version found"

        if out is not None:
            out = out.resolve()

        if from_version is None:
            prev_id = GAME_VERSIONS.index(version) + 1
            assert prev_id < len(GAME_VERSIONS), f"No version found before {version}"

            from_version = GAME_VERSIONS[prev_id]

        generate_changelog(from_version, version, out, formatter)
        return 0

    @staticmethod
    def source(version: GameVersion | None, game_dir: Path, ignore_checksum: bool, keep_cache: bool) -> int:
        game_dir = game_dir.resolve()

        print(f"\n>>> Sourcing gamedata from \"{game_dir}\".")

        try:
            source_gamedata(game_dir, ignore_checksum, version)

        except AssertionError as e:
            print("Sourcing gamedata failed:", *e.args)
            return 1

        return 0

    @staticmethod
    def source_map(lod: int, underground: bool, game_dir: Path, ignore_checksum: bool, keep_cache: bool, out: Path | None) -> int:
        game_dir = game_dir.resolve()

        if out is not None:
            out = out.resolve()

        print(f"\n>>> Extracting map from \"{game_dir}\".")

        try:
            source_map(game_dir, out, lod, underground, ignore_checksum, keep_cache)

        except AssertionError as e:
            print("Sourcing map failed:", *e.args)
            return 1

        return 0

    @staticmethod
    def source_icons(types: list[Table], size: int, game_dir: Path, ignore_checksum: bool, keep_cache: bool, out: Path | None) -> int:
        game_dir = game_dir.resolve()

        if out is None:
            out = Path.cwd()
        else:
            out = out.resolve()

        print(f"\n>>> Extracting {', '.join(map(str, types))} icons from \"{game_dir}\".")

        try:
            source_icons(game_dir, types, size, out, ignore_checksum, keep_cache)

        except AssertionError as e:
            print("Sourcing icons failed:", *e.args)
            return 1

        return 0

    @staticmethod
    def serve_api(port: int, bind: str, precache: bool) -> int:
        serve_app_api(port, bind=bind, precache=precache)
        return 0