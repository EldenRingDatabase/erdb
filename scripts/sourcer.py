import json
import shutil
import subprocess as proc
import scripts.config as cfg
import xml.etree.ElementTree as xmltree
from itertools import chain, islice
from time import sleep
from hashlib import md5
from pathlib import Path
from typing import Tuple, Dict, List, NamedTuple, Optional
from scripts.game_version import GameVersion

def _prepare_writable_path(path: Path, default_filename: str) -> Path:
    (path if path.suffix == "" else path.parent).mkdir(parents=True, exist_ok=True)
    return path / default_filename if path.is_dir() else path

def _is_empty(d: Path) -> bool:
    assert d.is_dir(), f"{d} is not a directory."
    return not any(d.iterdir())

def _get_size(d: Path) -> str:
    assert d.is_dir(), f"{d} is not a directory."
    size = sum(p.stat().st_size for p in d.rglob("*"))
    return f"{size:,}"

def _load_manifest():
    with open(cfg.ROOT / "gamedata" / "_Extracted" / "manifest.json") as f:
        return json.load(f)

def _unpacked_dcx(dcx: Path) -> Path:
    return dcx.parent / dcx.stem

def _unpacked_tpf(tpf: Path) -> Path:
    return tpf.parent / tpf.name.replace(".", "-") / f"{tpf.stem}.dds"

def _chunks(files_iterable, size: int):
    it = iter(files_iterable)
    for first in it:
        yield chain([first], islice(it, size - 1))

class _File(NamedTuple):
    path: Path
    md5: Optional[str]

    @classmethod
    def from_manifest(cls, path: Path, name: str, md5: str) -> "_File":
        return cls(path / Path(name), None if len(md5) == 0 else md5)

    def __str__(self) -> str:
        return str(self.path)

class _Command(NamedTuple):
    args: List[str]

    def run(self, cwd: Path):
        print(f"> [{cwd}]", *self.args, flush=True)

        p = proc.Popen(self.args, cwd=cwd, stdout=proc.PIPE, stderr=proc.STDOUT, text=True, shell=True, bufsize=1)

        for line in p.stdout:
            print(line.strip(), flush=True)

        while p.poll() is None:
            sleep(0.2)

        assert p.returncode == 0, f"Command failed with return code {p.returncode}."

    @classmethod
    def make(cls, args: List[str], **kwargs) -> "_Command":
        return cls([arg.format(**kwargs) for arg in args])

class _Tool(NamedTuple):
    name: str
    url: str
    path: Path
    files: List[_File]
    commands: List[_Command]

    def check_files(self, ignore_checksum: bool):
        print(f"Validating files in \"{self.path}\"...", flush=True)

        for f in self.files:
            print("*", f, flush=True)

            assert f.path.exists(), f"{f} does not exist."

            if f.md5 is not None:
                if md5(f.path.read_bytes()).hexdigest() != f.md5:
                    if ignore_checksum:
                        print(f"WARNING: Checksum for {f} mismatched, but is being ignored.", flush=True)
                    else:
                        assert False, f"Mismatched checksum of {f}."

        print(f"{self.name} files validated successfully!", flush=True)

    def run_commands(self):
        print(f"\nRunning {len(self.commands)} tool command(s).", flush=True)
        for cmd in self.commands:
            cmd.run(self.path)

    def run_command(self, *args: str):
        _Command.make([*args]).run(self.path)

    @classmethod
    def from_manifest(cls, game_dir: Path, name: str, data: Dict, skip_commands: bool=False) -> "_Tool":
        path = cfg.ROOT / "thirdparty" / name
        files = [_File.from_manifest(path, name, md5) for name, md5 in data["files"].items()]

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

class _MapTile(NamedTuple):
    Coords = Tuple[int, int]
    Code = int
    Masks = Dict[Coords, Code]

    path: Path
    underground: bool
    lod: int
    x: int
    y: int
    code: Code

    @property
    def coords(self) -> Coords:
        return (self.x, self.y)

    @property
    def is_out_of_bounds(self) -> bool:
        """
        Tiles with this bit are always out of bounds, filtering them
        will allow us to trim more unused tiles at edges of the map.
        """
        return self.code & (1 << 14)

    @classmethod
    def from_path(cls, path: Path):
        # split until first dot, not necessairly extension in case of ".tpf.dcx"
        filename, _ = path.name.split(".", 1)

        parts = filename.split("_")
        assert len(parts) == 7, f"Invalid map tile filename: {path}"

        return cls(path, parts[2] == "M01", int(parts[3][1]), int(parts[4]), int(parts[5]), int(parts[6], 16))

    @staticmethod
    def glob(path: Path, extension: str, lod: int, underground: bool, masks: Masks) -> List["_MapTile"]:
        glob_filter = f"*MENU_MapTile_M0{1 if underground else 0}_L{lod}*{extension}"
        tiles = (_MapTile.from_path(p) for p in path.rglob(glob_filter))

        # filter the valid, fully-unlocked tile variants based on their bitmask
        return [t for t in tiles if masks.get(t.coords) == t.code and not t.is_out_of_bounds]

