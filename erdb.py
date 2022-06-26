import argparse
import json
import scripts.config as cfg
from pathlib import Path
from typing import Dict, List, NamedTuple
from jsonschema import validate, RefResolver, ValidationError
from scripts.find_valid_values import find_valid_values
from scripts.attack_power import CalculatorData, ArmamentCalculator, Attributes
from scripts.game_version import GameVersion, GameVersionRange
from scripts.erdb_generators import ERDBGenerator, ERDBGeneratorBase

cfg.ROOT = Path(__file__).parent.resolve()
cfg.VERSIONS = sorted([GameVersion.from_string(p.name) for p in (cfg.ROOT / "gamedata" / "_Extracted").glob("*") if GameVersion.match_path(p)], reverse=True)

class ErdbArgs(NamedTuple):
    generators: List[ERDBGenerator]
    minimize_json: bool
    find_values: str
    find_values_limit: int
    gamedata: GameVersionRange
    calc_ar: List[str]

    @classmethod
    def from_args(cls, args) -> "ErdbArgs":
        generators = set(args.generate)

        if ERDBGenerator.ALL in generators:
            generators.update(ERDBGenerator)
            generators.remove(ERDBGenerator.ALL)

        gamedata = \
            GameVersionRange.from_version(cfg.VERSIONS[0]) \
            if args.gamedata is None else \
            GameVersionRange.from_string(" ".join(args.gamedata))

        return cls(generators, args.minimize_json, args.find_values, args.find_values_limit, gamedata, args.calc_ar)

    @classmethod
    def create(cls) -> "ErdbArgs":
        parser = argparse.ArgumentParser(description="Interface for ERDB operations.")
        parser.add_argument("--generate", "-g", type=ERDBGenerator, default=[], choices=list(ERDBGenerator), nargs="+", help="The type of items to generate.")
        parser.add_argument("--minimize-json", action="store_true", help="Ouput minimized JSON when generating data.")
        parser.add_argument("--find-values", "-f", type=str, help="Find all possible values of a field per param name, format: ParamName:FieldName.")
        parser.add_argument("--find-values-limit", type=int, default=-1, help="Limit find-values examples to X per value.")
        parser.add_argument("--gamedata", type=str, nargs="+", action="extend", help="Game version range to source the data from.")
        parser.add_argument("--calc-ar", type=str, nargs=4, help="Calculate attack power for weapons, format: s,d,i,f,a armament affinity level")
        return cls.from_args(parser.parse_args())

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

def main():
    args = ErdbArgs.create()

    with open(cfg.ROOT / "latest_version.txt", mode="w") as f:
        f.write(str(cfg.VERSIONS[0]))

    for version in args.gamedata.iterate(cfg.VERSIONS):
        (cfg.ROOT / str(version)).mkdir(exist_ok=True)

        for gen in args.generators:
            print(f"\n>>> Generating \"{gen}\" from version {version}", flush=True)
            generate(gen.construct(version), version, args.minimize_json)

        if args.find_values:
            parts = args.find_values.split(":")
            assert len(parts) == 2, "Incorrect find-values format"
            find_valid_values(parts[0], version, parts[1], args.find_values_limit)

        if args.calc_ar:
            attribs, armament, affinity, level = args.calc_ar

            calculator_data     = CalculatorData.create(cfg.ROOT / str(version))
            armament_calculator = ArmamentCalculator(calculator_data, armament, affinity, level)
            player_attributes   = Attributes.from_string(attribs)

            for attack_type, value in armament_calculator.attack_power(player_attributes).items():
                print(f"{attack_type}: {value.base} +{value.scaling} ({value.total})")

            for effect_type, value in armament_calculator.status_effects(player_attributes).items():
                print(f"{effect_type}: {value.base} +{value.scaling} ({value.total})")

if __name__ == "__main__":
    main()