import json
from math import floor
from pathlib import Path
from typing import Dict, Iterator, NamedTuple, Tuple


"""
Wrapper class for values, specifying base damage of the armament
and additional scaling from player attributes. Can be unpacked with:
    base, scaling = ValueType(1, 2)
"""
class ValueType(NamedTuple):
    base: float
    scaling: float

    @property
    def total(self) -> float:
        return floor(self.base + self.scaling)

    def __iter__(self) -> Iterator[Tuple[float, float]]:
        return iter((self.base, self.scaling))

class AttackPower(NamedTuple):
    physical: ValueType
    magic: ValueType
    fire: ValueType
    lightning: ValueType
    holy: ValueType

    def items(self):
        return zip(self._fields, self)

class StatusEffects(NamedTuple):
    bleed: ValueType
    frostbite: ValueType
    poison: ValueType
    scarlet_rot: ValueType
    sleep: ValueType
    madness: ValueType

    def items(self):
        return zip(self._fields, self)

class Attributes(NamedTuple):
    strength: int
    dexterity: int
    intelligence: int
    faith: int
    arcane: int

    def items(self):
        return zip(self._fields, self)

    @classmethod
    def from_string(cls, string: str) -> "Attributes":
        parts = string.split(",")

        assert len(parts) == 5, "Invalid Attributes string"
        assert all(1 <= v <= 99 for v in map(int, parts)), "Invalid Attributes string"

        return cls(*map(int, parts))

    def __str__(self) -> str:
        return f"{self.strength},{self.dexterity},{self.intelligence},{self.faith},{self.arcane}"

class CorrectionAttack(NamedTuple):
    correction: Dict[str, Dict]
    override: Dict[str, Dict]
    ratio: Dict[str, Dict]

    @classmethod
    def from_dict(cls, data: Dict) -> "CorrectionAttack":
        return cls(data["correction"], data["override"], data["ratio"])

class CalculatorData(NamedTuple):
    armaments: Dict[str, Dict]
    reinforcements: Dict[str, Dict[str, Dict]]
    correction_attack: Dict[str, Dict[str, str]]
    correction_graph: Dict[str, Dict[str, float]]

    @classmethod
    def create(cls, data_path: Path) -> "CalculatorData":
        if not isinstance(data_path, Path):
            data_path = Path(data_path)

        with open(data_path / "armaments.json") as f:
            armaments = json.load(f)["Armaments"]

        with open(data_path / "reinforcements.json") as f:
            reinforcements = json.load(f)["Reinforcements"]

        with open(data_path / "correction-attack.json") as f:
            correction_attack = json.load(f)["CorrectionAttack"]

        with open(data_path / "correction-graph.json") as f:
            correction_graph = json.load(f)["CorrectionGraph"]

        return cls(armaments, reinforcements, correction_attack, correction_graph)