def source_gamedata(game_dir: Path, version: GameVersion, ignore_checksum: bool):
    destination = cfg.ROOT / "gamedata" / "_Extracted" / str(version)
    assert not destination.exists() or _is_empty(destination), f"{destination} exists and is not empty."

    # TODO: check if `game_dir` is UXM-unpacked (backup_ directory?)

    manifest = _load_manifest()
    tools = _Tool.load_all(game_dir, manifest)

    for tool in tools:
        print(f"\nUsing tool \"{tool.name}\", acquired from \"{tool.url}\".", flush=True)
        tool.check_files(ignore_checksum)
        tool.run_commands()

    print(f"Creating directory {destination}.", flush=True)
    destination.mkdir(exist_ok=True)

    print("Copying source files...", flush=True)
    for filename, metadata in manifest["gamedata"].items():
        location = metadata["location"].format(game_dir=game_dir)
        shutil.copy(Path(location) / filename, destination)

    print(f"Sourcing version {version} complete!", flush=True)

def _assemble_map(tiles: List[_MapTile], out: Optional[Path]=None):
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
    from PIL import Image

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

def _parse_tile_masks(mask_dir: Path, lod: int=0, underground: bool=False) -> _MapTile.Masks:
    masks: _MapTile.Masks = dict()

    mtmsk = f"MENU_MapTile_M0{1 if underground else 0}.mtmsk"
    tree = xmltree.parse(mask_dir / mtmsk)

    for entry in tree.getroot().findall(".//MapTileMask"):
        index = int(entry.attrib.get("id"))
        this_lod, coords = divmod(index, 10000)

        if this_lod == lod:
            x, y = divmod(coords, 100)
            masks[(x, y)] = int(entry.attrib.get("mask"))

    return masks

def source_map(game_dir: Path, out: Optional[Path]=None, lod: int=0, underground: bool=False, ignore_checksum: bool=False, keep_cache: bool=False):
    def _get_not_unpacked(tiles: List[_MapTile], func):
        return (t.path for t in tiles if not func(t.path).is_file())

    manifest = _load_manifest()

    yabber, = _Tool.load_custom(game_dir, manifest, "Yabber")
    yabber.check_files(ignore_checksum)

    tile_dir = (game_dir / "menu" / "71_maptile-tpfbhd" / "71_MapTile")
    mask_dir = (game_dir / "menu" / "71_maptile-mtmskbnd" / "GR" / "data" / "INTERROOT_win64" / "menu" / "ScaleForm" / "maptile" / "mask")

    try:

        if not tile_dir.is_dir() or _is_empty(tile_dir):
            yabber.run_command("Yabber.exe", f"{game_dir}/menu/71_maptile.tpfbhd")

        if not mask_dir.is_dir() or _is_empty(mask_dir):
            yabber.run_command("Yabber.DCX.exe", f"{game_dir}/menu/71_maptile.mtmskbnd.dcx")
            yabber.run_command("Yabber.exe", f"{game_dir}/menu/71_maptile.mtmskbnd")

        masks = _parse_tile_masks(mask_dir, lod, underground)

        dcx_tiles = _MapTile.glob(tile_dir, ".tpf.dcx", lod, underground, masks)
        dcx_files = _get_not_unpacked(dcx_tiles, _unpacked_dcx)
        for file_chunk in _chunks(dcx_files, 20):
            yabber.run_command("Yabber.DCX.exe", *map(str, file_chunk))

        tpf_tiles = _MapTile.glob(tile_dir, ".tpf", lod, underground, masks)
        tpf_files = _get_not_unpacked(tpf_tiles, _unpacked_tpf)
        for file_chunk in _chunks(tpf_files, 20):
            yabber.run_command("Yabber.exe", *map(str, file_chunk))

        _assemble_map(_MapTile.glob(tile_dir, ".dds", lod, underground, masks), out)

    except: raise

    finally:

        if keep_cache:
            print("Keeping unpacked files due to --keep-cache option:", flush=True)
            print("*", tile_dir, _get_size(tile_dir), "bytes", flush=True)
            print("*", mask_dir, _get_size(mask_dir), "bytes", flush=True)

        else:
            print("Removing unpacked files (--keep-cache not specified)...", flush=True)
            shutil.rmtree(tile_dir, ignore_errors=True)
            shutil.rmtree(mask_dir, ignore_errors=True)