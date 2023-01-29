import re
import json
import shutil
from typing import Iterable, NamedTuple
import requests
from io import BytesIO, TextIOWrapper
from pathlib import Path
from zipfile import ZipFile
from jinja2 import Environment, Template, FileSystemLoader
from htmlmin import minify as minifyhtml

import erdb.utils.attack_power as attack_power_module
from erdb.loaders import PKG_DATA_PATH
from erdb.utils.common import scaling_grade, to_somber
from erdb.table import Table


_ITEMS = {
    Table.ARMAMENTS: ["reinforcements"]
}

class ThirdpartyLibrary(NamedTuple):
    name: str
    destination: Path
    freeze_version: str
    files: Iterable[str]

    def _current_version(self) -> str | None:
        assert False, "not implemented"

    def _download(self, version: str):
        assert False, "not implemented"

    def ensure_version(self, desired: str | None):
        current = self._current_version()

        if current is None: # local not found
            self._download(self.freeze_version if desired is None else desired)

        elif desired is not None and desired != current:
            print(f"> Current {self.name} version ({current}) doesn't match desired ({desired}).", flush=True)
            self._download(desired)

class UIkit(ThirdpartyLibrary):
    def _current_version(self) -> str | None:
        versions: set[str] = set()

        for loc in self.files:
            if not (self.destination / loc).exists():
                return None

            with open(self.destination / loc, mode="r") as f:
                content = f.read(64) # version string is contained at the start

                if version_lookup := re.search(r"UIkit (\d+\.\d+\.\d+)", content):
                    versions.add(version_lookup.group(1))

                else:
                    return None # a file's wrong

        # every version must be the same
        return next(iter(versions)) if len(versions) == 1 else None

    def _download(self, version: str):
        print(f"> Downloading {self.name} {version}...", flush=True)

        shutil.rmtree(self.destination, ignore_errors=True)
        self.destination.mkdir(parents=True, exist_ok=False)

        resp = requests.get(f"https://github.com/uikit/uikit/releases/download/v{version}/uikit-{version}.zip")
        z = ZipFile(BytesIO(resp.content))

        for loc in self.files:
            z.extract(loc, self.destination)

        print(f"> {self.name} {version} installed at {self.destination}.", flush=True)

class PyScript(ThirdpartyLibrary):
    def _current_version(self) -> str | None:
        for loc in [*self.files, "version.txt"]:
            if not (self.destination / loc).exists():
                return None

        with open(self.destination / "version.txt", mode="r") as f:
            version = f.read()

        return version if len(version) > 0 else None

    def _download(self, version: str):
        print(f"> Downloading {self.name} {version}...", flush=True)

        shutil.rmtree(self.destination, ignore_errors=True)
        self.destination.mkdir(parents=True, exist_ok=False)

        for loc in self.files:
            with open(self.destination / loc, mode="wb") as f:
                resp = requests.get(f"https://pyscript.net/releases/{version}/{loc}")

                if resp.status_code != 200:
                    return

                f.write(resp.content)

        with open(self.destination / "version.txt", mode="w") as f:
            f.write(version)

        print(f"> {self.name} {version} installed at {self.destination}.", flush=True)

def _read_json(file: Path):
    with open(file, mode="r", encoding="utf-8") as f:
        return json.load(f)

def _write_html(template: Template, root: Path, file: Path, minimize: bool, **data):
    def relative_root():
        depth = len(file.parent.relative_to(root).parts)
        return "../" * depth

    def write(f: TextIOWrapper, data: str):
        f.write(minifyhtml(data, remove_all_empty_space=True, remove_comments=True) if minimize else data)

    with open(file, mode="w", encoding="utf-8") as f:
        write(f, template.render(site_root=relative_root(), **data))

def _generate_items(env: Environment, data_path: Path, minimize: bool, out: Path):
    items_path = out / "items"

    for table, dependencies in _ITEMS.items():
        print(f">>> Generating {table} wiki pages", flush=True)

        item_path = items_path / table
        item_path.mkdir(parents=True, exist_ok=True)

        with open(data_path / f"{table}.json", mode="r", encoding="utf-8") as f:
            main_data = json.load(f)

        data = {}

        for dep in dependencies:
            print(f"Reading dependent table {dep}", flush=True)
            with open(data_path / f"{dep}.json", mode="r", encoding="utf-8") as f:
                data[dep] = json.load(f)

        cur, count = 0, len(main_data)

        for key, item in main_data.items():
            print(f"[{(cur := cur + 1)}/{count}] {key}", flush=True)

            data["item"] = item

            single = env.get_template(f"{table}-single.html.jinja")
            _write_html(single, out, item_path / f"{key}.html", minimize, **data)

        print(f"Generating index page", flush=True)

        index = env.get_template(f"{table}-index.html.jinja")
        _write_html(index, out, item_path / "index.html", minimize, items=main_data)

        print(flush=True)

def _generate_tools(env: Environment, data_path: Path, out: Path):
    tools_path = out / "tools"
    tools_path.mkdir(parents=True, exist_ok=True)

    print(">>> Generating AR calculator", flush=True)

    data = {
        "armaments": _read_json(data_path / "armaments.json"),
        "correction_attack": _read_json(data_path / "correction-attack.json"),
        "correction_graph": _read_json(data_path / "correction-graph.json"),
        "reinforcements": _read_json(data_path / "reinforcements.json"),
    }

    shutil.copy(attack_power_module.__file__, out / "scripts")

    ar_calculator = env.get_template("ar-calculator.html.jinja")
    _write_html(ar_calculator, out, tools_path / "ar-calculator.html", minimize=False, **data)

def generate(uikit_version: str | None, pyscript_version: str | None, data_path: Path, minimize: bool, out: Path):
    thirdparty = out / "thirdparty"
    thirdparty.mkdir(parents=True, exist_ok=True)

    UIkit(
        "UIkit", thirdparty / "uikit",
        freeze_version="3.15.18",
        files=("css/uikit.min.css", "js/uikit.min.js", "js/uikit-icons.min.js")
    ).ensure_version(uikit_version)

    PyScript(
        "pyscript", thirdparty / "pyscript",
        freeze_version="2022.12.1",
        files=("pyscript.css", "pyscript.js")
    ).ensure_version(pyscript_version)

    env = Environment(loader=FileSystemLoader(PKG_DATA_PATH / "wiki" / "templates"))
    env.filters["scaling_grade"] = scaling_grade
    env.filters["to_somber"] = to_somber
    env.trim_blocks = True
    env.lstrip_blocks = True

    print(f">>> Copying scripts", flush=True)
    shutil.copytree(PKG_DATA_PATH / "wiki" / "scripts", out / "scripts", dirs_exist_ok=True)

    _generate_items(env, data_path, minimize, out)
    _generate_tools(env, data_path, out)