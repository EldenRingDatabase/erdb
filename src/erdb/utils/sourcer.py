import json
import shutil
import string
import requests
import subprocess as proc
import xml.etree.ElementTree as xmltree
from PIL import Image
from io import BytesIO
from csv import DictReader
from zipfile import ZipFile, ZIP_DEFLATED
from itertools import chain, islice
from time import sleep
from hashlib import md5
from pathlib import Path
from typing import NamedTuple, Self

from erdb.table import Table
from erdb.loaders import PKG_DATA_PATH
from erdb.utils.common import get_filename
from erdb.typing.game_version import GameVersion, GameVersionInstance
from erdb.typing.params import ParamRow
from erdb.typing.enums import ItemIDFlag


def _prepare_writable_path(path: Path, default_filename: str) -> Path:
    (path if path.suffix == "" else path.parent).mkdir(parents=True, exist_ok=True)
    return path / default_filename if path.is_dir() else path

def _is_empty(d: Path) -> bool:
    assert d.is_dir(), f"{d} is not a directory."
    return not any(d.iterdir())

def _load_manifest():
    with open(PKG_DATA_PATH / "gamedata" / "manifest.json") as f:
        return json.load(f)

def _process_cache(*paths: Path, keep_cache: bool):
    def get_size(d: Path) -> str:
        assert d.is_dir(), f"{d} is not a directory."
        size = sum(p.stat().st_size for p in d.rglob("*"))
        return f"{size:,}"

    if keep_cache:
        print("Keeping unpacked files due to --keep-cache option:", flush=True)
        for p in paths: print("*", p, get_size(p), "bytes", flush=True)

    else:
        print("Removing unpacked files (--keep-cache not provided)...", flush=True)
        for p in paths: shutil.rmtree(p, ignore_errors=True)

def _get_app_version(game_exe: Path) -> list[int]:
    try:
        import win32api as w
    except ModuleNotFoundError:
        assert False, "Module \"pywin32\" is not installed, please install it manually"

    info = w.GetFileVersionInfo(str(game_exe), "\\")
    ms = info["FileVersionMS"] # type: ignore
    ls = info["FileVersionLS"] # type: ignore
    major, minor, patch = w.HIWORD(ms), w.LOWORD(ms), w.HIWORD(ls)

    return [int(major), int(minor), int(patch)]

def _get_effective_version(game_dir: Path) -> GameVersion:
    app_version = _get_app_version(game_dir / "eldenring.exe")
    version_instance = GameVersionInstance.construct(app_version, game_dir / "regulation_version.txt")
    print(f"Detected versions: {version_instance}.", flush=True)
    return version_instance.effective

class _File(NamedTuple):
    path: Path
    verifier: str
    verifier_is_md5: bool

    @classmethod
    def from_manifest(cls, tool_path: Path, name: str, verifier: str, **kwargs) -> Self:
        verifier = verifier.format(**kwargs)
        verifier_is_md5 = all(c in string.hexdigits for c in verifier)
        return cls(tool_path / Path(name), verifier, verifier_is_md5)

    def __str__(self) -> str:
        return str(self.path)

class _Command(NamedTuple):
    args: list[str]

    def run(self, cwd: Path):
        print(f"> [{cwd}]", *self.args, flush=True)

        p = proc.Popen(self.args, cwd=cwd, stdout=proc.PIPE, stderr=proc.STDOUT, text=True, shell=True, bufsize=1)
        assert p.stdout is not None

        for line in p.stdout:
            print(line.strip(), flush=True)

        while p.poll() is None:
            sleep(0.2)

        assert p.returncode == 0, f"Command failed with return code {p.returncode}."

    @classmethod
    def make(cls, args: list[str], **kwargs) -> Self:
        return cls([arg.format(**kwargs) for arg in args])

