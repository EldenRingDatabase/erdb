from copy import deepcopy
from enum import Enum
from types import SimpleNamespace
from typing import Any, Callable, Dict, NamedTuple, Optional, List

class EffectType(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class EffectModel(str, Enum):
    MULTIPLICATIVE = "multiplicative"
    ADDITIVE = "additive"

"""
Helper class of attributes used for effects, these are self-made
and don't correspond to anything in the game.
Schema counterpart in ./enums/attributes-names.schema.json
"""
class AttributeName(str, Enum):
    MAXIMUM_HEALTH = "Maximum Health",
    HEALTH_POINTS = "Health Points",
    FLASK_HEALTH_RESTORATION = "Flask Health Restoration",
    MAXIMUM_FOCUS = "Maximum Focus",
    FOCUS_POINTS = "Focus Points",
    FLASK_FOCUS_RESTORATION = "Flask Focus Restoration",
    MAXIMUM_STAMINA = "Maximum Stamina",
    STAMINA_RECOVERY_SPEED = "Stamina Recovery Speed",
    MAXIMUM_EQUIP_LOAD = "Maximum Equip Load",
    POISE = "Poise",
    VIGOR = "Vigor",
    MIND = "Mind",
    ENDURANCE = "Endurance",
    STRENGHT = "Strength",
    DEXTERITY = "Dexterity",
    INTELLIGENCE = "Intelligence",
    FAITH = "Faith",
    ARCANE = "Arcane",
    STANDARD_ABSORPTION = "Standard Absorption",
    STRIKE_ABSORPTION = "Strike Absorption",
    SLASH_ABSORPTION = "Slash Absorption",
    PIERCE_ABSORPTION = "Pierce Absorption",
    PHYSICAL_ABSORPTION = "Physical Absorption",
    MAGIC_ABSORPTION = "Magic Absorption",
    FIRE_ABSORPTION = "Fire Absorption",
    LIGHTNING_ABSORPTION = "Lightning Absorption",
    HOLY_ABSORPTION = "Holy Absorption",
    ELEMENTAL_ABSORPTION = "Elemental Absorption",
    ABSORPTION = "Absorption",
    STANDARD_ATTACK_POWER = "Standard Attack Power",
    STRIKE_ATTACK_POWER = "Strike Attack Power",
    SLASH_ATTACK_POWER = "Slash Attack Power",
    PIERCE_ATTACK_POWER = "Pierce Attack Power",
    PHYSICAL_ATTACK_POWER = "Physical Attack Power",
    MAGIC_ATTACK_POWER = "Magic Attack Power",
    FIRE_ATTACK_POWER = "Fire Attack Power",
    LIGHTNING_ATTACK_POWER = "Lightning Attack Power",
    HOLY_ATTACK_POWER = "Holy Attack Power",
    ELEMENTAL_ATTACK_POWER = "Elemental Attack Power",
    ATTACK_POWER = "Attack Power",
    STAMINA_ATTACK_RATE = "Stamina Attack Rate"
    STABILITY = "Stability"
    IMMUNITY = "Immunity",
    ROBUSTNESS = "Robustness"
    VITALITY = "Vitality",
    FOCUS = "Focus",
    POISON_RESISTANCE = "Poison Resistance",
    SCARLET_ROT_RESISTANCE = "Scarlet Rot Resistance",
    BLEED_RESISTANCE = "Bleed Resistance",
    FROSTBITE_RESISTANCE = "Frostbite Resistance",
    SLEEP_RESISTANCE = "Sleep Resistance",
    MADNESS_RESISTANCE = "Madness Resistance",
    DEATH_BLIGHT_RESISTANCE = "Death Blight Resistance",
    MEMORY_SLOTS = "Memory Slots",
    CASTING_SPEED = "Casting Speed",
    SPELL_DURATION = "Spell Duration",
    SORCERY_FOCUS_CONSUMPTION = "Sorcery Focus Consumption",
    INCANTATION_FOCUS_CONSUMPTION = "Incantation Focus Consumption",
    PYROMANCY_FOCUS_CONSUMPTION = "Pyromancy Focus Consumption",
    SPELL_FOCUS_CONSUMPTION = "Spell Focus Consumption",
    SKILL_FOCUS_CONSUMPTION = "Skill Focus Consumption",
    BOW_DISTANCE = "Bow Distance",
    ENEMY_HEARING = "Enemy Hearing",
    FALL_DAMAGE = "Fall Damage",
    ITEM_DISCOVERY = "Item Discovery",
    RUNE_ACQUISITION = "Rune Acquisition",
    INVISIBLE_AT_DISTANCE = "Invisible at Distance"
    REDUCE_HEADSHOT_IMPACT = "Reduce Headshot Impact"
    SWITCH_ANIMATION_GENDER = "Switch Animation Gender"
    APPEAR_AS_COOPERATOR = "Appear as Cooperator"
    APPEAR_AS_HOST = "Appear as Host"
    PRESERVE_RUNES_ON_DEATH = "Preserve Runes on Death"
    DESTROY_ITEM_ON_DEATH = "Destroy Item on Death"
    ATTRACT_ENEMY_AGGRESSION = "Attract Enemy Aggression"

class AttributeField(NamedTuple):
    attribute: AttributeName
    effect_model: EffectModel
    effect_type: EffectType
    parser: Callable
    conditions: Optional[List[str]]
    default_value: Any

    def get_effective_type(self, value: Any):
        T = EffectType
        value_increase = value >= self.default_value
        return {
            T.POSITIVE: { True: T.POSITIVE, False: T.NEGATIVE, },
            T.NEGATIVE: { True: T.NEGATIVE, False: T.POSITIVE, },
            T.NEUTRAL:  { True: T.NEUTRAL,  False: T.NEUTRAL,  }
        }[self.effect_type][value_increase]

    @classmethod
    def create(cls, attribute: AttributeName, effect_model: EffectModel, effect_type: EffectType,
               parser: Callable, conditions: Optional[List[str]]=None, default_value: Optional[Any]=None) -> "AttributeField":

        def _default_value_from_model():
            return 1 if effect_model == EffectModel.MULTIPLICATIVE else 0

        default_value = _default_value_from_model() if default_value is None else default_value
        return cls(attribute, effect_model, effect_type, parser, conditions, default_value)

class SchemaEffect(SimpleNamespace):
    attribute: AttributeName
    conditions: Optional[List[str]]=None
    tick_interval: Optional[float]=None
    effect_model: EffectModel
    effect_type: EffectType
    value: float
    value_pvp: Optional[float]=None

    def to_dict(self) -> Dict:
        d = {
            "attribute": self.attribute,
            "model": self.effect_model,
            "type": self.effect_type,
            "value": self.value,
        }

        for prop in ["conditions", "tick_interval", "value_pvp"]:
            if getattr(self, prop) is not None:
                d[prop] = getattr(self, prop)

        return d

    def get_values_hash(self) -> int:
        conds = None if self.conditions is None else tuple(self.conditions)
        return hash((conds, self.tick_interval, self.effect_model, self.effect_type, self.value, self.value_pvp))

    def clone(self, new_attribute: AttributeName) -> "SchemaEffect":
        new_effect = deepcopy(self)
        new_effect.attribute = new_attribute
        return new_effect

    @classmethod
    def from_attribute_field(cls, value: float, attrib_field: AttributeField) -> "SchemaEffect":
        value = attrib_field.parser(value, attrib_field.effect_model)

        return cls(
            attribute=attrib_field.attribute,
            conditions=attrib_field.conditions,
            effect_model=attrib_field.effect_model,
            effect_type=attrib_field.get_effective_type(value),
            value=value)