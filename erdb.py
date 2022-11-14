import json
import scripts.config as cfg
from pathlib import Path
from typing import Dict, List, Optional
from jsonschema import validate, RefResolver, ValidationError
from scripts.directus_client import DirectusClient
from scripts.erdb_args import parse_args
from scripts.find_valid_values import find_valid_values
from scripts.attack_power import CalculatorData, ArmamentCalculator, Attributes
from scripts.game_version import GameVersion, GameVersionRange
from scripts.erdb_generators import GameParam
from scripts.sourcer import source_gamedata, source_map, source_icons
from scripts.changelog import generate as generate_changelog

cfg.ROOT = Path(__file__).parent.resolve()
cfg.VERSIONS = sorted([GameVersion.from_string(p.stem) for p in (cfg.ROOT / "gamedata" / "_Extracted").glob("*zip")], reverse=True)

def validate_and_write(file_path: Path, schema_name: str, data: Dict, store: Dict[str, Dict], minimize: bool) -> bool:
    try:
        resolver = RefResolver(base_uri="unused", referrer="unused", store=store)
        validate(data, store[schema_name], resolver=resolver)

    except ValidationError as e:
        readable_path = "/".join(str(part) for part in e.path)
        print(f"Failed to validate \"{readable_path}\": {e.message}", flush=True)
        return False

    finally:
        with open(file_path, mode="w", encoding="utf-8") as f:
            kwargs = {"separators": (",", ":")} if minimize else {"indent": 4}
            json.dump(data, f, ensure_ascii=False, **kwargs)

    return True

def iterate_gamedata(gamedata: GameVersionRange) -> GameVersion:
    for version in gamedata.iterate(cfg.VERSIONS):
        (cfg.ROOT / str(version)).mkdir(exist_ok=True)
        yield version

def on_generate(game_params: List[GameParam], gamedata: GameVersionRange, minimize: bool):
    for version in iterate_gamedata(gamedata):
        for generator in (gp.generator(version) for gp in game_params):
            print(f"\n>>> Generating \"{generator.element_name()}\" from version {version}", flush=True)

            output_file = cfg.ROOT / str(version) / generator.output_file()
            print(f"Output file: {output_file}", flush=True)

            if output_file.exists():
                print(f"Output file exists and will be overridden", flush=True)

            data = generator.generate()
            count = len(data)

            data = {
                generator.element_name(): data,
                "$schema": f"../schema/{generator.schema_file()}"
            }

            print(f"Generated {count} elements", flush=True)

            ok = validate_and_write(output_file, generator.schema_file(), data, generator.schema_store, minimize)
            assert ok, "Generated schema failed to validate"

            print(f"Validated {count} elements", flush=True)

def on_replicate(gamedata: GameVersionRange, endpoint: str, token: str):
    directus = DirectusClient(endpoint, token)

    for version in iterate_gamedata(gamedata):
        for game_param in GameParam.ALL.effective():
            generator = game_param.generator(version)
            directus.update_collection(game_param, generator.top_level_properties())
            directus.import_data(game_param, generator.generate())

        return # TODO: support multiple game versions in one API

def on_find_values(param: str, field: str, limit: int, gamedata: GameVersionRange):
    for version in iterate_gamedata(gamedata):
        print(f"\n>>> Finding values for version {version}")
        find_valid_values(param, version, field, limit)

def on_calculate_ar(attribs: str, armament: str, affinity: str, level: str, gamedata: GameVersionRange):
    for version in iterate_gamedata(gamedata):
        print(f"\n>>> Calculating AR for {affinity} {armament} +{level} at {attribs} for version {version}")

        data = CalculatorData.create(cfg.ROOT / str(version))
        calc = ArmamentCalculator(data, armament, affinity, level)
        attr = Attributes.from_string(attribs)

        for attack_type, value in calc.attack_power(attr).items():
            print(f"{attack_type}: {value.base} +{value.scaling} ({value.total})")

        for effect_type, value in calc.status_effects(attr).items():
            print(f"{effect_type}: {value.base} +{value.scaling} ({value.total})")

def on_changelog(version: GameVersion, out: Optional[Path], formatter_id: str, from_version: Optional[GameVersion]):
    assert version in cfg.VERSIONS, f"No {version} version found"
    assert from_version is None or from_version in cfg.VERSIONS, f"No {from_version} version found"

    if out is not None:
        out = out.resolve()

    if from_version is None:
        prev_id = cfg.VERSIONS.index(version) + 1
        assert prev_id < len(cfg.VERSIONS), f"No version found before {version}"

        from_version = cfg.VERSIONS[prev_id]

    generate_changelog(from_version, version, out, formatter_id)

def on_source(game_dir: Path, ignore_checksum: bool, version: Optional[GameVersion]):
    game_dir = game_dir.resolve()
    print(f"\n>>> Sourcing gamedata from \"{game_dir}\".")

    try:
        source_gamedata(game_dir, ignore_checksum, version)

    except AssertionError as e:
        print("Sourcing gamedata failed:", *e.args)

def on_map(game_dir: Path, out: Optional[Path], lod: int, underground: bool, ignore_checksum: bool, keep_cache: bool):
    game_dir = game_dir.resolve()

    if out is not None:
        out = out.resolve()

    print(f"\n>>> Extracting map from \"{game_dir}\".")

    try:
        source_map(game_dir, out, lod, underground, ignore_checksum, keep_cache)

    except AssertionError as e:
        print("Sourcing map failed:", *e.args)

def on_icons(game_dir: Path, game_params: List[GameParam], size: int, destination: Path, ignore_checksum: bool, keep_cache: bool):
    game_dir = game_dir.resolve()
    destination = destination.resolve()

    print(f"\n>>> Extracting {', '.join(map(str, game_params))} icons from \"{game_dir}\".")

    try:
        source_icons(game_dir, game_params, size, destination, ignore_checksum, keep_cache)

    except AssertionError as e:
        print("Sourcing icons failed:", *e.args)

def on_fetch_calc_data(version: str, google_key: str):
    from scripts.fetch_attack_power_data import fetch as fetch_attack_power_data
    fetch_attack_power_data(version, google_key)

def main():
    if len(cfg.VERSIONS) > 0:
        with open(cfg.ROOT / "latest_version.txt", mode="w") as f:
            f.write(str(cfg.VERSIONS[0]))

    parse_args(on_generate, on_replicate, on_find_values, on_calculate_ar, on_changelog, on_source, on_map, on_icons, on_fetch_calc_data)

if __name__ == "__main__":
    main()