class _Tool(NamedTuple):
    name: str
    url: str
    path: Path
    files: list[_File]
    commands: list[_Command]

    def check_files(self, ignore_checksum: bool):
        print(f"Validating files in \"{self.path}\"...", flush=True)

        for f in self.files:
            print("*", f, flush=True)

            if f.verifier_is_md5:
                assert f.path.exists(), f"{f} does not exist."

                if md5(f.path.read_bytes()).hexdigest() != f.verifier:
                    if ignore_checksum:
                        print(f"WARNING: Checksum for {f} mismatched, but is being ignored.", flush=True)
                    else:
                        assert False, f"Mismatched checksum of {f}."

            else:
                print(f"Copying {f.verifier} to {f.path}...")
                shutil.copy(f.verifier, f.path)

        print(f"{self.name} files validated successfully!", flush=True)

    def run_commands(self):
        print(f"\nRunning {len(self.commands)} tool command(s).", flush=True)
        for cmd in self.commands:
            cmd.run(self.path)

    def run_command(self, *args: str):
        _Command.make([*args]).run(self.path)

    @classmethod
    def from_manifest(cls, game_dir: Path, name: str, data: dict, skip_commands: bool = False) -> Self:
        path = PKG_DATA_PATH / "thirdparty" / name

        if not path.exists() or _is_empty(path):
            print(name, "is not found and will be downloaded...", flush=True)
            _Tool.download_and_unzip(data["url"], path)

        files = [_File.from_manifest(path, name, verifier, game_dir=game_dir) for name, verifier in data["files"].items()]

        commands = \
            [] if skip_commands else \
            [_Command.make(args, game_dir=game_dir) for args in data["cmds"]]

        return cls(name, data["url"], path, files, commands)

    @classmethod
    def load_all(cls, game_dir: Path, manifest):
        return [cls.from_manifest(game_dir, name, data) for name, data in manifest["tools"].items()]

    @classmethod
    def load_custom(cls, game_dir: Path, manifest, *names: str):
        return [cls.from_manifest(game_dir, name, manifest["tools"][name], skip_commands=True) for name in names]

    @staticmethod
    def download_and_unzip(url: str, destination: Path):
        print("Downloading", url, flush=True)

        resp = requests.get(url)

        z = ZipFile(BytesIO(resp.content))
        top_level_names = {name.split("/")[0] for name in z.namelist()}

        # each tool should have <ToolName>/<files> as contents of its zip
        assert len(top_level_names) == 1

        main_dir = next(iter(top_level_names))

        z.extractall(destination.parent)
        shutil.move(destination.parent / main_dir, destination)

        print("Extracted tool files to:", destination, flush=True)

class _MapTile(NamedTuple):
    Coords = tuple[int, int]
    Code = int
    Masks = dict[Coords, Code]

    path: Path
    underground: bool
    lod: int
    x: int
    y: int
    code: Code

    @property
    def stem(self) -> str:
        ext = "".join(self.path.suffixes)
        return self.path.name.removesuffix(ext)

    @property
    def coords(self) -> Coords:
        return (self.x, self.y)

    @property
    def is_out_of_bounds(self) -> bool:
        """
        Tiles with this bit are always out of bounds, filtering them
        will allow us to trim more unused tiles at edges of the map.
        """
        return bool(self.code & (1 << 14))

    @classmethod
    def from_path(cls, path: Path):
        # split until first dot, not necessairly extension in case of ".tpf.dcx"
        filename, _ = path.name.split(".", 1)

        parts = filename.split("_")
        assert len(parts) == 7, f"Invalid map tile filename: {path}"

        return cls(path, parts[2] == "M01", int(parts[3][1]), int(parts[4]), int(parts[5]), int(parts[6], 16))

    @staticmethod
    def glob(path: Path, extension: str, lod: int, underground: bool, masks: Masks) -> list["_MapTile"]:
        glob_filter = f"*MENU_MapTile_M0{1 if underground else 0}_L{lod}*{extension}"
        tiles = (_MapTile.from_path(p) for p in path.rglob(glob_filter))

        # filter the valid, fully-unlocked tile variants based on their bitmask
        return [t for t in tiles if masks.get(t.coords) == t.code and not t.is_out_of_bounds]

def source_gamedata(game_dir: Path, ignore_checksum: bool, version: GameVersion | None = None):
    # TODO: check if `game_dir` is UXM-unpacked (backup_ directory?)
    #       preferably do unpacking via custom CLI tool mimicing UXM

    manifest = _load_manifest()
    tools = _Tool.load_all(game_dir, manifest)

    for tool in tools:
        print(f"\nUsing tool \"{tool.name}\", acquired from \"{tool.url}\".", flush=True)
        tool.check_files(ignore_checksum)
        tool.run_commands()

    if version is None:
        version = _get_effective_version(game_dir)

    print(f"Effective version: {version}.", flush=True)

    archive = PKG_DATA_PATH / "gamedata" / f"{version}.zip"
    assert not archive.exists(), f"{archive} exists and is not empty."

    print(f"Adding files to archive...", flush=True)
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as z:
        for filename, metadata in manifest["gamedata"].items():
            location = metadata["location"].format(game_dir=game_dir)
            z.write(Path(location) / filename, arcname=filename)

    print(f"Sourcing version {version} complete!", flush=True)

