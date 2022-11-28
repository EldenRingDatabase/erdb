import operator as op
from types import SimpleNamespace
from typing import NamedTuple, Self

from erdb.typing.effects import AttributeName, SchemaEffect


_A = AttributeName

class AttributeAggregatorHint(NamedTuple):
    base: set[AttributeName]
    effective: AttributeName

class AggregatedSchemaEffect(SimpleNamespace):
    attribute_names: set[AttributeName]
    example_effect: SchemaEffect

    @classmethod
    def from_effect(cls, effect: SchemaEffect) -> Self:
        return cls(attribute_names={effect.attribute}, example_effect=effect)

"""
Specifies which attribute sets can be collapsed into their effective attribute.
ORDER IS IMPORTANT because effective attributes are taken into consideration in
consecutive iterations.
"""
_AGGREGATOR_HINTS: list[AttributeAggregatorHint] = [
    AttributeAggregatorHint(
        base={_A.STANDARD_ABSORPTION, _A.STRIKE_ABSORPTION, _A.SLASH_ABSORPTION, _A.PIERCE_ABSORPTION},
        effective=_A.PHYSICAL_ABSORPTION
    ),
    AttributeAggregatorHint(
        base={_A.MAGIC_ABSORPTION, _A.FIRE_ABSORPTION, _A.LIGHTNING_ABSORPTION, _A.HOLY_ABSORPTION},
        effective=_A.ELEMENTAL_ABSORPTION
    ),
    AttributeAggregatorHint(
        base={_A.PHYSICAL_ABSORPTION, _A.ELEMENTAL_ABSORPTION},
        effective=_A.ABSORPTION
    ),
    AttributeAggregatorHint(
        base={_A.STANDARD_ATTACK_POWER, _A.STRIKE_ATTACK_POWER, _A.SLASH_ATTACK_POWER, _A.PIERCE_ATTACK_POWER},
        effective=_A.PHYSICAL_ATTACK_POWER
    ),
    AttributeAggregatorHint(
        base={_A.MAGIC_ATTACK_POWER, _A.FIRE_ATTACK_POWER, _A.LIGHTNING_ATTACK_POWER, _A.HOLY_ATTACK_POWER},
        effective=_A.ELEMENTAL_ATTACK_POWER
    ),
    AttributeAggregatorHint(
        base={_A.PHYSICAL_ATTACK_POWER, _A.ELEMENTAL_ATTACK_POWER},
        effective=_A.ATTACK_POWER
    ),
    AttributeAggregatorHint(
        base={_A.POISON_RESISTANCE, _A.SCARLET_ROT_RESISTANCE},
        effective=_A.IMMUNITY
    ),
    AttributeAggregatorHint(
        base={_A.BLEED_RESISTANCE, _A.FROSTBITE_RESISTANCE},
        effective=_A.ROBUSTNESS
    ),
    AttributeAggregatorHint(
        base={_A.SLEEP_RESISTANCE, _A.MADNESS_RESISTANCE},
        effective=_A.FOCUS
    ),
    AttributeAggregatorHint(
        base={_A.DEATH_BLIGHT_RESISTANCE},
        effective=_A.VITALITY
    ),
    AttributeAggregatorHint(
        base={_A.SORCERY_FOCUS_CONSUMPTION, _A.INCANTATION_FOCUS_CONSUMPTION, _A.PYROMANCY_FOCUS_CONSUMPTION},
        effective=_A.SPELL_FOCUS_CONSUMPTION
    ),
    AttributeAggregatorHint(
        base={_A.SORCERY_FOCUS_CONSUMPTION, _A.INCANTATION_FOCUS_CONSUMPTION}, # since pyromancies are unused
        effective=_A.SPELL_FOCUS_CONSUMPTION
    ),
]

def _get_aggregated_effects(effects: list[SchemaEffect]) -> dict[int, AggregatedSchemaEffect]:
    aggregated_effects: dict[int, AggregatedSchemaEffect] = dict()

    for effect in effects:
        if (key := effect.get_values_hash()) in aggregated_effects:
            aggregated_effects[key].attribute_names.add(effect.attribute)
        else:
            aggregated_effects[key] = AggregatedSchemaEffect.from_effect(effect)

    return aggregated_effects

def _aggregate_attributes(attributes: set[AttributeName], hints: list[AttributeAggregatorHint]) -> set[AttributeName]:
    for hint in hints:
        if hint.base.issubset(attributes):
            attributes.difference_update(hint.base)
            attributes.add(hint.effective)

    return attributes

def _aggregated_effects_to_effects(aggregated_effects: dict[int, AggregatedSchemaEffect]) -> list[SchemaEffect]:
    effects = []

    for aggregated_effect in aggregated_effects.values():
        for attribute_name in aggregated_effect.attribute_names:
            effects.append(aggregated_effect.example_effect.clone(attribute_name))

    return effects

def aggregate_effects(base_effects: list[SchemaEffect]) -> list[SchemaEffect]:
    aggregated_effects = _get_aggregated_effects(base_effects)

    for key, aggregated_effect in aggregated_effects.items():
        aggregated_effects[key].attribute_names = _aggregate_attributes(aggregated_effect.attribute_names, _AGGREGATOR_HINTS)

    return sorted(_aggregated_effects_to_effects(aggregated_effects), key=op.attrgetter("attribute"))