class ArmamentCalculator:
    _name: str
    _affinity: str
    _level: str

    # data cache relevant for this armament, affinity and level
    _affinity_properties: Dict
    _requirements: Dict[str, int]
    _reinforcement: Dict
    _correction_attack: CorrectionAttack
    _correction_graph: Dict[str, Dict[str, float]]

    def __init__(self, data: CalculatorData, name: str, affinity: str="Standard", level: str="0") -> None:
        self._name = name
        self._affinity = affinity
        self._level = level
        self._cache_data(data)

    def _cache_data(self, data: CalculatorData):
        """
        Cache some data we will be using for this particular armament/affinity/level combo,
        called every time the ArmamentCalculator instance is updated.
        """
        self._affinity_properties = data.armaments[self._name]["affinity"][self._affinity]
        reinforcement_type        = self._affinity_properties["reinforcement_type"]
        correction_attack_id      = self._affinity_properties["correction_attack_id"]

        self._requirements        = data.armaments[self._name]["requirement"]
        self._reinforcement       = data.reinforcements[reinforcement_type][self._level]
        self._correction_attack   = CorrectionAttack.from_dict(data.correction_attack[correction_attack_id])
        self._correction_graph    = data.correction_graph

    @property
    def name(self) -> str:
        return self._name

    @property
    def affinity(self) -> str:
        return self._affinity

    @property
    def level(self) -> str:
        return self._level

    def set_name(self, name: str, data: CalculatorData):
        self._name = name
        self._cache_data(data)

    def set_affinity(self, affinity: str, data: CalculatorData):
        self._affinity = affinity
        self._cache_data(data)

    def set_level(self, level: str, data: CalculatorData):
        self._level = level
        self._cache_data(data)

    """
    Calculate attack power of the weapon given player attributes.
    """
    def attack_power(self, attributes: Attributes) -> AttackPower:
        ret = {attack_type: self._get_base_and_scaled_damage(attack_type, attributes) for attack_type in AttackPower._fields}
        return AttackPower(**ret)

    """
    Retrieve base damage and scaled damage from the specific attack type and attributes.
    """
    def _get_base_and_scaled_damage(self, attack_type: str, attributes: Attributes) -> ValueType:
        base     = self._affinity_properties["damage"].get(attack_type, 0.0) * self._reinforcement["damage"][attack_type]
        scalings = [self._get_scaling_per_attribute(attack_type, attrib_name, attrib_value) for attrib_name, attrib_value in attributes.items()]
        low_cap  = min(scalings) # in case multiple attributes are not met, do not go below lowest scaling

        # return base damage and scaling which is the base * sum of scalings per every attribute
        return ValueType(base, base * max(low_cap, sum(scalings)))

    """
    Retrieve scaled damage for an attack type/player attribute/attribute value combo.
    """
    def _get_scaling_per_attribute(self, attack_type: str, attrib_name: str, attrib_value: int) -> float:
        # attack type does not scale with this attribute
        if not self._correction_attack.correction[attack_type][attrib_name]:
            return 0.0

        # get the impact ratio of the scaling for this attack type and attribute
        scaling_impact_ratio = self._correction_attack.ratio[attack_type][attrib_name]

        # requirement is not met, penalize scaling of this attack type for this attribute
        if attrib_value < self._requirements.get(attrib_name, 0):
            return 0.6 * (scaling_impact_ratio - 1) - 0.4

        # get scaling values for armament and its particular reinforcement level
        base_scaling  = self._affinity_properties["scaling"].get(attrib_name, 0.0)
        level_scaling = self._reinforcement["scaling"][attrib_name]

        # override base scaling if an override is defined
        base_scaling = self._correction_attack.override[attack_type].get(attrib_name, base_scaling)

        # get correction for scaling based on the attribute value
        correction_id      = self._affinity_properties["correction_calc_id"][attack_type]
        scaling_correction = self._correction_graph[correction_id][str(attrib_value)]

        # return actual scaled value for this attack type and attribute
        return scaling_impact_ratio - 1 + base_scaling * level_scaling * scaling_correction * scaling_impact_ratio

    """
    Calculate status effects of the weapon given player attributes.
    """
    def status_effects(self, attributes: Attributes) -> StatusEffects:
        ret = {effect_type: self._get_base_and_scaled_effect(effect_type, attributes) for effect_type in StatusEffects._fields}
        return StatusEffects(**ret)

    """
    Retrieve base and scaled status effect values from the specific effect type and attributes.
    """
    def _get_base_and_scaled_effect(self, effect_type: str, attributes: Attributes) -> ValueType:
        base = self._affinity_properties["status_effects"].get(effect_type, 0.0)

        # overwrite base value if the effect upgrades for the affinity
        if levels := self._affinity_properties["status_effect_overlay"].get(effect_type):
            base = levels[self._reinforcement["level"]]

        # retrieve scaling value if the effect can scale
        if correction_id := self._affinity_properties["correction_calc_id"].get(effect_type):
            base_scaling       = self._affinity_properties["scaling"].get("arcane", 0.0)
            level_scaling      = self._reinforcement["scaling"].get("arcane")
            scaling_correction = self._correction_graph[correction_id][str(attributes.arcane)]

            return ValueType(base, base * base_scaling * level_scaling * scaling_correction)
        
        return ValueType(base, 0.0)