def _assemble_map(tiles: list[_MapTile], out: Path | None = None):
    if len(tiles) == 0:
        print(f"WARNING: No tiles found with specified options.", flush=True)
        return

    low_x,  low_y  = min(t.x for t in tiles), min(t.y for t in tiles)
    high_x, high_y = max(t.x for t in tiles), max(t.y for t in tiles)

    # X and Y are number of tiles, add 1 for 0th row and col
    X, Y = high_x - low_x + 1, high_y - low_y + 1

    lod = tiles[0].lod
    level = "underground" if tiles[0].underground else "overworld"

    print(f"Generating {X}x{Y} {level} map file with lod {lod}...", flush=True)

    expected_size = 256
    worldmap = Image.new("RGB", (X * expected_size, Y * expected_size))

    for tile in tiles:
        with Image.open(tile.path) as img:
            assert expected_size == img.width == img.height
            x, y = tile.x - low_x, Y - tile.y + low_y - 1
            worldmap.paste(img, (x * expected_size, y * expected_size))

    if out is None:
        worldmap.show()
        return

    out = _prepare_writable_path(out, f"er_map_{level}_l{lod}.jpeg")
    print(f"Writing to {out}...", flush=True)

    worldmap.save(out, format=out.suffix[1:]) # remove the initial dot

def _parse_tile_masks(mask_dir: Path, lod: int = 0, underground: bool = False) -> _MapTile.Masks:
    masks: _MapTile.Masks = dict()

    mtmsk = f"MENU_MapTile_M0{1 if underground else 0}.mtmsk"
    tree = xmltree.parse(mask_dir / mtmsk)

    for entry in tree.getroot().findall(".//MapTileMask"):
        index = int(str(entry.attrib.get("id")))
        this_lod, coords = divmod(index, 10000)

        if this_lod == lod:
            x, y = divmod(coords, 100)
            masks[(x, y)] = int(str(entry.attrib.get("mask")))

    return masks

def _unpack_missing_dds(yabber: _Tool, dds_files: list[Path]):
    def chunks(files_iterable, size: int):
        it = iter(files_iterable)
        for first in it:
            yield chain([first], islice(it, size - 1))

    files = [f for f in dds_files if not f.exists()]
    files = [dcx for f in files if (dcx := f.parent.parent / f.with_suffix(".tpf.dcx").name).exists()]

    for files_chunk in chunks(files, 20):
        yabber.run_command("Yabber.exe", *map(str, files_chunk))

def source_map(game_dir: Path, out: Path | None = None, lod: int = 0, underground: bool = False, ignore_checksum: bool = False, keep_cache: bool = False):
    manifest = _load_manifest()

    yabber, = _Tool.load_custom(game_dir, manifest, "Yabber")
    yabber.check_files(ignore_checksum)

    tile_dir = game_dir / "menu" / "71_maptile-tpfbhd" / "71_MapTile"
    mask_dir = game_dir / "menu" / "71_maptile-mtmskbnd-dcx" / "GR" / "data" / "INTERROOT_win64" / "menu" / "ScaleForm" / "maptile" / "mask"

    try:

        if not tile_dir.is_dir() or _is_empty(tile_dir):
            yabber.run_command("Yabber.exe", f"{game_dir}/menu/71_maptile.tpfbhd")

        if not mask_dir.is_dir() or _is_empty(mask_dir):
            yabber.run_command("Yabber.exe", f"{game_dir}/menu/71_maptile.mtmskbnd.dcx")

        masks = _parse_tile_masks(mask_dir, lod, underground)

        dcx_tiles = _MapTile.glob(tile_dir, ".tpf.dcx", lod, underground, masks)
        dds_files = [t.path.parent / f"{t.stem}-tpf-dcx" / f"{t.stem}.dds" for t in dcx_tiles]

        _unpack_missing_dds(yabber, dds_files)

        _assemble_map(_MapTile.glob(tile_dir, ".dds", lod, underground, masks), out)

    except: raise
    finally: _process_cache(tile_dir, mask_dir, keep_cache=keep_cache)

