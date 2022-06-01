import argparse
import pathlib
import re
import json
from enum import Enum
from typing import Dict, List, NamedTuple
from jsonschema import validate, RefResolver, ValidationError
from scripts.erdb_common import GeneratorDataBase, patch_keys, update_nested
from scripts.find_valid_values import find_valid_values
from scripts.generate_armor import ArmorGeneratorData
from scripts.generate_spirit_ashes import SpiritAshGeneratorData
from scripts.generate_talismans import TalismanGeneratorData
from scripts.generate_ashes_of_war import AshOfWarGeneratorData

class Version(NamedTuple):
    major: str
    minor: str
    patch: str
    nums: List[int]

    @classmethod
    def from_string(cls: "Version", version: str) -> "Version":
        parts = version.split(".")
        assert len(parts) == 3, "Invalid version string given"
        nums = [int(parts[0]), int(parts[1]), int(parts[2])]
        return cls(parts[0], parts[1], parts[2], nums)

    @staticmethod
    def match_path(path: pathlib.Path) -> bool:
        return re.search(r"^[0-9\.]+$", path.name)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Version):
            return False
        return self.major == __o.major and self.minor == __o.minor and self.patch == __o.patch

    def __lt__(self, __o: "Version") -> bool:
        for this_num, other_num in zip(self.nums, __o.nums):
            if this_num != other_num:
                return this_num < other_num
        return False

class Generator(Enum):
    ALL = "all"
    ARMOR = "armor"
    SPIRIT_ASHES = "spirit-ashes"
    TALISMANS = "talismans"
    ASHES_OF_WAR = "ashes-of-war"

    def __str__(self):
        return self.value

_ROOT: pathlib.Path = pathlib.Path(__file__).parent.resolve()
_VERSION_DIRS: List[Version] = sorted([Version.from_string(p.name) for p in (_ROOT / "source").glob("*") if Version.match_path(p)], reverse=True)

_GENERATORS: Dict[Generator, GeneratorDataBase] = {
    Generator.ARMOR: ArmorGeneratorData,
    Generator.SPIRIT_ASHES: SpiritAshGeneratorData,
    Generator.TALISMANS: TalismanGeneratorData,
    Generator.ASHES_OF_WAR: AshOfWarGeneratorData,
}

def get_args():
    parser = argparse.ArgumentParser(description="Interface for ERDB operations.")
    parser.add_argument("--generate", "-g", type=Generator, default=[], choices=list(Generator), nargs="+", help="The type of items to generate.")
    parser.add_argument("--find-values", "-f", type=str, help="Find all possible values of a field per param name, format: ParamName:FieldName.")
    parser.add_argument("--find-values-limit", type=int, default=-1, help="Limit find-values examples to X per value.")
    parser.add_argument("--source-version", "-s", type=Version.from_string, default=_VERSION_DIRS[0], choices=_VERSION_DIRS, help="Game version to source the data from.")
    return parser.parse_args()

def get_generators(args) -> List[Generator]:
    generators = set(args.generate)

    if Generator.ALL in generators:
        generators.update(Generator)
        generators.remove(Generator.ALL)

    return list(generators)

def generate(gendata: GeneratorDataBase, version: Version) -> None:
    output_file = _ROOT / str(version) / gendata.output_file
    print(f"Output file: {output_file}", flush=True)

    if output_file.exists():
        with open(output_file, mode="r") as f:
            item_data_full = json.load(f)
        print(f"Loaded output file", flush=True)
    else:
        item_data_full = {gendata.element_name: {}}
        print(f"Output file does not exist and will be created", flush=True)
    
    item_data_full["$schema"] = f"../schema/{gendata.schema_file}"
    item_data = item_data_full[gendata.element_name]
    print(f"Collected existing data with {len(item_data)} elements", flush=True)

    for row in gendata.main_param_iterator(gendata.main_param):
        new_obj = gendata.construct_object(row)
        cur_obj = item_data.get(row.name, {})

        update_nested(cur_obj, new_obj)
        item_data[row.name] = patch_keys(cur_obj, gendata.schema_properties)

    print(f"Generated {len(item_data)} elements", flush=True)

    item_data_full[gendata.element_name] = item_data
    ok = validate_and_write(output_file, gendata.schema_file, item_data_full, gendata.schema_store)
    assert ok, "Generated schema failed to validate"

    print(f"Validated {len(item_data)} elements", flush=True)

def validate_and_write(file_path: str, schema_name: str, data: Dict, store: Dict[str, Dict]) -> bool:
    try:
        resolver = RefResolver(base_uri="unused", referrer="unused", store=store)
        validate(data, store[schema_name], resolver=resolver)

    except ValidationError as e:
        readable_path = "/".join(str(part) for part in e.path)
        print(f"Failed to validate \"{readable_path}\": {e.message}", flush=True)
        return False

    finally:
        with open(file_path, mode="w") as f:
            json.dump(data, f, indent=4, sort_keys=True)

    return True

def main():
    args = get_args()

    with open("latest_version.txt", mode="w") as f:
        f.write(str(_VERSION_DIRS[0]))

    (_ROOT / str(args.source_version)).mkdir(exist_ok=True)

    for gen in get_generators(args):
        print(f"\n>>> Generating \"{gen}\" from version {args.source_version}", flush=True)
        gendata = _GENERATORS[gen].construct(str(args.source_version))
        generate(gendata, args.source_version)

    if args.find_values:
        parts = args.find_values.split(":")
        assert len(parts) == 2, "Incorrect find-values format"
        find_valid_values(parts[0], args.source_version, parts[1], args.find_values_limit)

if __name__ == "__main__":
    main()