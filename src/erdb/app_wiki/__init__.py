import re
import json
import shutil
import requests
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from jinja2 import Environment, FileSystemLoader

from erdb.loaders import PKG_DATA_PATH
from erdb.utils.common import scaling_grade
from erdb.table import Table


_UIKIT_VERSION_FREEZE = "3.15.18"
_UIKIT_FILES = ("css/uikit.min.css", "js/uikit.min.js", "js/uikit-icons.min.js")

_ITEMS = {
    Table.ARMAMENTS: ["reinforcements"]
}

def _current_uikit_version(uikit_dir: Path) -> str | None:
    versions: set[str] = set()

    for loc in _UIKIT_FILES:
        if not (uikit_dir / loc).exists():
            return None

        with open(uikit_dir / loc, mode="r") as f:
            content = f.read(64) # version string is contained at the start

            if version_lookup := re.search(r"UIkit (\d+\.\d+\.\d+)", content):
                versions.add(version_lookup.group(1))

            else:
                return None # a file's wrong

    # every version must be the same
    return next(iter(versions)) if len(versions) == 1 else None

def _download_uikit(version: str, dest: Path):
    print(f"> Downloading UIkit {version}...", flush=True)

    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=False)

    resp = requests.get(f"https://github.com/uikit/uikit/releases/download/v{version}/uikit-{version}.zip")
    z = ZipFile(BytesIO(resp.content))

    for loc in _UIKIT_FILES:
        z.extract(loc, dest)

    print(f"> UIkit {version} installed at {dest}.", flush=True)

def _ensure_uikit_version(desired: str | None, uikit_dir: Path):
    current = _current_uikit_version(uikit_dir) 

    if current is None: # local not found
        _download_uikit(_UIKIT_VERSION_FREEZE if desired is None else desired, uikit_dir)

    elif desired is not None and desired != current:
        print(f"> Current UIkit version ({current}) doesn't match desired ({desired}).", flush=True)
        _download_uikit(desired, uikit_dir)

def _find_uikit_relative(start: Path, until: Path) -> str:
    path = start
    relative = ""

    while (path := path.parent) != until.parent:
        relative += "../"

        if "uikit" in (p.name for p in path.iterdir()):
            return f"{relative}uikit"

    return ""

def generate(uikit_version: str | None, data_path: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    _ensure_uikit_version(uikit_version, out / "uikit")

    env = Environment(loader=FileSystemLoader(PKG_DATA_PATH / "wiki" / "templates"))
    env.filters["scaling_grade"] = scaling_grade

    items_path = out / "items"

    for table, dependencies in _ITEMS.items():
        print(f">>> Generating {table} wiki pages", flush=True)

        item_path = items_path / table
        item_path.mkdir(parents=True, exist_ok=True)

        uikit_relative = _find_uikit_relative(item_path, out)

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
            with open(item_path / f"{key}.html", mode="w", encoding="utf-8") as f:
                f.write(single.render(uikit_relative=uikit_relative, **data))

        print(f"Generating index page", flush=True)

        index = env.get_template(f"{table}-index.html.jinja")
        with open(item_path / "index.html", mode="w", encoding="utf-8") as f:
            f.write(index.render(uikit_relative=uikit_relative, items=main_data))

        print(flush=True)