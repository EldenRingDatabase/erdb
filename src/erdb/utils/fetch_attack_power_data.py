import json
from enum import Enum
from pathlib import Path
from time import sleep


try:
    import gspread
except ModuleNotFoundError:
    assert False, "Module \"gspread\" is not installed, please install it manually"

class Field(Enum):
    CLASS = "G10"
    NAME = "G11"
    AFFINITY = "G12"
    LEVEL = "G13"

    STRENGTH = "G15"
    DEXTERITY = "G16"
    INTELLIGENCE = "G17"
    FAITH = "G18"
    ARCANE = "G19"

    AP_PHYSICAL_BASE = "G30"
    AP_PHYSICAL_SCALING = "J30"
    AP_PHYSICAL_ROUNDED = "L30" # rounded

    AP_MAGIC_BASE = "G31"
    AP_MAGIC_SCALING = "J31"
    AP_MAGIC_ROUNDED = "L31" # rounded

    AP_FIRE_BASE = "G32"
    AP_FIRE_SCALING = "J32"
    AP_FIRE_ROUNDED = "L32" # rounded

    AP_LIGHTNING_BASE = "G33"
    AP_LIGHTNING_SCALING = "J33"
    AP_LIGHTNING_ROUNDED = "L33" # rounded

    AP_HOLY_BASE = "G34"
    AP_HOLY_SCALING = "J34"
    AP_HOLY_ROUNDED = "L34" # rounded

    SB_PHYSICAL_BASE = "G35"
    SB_PHYSICAL_SCALING = "J35"
    SB_PHYSICAL_ROUNDED = "L35" # rounded

    SB_MAGIC_BASE = "G36"
    SB_MAGIC_SCALING = "J36"
    SB_MAGIC_ROUNDED = "L36" # rounded

    SB_FIRE_BASE = "G37"
    SB_FIRE_SCALING = "J37"
    SB_FIRE_ROUNDED = "L37" # rounded

    SB_LIGHTNING_BASE = "G38"
    SB_LIGHTNING_SCALING = "J38"
    SB_LIGHTNING_ROUNDED = "L38" # rounded

    SB_HOLY_BASE = "G39"
    SB_HOLY_SCALING = "J39"
    SB_HOLY_ROUNDED = "L39" # rounded

    POISON_BASE = "G40"
    POISON_SCALING = "J40"
    POISON_ROUNDED = "L40" # rounded

    SCARLET_ROT_BASE = "G41"
    SCARLET_ROT_SCALING = "J41"
    SCARLET_ROT_ROUNDED = "L41" # rounded

    BLEED_BASE = "G42"
    BLEED_SCALING = "J42"
    BLEED_ROUNDED = "L42" # rounded

    FROSTBITE_BASE = "G43"
    FROSTBITE_SCALING = "J43"
    FROSTBITE_ROUNDED = "L43" # rounded

    SLEEP_BASE = "G44"
    SLEEP_SCALING = "J44"
    SLEEP_ROUNDED = "L44" # rounded

    MADNESS_BASE = "G45"
    MADNESS_SCALING = "J45"
    MADNESS_ROUNDED = "L45" # rounded

    @staticmethod
    def attribs() -> list["Field"]:
        return [Field.STRENGTH, Field.DEXTERITY, Field.INTELLIGENCE, Field.FAITH, Field.ARCANE]

_ATTRIB_SET: list[str] = [
    "20,18,30,30,7",  # holy
    "9,7,30,30,20",   # holy unoptimal
    "20,80,11,15,7",  # dexterity
    "8,80,9,9,20",    # dexterity unoptimal
    "30,18,11,70,7",  # faith
    "9,7,8,70,20",    # faith unoptimal
    "20,18,60,15,7",  # intelligence
    "9,7,60,9,20",    # intelligence unoptimal
    "1,1,1,1,1",      # lowest
    "20,18,11,15,80", # arcane
    "40,40,11,15,7",  # quality
    "40,40,6,8,20",   # quality unoptimal
    "10,10,10,10,10", # starting wretch
    "14,13,9,9,7",    # starting vagabond
    "60,18,11,15,7",  # strength
    "60,12,9,9,20",   # strength unoptimal
    "99,99,99,99,99", # unscaled shitter
]

def retry_on_quota_limit(times: int, time: int):
    def _decorator(func):
        def _newfn(*args, **kwargs):
            attempt = 0

            while attempt < times:
                try:
                    return func(*args, **kwargs)

                except gspread.exceptions.APIError as e:
                    print(f"Quota limit likely exceeded, trying again in {time} second(s)...", flush=True)
                    sleep(time)
                    attempt += 1

            return func(*args, **kwargs)

        return _newfn
    return _decorator