def source_icons(game_dir: Path, tables: list[Table], size: int, desination: Path, ignore_checksum: bool = False, keep_cache: bool = False):
    assert 1 <= size <= 1024, f"Invalid size: {size}"

    def readr(tb: Table):
        """
        Need the make sure the item name is used from the very first occurence
        of the icon ID, otherwise icon IDs will be assigned to a fully upgraded
        version of the item since upgrades share the icon. Reverse reading the
        param is easier for dict comprehension, because instead of checking if a
        key exist, we can keep overriding and keep the code simpler.
        """
        with open(game_dir / "param" / "gameparam" / f"{tb.param_name}.csv", mode="r") as f:
            reader = DictReader(f, delimiter=";")
            rows = {int(row["Row ID"]): row for row in reader}

            for index in reversed(rows.keys()):
                yield ParamRow.make(rows[index], ItemIDFlag.DISABLE_CHECK)

    def get_names(tb: Table):
        assert "names" in tb.spec.msg_retrievers, f"Table {tb} must specify a \"names\" msg retriever to write icons."

        names_file = names_dir / "GR" / "data" / "INTERROOT_win64" / "msg" / "engUS" / (tb.spec.msg_retrievers["names"].file_name + ".fmg")
        yabber.run_command("Yabber.exe", str(names_file))

        tree = xmltree.parse(names_file.with_suffix(".fmg.xml"))
        entries = tree.findall(".//text")

        return {int(str(e.get("id"))) : str(e.text) for e in entries}

    def is_valid_row(tb: Table, row: ParamRow) -> bool:
        return all(pred(row) for pred in tb.spec.predicates) and row.index in tb.spec.main_param_retriever

    def get_icon_id(row: ParamRow) -> int:
        return row["iconId"].as_int if "iconId" in row else row["iconIdM"].as_int

    def get_icon_dds(loc: Path, icon_id: int) -> Path:
        stem = f"MENU_Knowledge_{icon_id:05}"
        return loc / "00_Solo" / f"{stem}-tpf-dcx" / f"{stem}.dds"

    manifest = _load_manifest()

    yabber, er_exporter = _Tool.load_custom(game_dir, manifest, "Yabber", "ERExporter.Param")
    yabber.check_files(ignore_checksum)
    er_exporter.check_files(ignore_checksum)

    table_dir = game_dir / "param" / "gameparam"
    names_dir = game_dir / "msg" / "engus" / "item-msgbnd-dcx"
    icon_dir = game_dir / "menu" / "hi" / "00_solo-tpfbhd"
    desination.mkdir(parents=True, exist_ok=True)

    try:

        if not table_dir.is_dir() or _is_empty(table_dir):
            er_exporter.run_command("ERExporter.Param.exe", f"{game_dir}/regulation.bin")

        param_files = (game_dir / "param" / "gameparam" / f"{tb.param_name}.param" for tb in tables)
        param_files = [f for f in param_files if not f.with_suffix(".csv").exists()]

        if len(param_files) > 0:
            er_exporter.run_command("ERExporter.Param.exe", *map(str, param_files))

        if not names_dir.is_dir() or _is_empty(names_dir):
            yabber.run_command("Yabber.exe", str(names_dir.parent / "item.msgbnd.dcx"))

        if not icon_dir.is_dir() or _is_empty(icon_dir):
            yabber.run_command("Yabber.exe", str(icon_dir.parent / "00_solo.tpfbhd"))

        for tb in tables:
            names = get_names(tb)
            dest = desination / str(tb)
            dest.mkdir()

            print(f"Exporting to {dest}...", flush=True)

            id_to_name = {get_icon_id(row): get_filename(names[row.index]) for row in readr(tb) if is_valid_row(tb, row)}
            dds_files  = [get_icon_dds(icon_dir, icon_id) for icon_id in id_to_name.keys()]

            _unpack_missing_dds(yabber, dds_files)

            cur, count = 0, len(id_to_name)

            for icon_id, name in id_to_name.items():
                dds = get_icon_dds(icon_dir, icon_id)

                if not dds.exists():
                    print(f"[{(cur := cur + 1)}/{count}] Skipping missing icon for {name}: {dds}", flush=True)
                    continue

                with Image.open(dds) as img:
                    out = dest / f"{name}.png"

                    print(f"[{(cur := cur + 1)}/{count}] {out}", flush=True)
                    img.resize((size, size)).save(out, format="png")

    except: raise
    finally: _process_cache(table_dir, names_dir, icon_dir, keep_cache=keep_cache)
