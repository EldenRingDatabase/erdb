import json
import shutil
import subprocess as proc
import scripts.config as cfg
from time import sleep
from hashlib import md5
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional
from scripts.game_version import GameVersion

def _is_empty(directory: Path) -> bool:
    assert directory.is_dir(), f"{directory} is not a directory."
    return not any(directory.iterdir())

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
    def from_manifest(cls, args: List[str], **kwargs) -> "_Command":
        return cls([arg.format(**kwargs) for arg in args])

class _Tool(NamedTuple):
    name: str
    url: str
    path: Path
    files: List[_File]
    commands: List[_Command]

    def check_files(self, ignore_checksum: bool):
        print(f"Validating files in \"{self.path}\"...")

        for f in self.files:
            print("*", f)

            assert f.path.exists(), f"{f} does not exist."

            if f.md5 is not None:
                if md5(f.path.read_bytes()).hexdigest() != f.md5:
                    if ignore_checksum:
                        print(f"WARNING: Checksum for {f} mismatched, but is being ignored.")
                    else:
                        assert False, f"Mismatched checksum of {f}."

        print(f"{self.name} files validated successfully!")

    @classmethod
    def from_manifest(cls, game_dir: Path, name: str, data: Dict) -> "_Tool":
        path = cfg.ROOT / "thirdparty" / name
        files = [_File.from_manifest(path, name, md5) for name, md5 in data["files"].items()]
        commands = [_Command.from_manifest(args, game_dir=game_dir) for args in data["cmds"]]
        return cls(name, data["url"], path, files, commands)

def source_gamedata(game_dir: Path, version: GameVersion, ignore_checksum: bool):
    destination = cfg.ROOT / "gamedata" / "_Extracted" / str(version)
    assert not destination.exists() or _is_empty(destination), f"{destination} exists and is not empty."

    # TODO: check if `game_dir` is UXM-unpacked (backup_ directory?)

    with open(cfg.ROOT / "gamedata" / "_Extracted" / "manifest.json") as f:
        manifest = json.load(f)

    tools = [_Tool.from_manifest(game_dir, name, data) for name, data in manifest["tools"].items()]

    for tool in tools:
        print(f"\n>> Using tool \"{tool.name}\", acquired from \"{tool.url}\".")
        tool.check_files(ignore_checksum)

        print(f"\n>> Running {len(tool.commands)} tool command(s).")
        for cmd in tool.commands:
            cmd.run(tool.path)

    print(f">> Creating directory {destination}.")
    destination.mkdir(exist_ok=True)

    print(">> Copying source files...")
    for filename, metadata in manifest["gamedata"].items():
        location = metadata["location"].format(game_dir=game_dir)
        shutil.copy(Path(location) / filename, destination)

    print(f">> Sourcing version {version} complete!")