def _get_ingame_name(name: str) -> str:
    return {
        "Misericorde": "Miséricorde",
        "Great Epee": "Great Épée",
        "Varre's Bouquet": "Varré's Bouquet",
    }.get(name, name)

class OnlineCalc:
    _sheet: gspread.Worksheet
    _writes: int
    _reads: int

    def __init__(self, version: str, service_key: Path) -> None:
        gc = gspread.service_account(filename=service_key)
        self._sheet = gc.open(f"{version} Weapon AP Calculator").worksheet("Sheet1")
        self._writes = 0
        self._reads = 0

    @property
    def writes(self) -> int:
        return self._writes

    @property
    def reads(self) -> int:
        return self._reads

    def _inc_write(self):
        self._writes += 1

    def _inc_read(self):
        self._reads += 1

    @retry_on_quota_limit(times=60, time=5)
    def set_field(self, field: Field, value):
        self._sheet.update(field.value, value)
        self._inc_write()

    @retry_on_quota_limit(times=60, time=5)
    def set_fields(self, fields: list[Field], values: list):
        assert len(fields) == len(values)
        batch = [{"range": f.value, "values": [[v]]} for f, v in zip(fields, values)]
        self._sheet.batch_update(batch)
        self._inc_write()

    @retry_on_quota_limit(times=60, time=5)
    def get_field(self, field: Field):
        value = self._sheet.acell(field.value).value
        self._inc_read()
        return value

    @retry_on_quota_limit(times=60, time=5)
    def get_fields(self, start: Field, end: Field):
        values = self._sheet.get(f"{start.value}:{end.value}")
        self._inc_read()
        return values

    def set_armament(self, class_: str, name: str):
        # cannot self.set_fields because every field is checked individually
        self.set_field(Field.CLASS, class_)
        self.set_field(Field.NAME, name)

    def set_attribs(self, attribs: str):
        parts = attribs.split(",")
        assert len(parts) == 5

        self.set_fields(Field.attribs(), [*map(int, parts)])

def _get_attack_values(ap: list[str]) -> list[float]:
    return [float(v) for v in ap if v not in ["", "-   "]]

"""
gspread requires a path to the service key, downloaded from Google API when
setting up a serivce account login. Detailed instructions here:
https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account
"""
def fetch(version: str, service_key: str):
    calc = OnlineCalc(version, Path(service_key))
    calc.set_field(Field.LEVEL, 10) # always keep 10, valid for unique and standard armaments

    with open(Path.cwd() / version / "armaments.json", encoding="utf-8") as f:
        armaments = json.load(f)["Armaments"]

    # take sample for testing
    #armaments = {k: armaments[k] for k in list(armaments)[:30]}

    for attribs in _ATTRIB_SET:
        print(f"Attributes \"{attribs}\"", flush=True)

        calc.set_attribs(attribs)
        results = dict()

        count = len(armaments)

        for armament, data in armaments.items():
            print(f"Armament \"{armament}\" ({count} remaining)", flush=True)
            count -= 1

            print(f"Reads: {calc.reads}, writes: {calc.writes}", flush=True)

            calc.set_armament(data["class"], _get_ingame_name(armament))
            results[armament] = dict()

            for affinity in data["affinity"].keys():
                print(f"Affinity \"{affinity}\"", flush=True)

                calc.set_field(Field.AFFINITY, affinity)
                values = calc.get_fields(Field.AP_PHYSICAL_BASE, Field.MADNESS_ROUNDED)

                results[armament][affinity] = {
                    "attack_power": {
                        "physical": _get_attack_values(values[0]),
                        "magic": _get_attack_values(values[1]),
                        "fire": _get_attack_values(values[2]),
                        "lightning": _get_attack_values(values[3]),
                        "holy": _get_attack_values(values[4]),
                    },
                    "spell_buff": {
                        "physical": _get_attack_values(values[5]),
                        "magic": _get_attack_values(values[6]),
                        "fire": _get_attack_values(values[7]),
                        "lightning": _get_attack_values(values[8]),
                        "holy": _get_attack_values(values[9]),
                    },
                    "status_effects": {
                        "poison": _get_attack_values(values[10]),
                        "scarlet_rot": _get_attack_values(values[11]),
                        "bleed": _get_attack_values(values[12]),
                        "frostbite": _get_attack_values(values[13]),
                        "sleep": _get_attack_values(values[14]),
                        "madness": _get_attack_values(values[15]),
                    }
                }

        with open(Path.cwd() / f"{version}-attacks-{attribs}.json", mode="w") as f:
            json.dump(results, f, indent=4)

    print(f"Finished in {calc.reads} reads and {calc.writes} writes.", flush=True)
