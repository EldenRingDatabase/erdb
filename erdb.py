import json
import scripts.config as cfg
from pathlib import Path
from typing import Dict, List, Optional
from jsonschema import validate, RefResolver, ValidationError
from scripts.erdb_args import parse_args
from scripts.find_valid_values import find_valid_values
from scripts.attack_power import CalculatorData, ArmamentCalculator, Attributes
from scripts.game_version import GameVersion, GameVersionRange
from scripts.erdb_generators import ERDBGenerator, ERDBGeneratorBase
from scripts.sourcer import source_gamedata, source_map

cfg.ROOT = Path(__file__).parent.resolve()
cfg.VERSIONS = sorted([GameVersion.from_string(p.name) for p in (cfg.ROOT / "gamedata" / "_Extracted").glob("*") if GameVersion.match_path(p)], reverse=True)

def generate(gen: ERDBGeneratorBase, version: GameVersion, minimize: bool=False) -> None:
    output_file = cfg.ROOT / str(version) / gen.output_file()
    print(f"Output file: {output_file}", flush=True)

    if output_file.exists():
        print(f"Output file exists and will be overridden", flush=True)

    main_iter = gen.main_param_iterator(gen.main_param)
    item_data = {gen.get_key_name(row): gen.construct_object(row) for row in main_iter}

    print(f"Generated {len(item_data)} elements", flush=True)

    item_data_full = {
        gen.element_name(): item_data,
        "$schema": f"../schema/{gen.schema_file()}"
    }

    ok = validate_and_write(output_file, gen.schema_file(), item_data_full, gen.schema_store, minimize)
    assert ok, "Generated schema failed to validate"

    print(f"Validated {len(item_data)} elements", flush=True)

def validate_and_write(file_path: Path, schema_name: str, data: Dict, store: Dict[str, Dict], minimize: bool) -> bool:
    try:
        resolver = RefResolver(base_uri="unused", referrer="unused", store=store)
        validate(data, store[schema_name], resolver=resolver)

    except ValidationError as e:
        readable_path = "/".join(str(part) for part in e.path)
        print(f"Failed to validate \"{readable_path}\": {e.message}", flush=True)
        return False

    finally:
        with open(file_path, mode="w") as f:
            kwargs = {"separators": (",", ":")} if minimize else {"indent": 4}
            json.dump(data, f, **kwargs)

    return True

def iterate_gamedata(gamedata: GameVersionRange) -> GameVersion:
    for version in gamedata.iterate(cfg.VERSIONS):
        (cfg.ROOT / str(version)).mkdir(exist_ok=True)
        yield version

def on_generate(generators: List[ERDBGenerator], gamedata: GameVersionRange, minimize: bool):
    for version in iterate_gamedata(gamedata):
        for gen in generators:
            print(f"\n>>> Generating \"{gen}\" from version {version}", flush=True)
            generate(gen.construct(version), version, minimize)

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

def on_source(game_dir: Path, version: GameVersion, ignore_checksum: bool):
    game_dir = game_dir.resolve()
    print(f"\n>>> Sourcing gamedata from \"{game_dir}\" for version {version}.")

    try:
        source_gamedata(game_dir, version, ignore_checksum)

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

def on_fetch_calc_data(version: str, google_key: str):
    from scripts.fetch_attack_power_data import fetch as fetch_attack_power_data
    fetch_attack_power_data(version, google_key)

def main():
    with open(cfg.ROOT / "latest_version.txt", mode="w") as f:
        f.write(str(cfg.VERSIONS[0]))

    parse_args(on_generate, on_find_values, on_calculate_ar, on_source, on_map, on_fetch_calc_data)

if __name__ == "__main__":
    main()
