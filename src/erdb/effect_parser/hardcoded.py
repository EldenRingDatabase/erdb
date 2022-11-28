from typing import Dict, List, NamedTuple, Self, Tuple, Union

from erdb.typing.effects import EffectModel, EffectType, AttributeName, SchemaEffect
from erdb.typing.enums import SpEffectType, AttackType, AttackCondition


class SpEffectConditionOffset(NamedTuple):
    condition: Union[None, SpEffectType, AttackType, AttackCondition]
    offset: int

class SpEffectRanges(NamedTuple):
    class IntRange(NamedTuple):
        begin: int
        end: int

        def __contains__(self, __x: object) -> bool:
            assert isinstance(__x, int)
            return self.begin <= __x <= self.end

    ranges: List[IntRange]

    def __contains__(self, __x: object) -> bool:
        if isinstance(__x, str):
            return int(__x) in self

        if not isinstance(__x, int):
            return False

        return any(__x in r for r in self.ranges)

    @classmethod
    def construct(cls, *ranges: Tuple[int, int]) -> Self:
        return cls([cls.IntRange(r[0], r[1]) for r in ranges])

"""
Some SpEffects don't seem to have anything that identify what they do (Greatshield Talisman)
and/or are simply too difficult to parse (Winged Sword Insignia). They are listed here for visibility.

The list for each SpEffect ID should contain only the problematic effect(s). If any effect is parsable,
it will be appended to this list automatically during generation.

!! THIS LIST MUST BE CONFIRMED AFTER EACH UPDATE !!
Last confirmed ER version: 1.04.1
"""
_FROM_ID: Dict[int, List[SchemaEffect]] = {
    # >> Greatshield Talisman
    # This effect does not seem to utilize `guardStaminaCutRate`, unlike other shield buffs.
    341000: [
        SchemaEffect(
            attribute=AttributeName.STABILITY,
            effect_model=EffectModel.MULTIPLICATIVE,
            effect_type=EffectType.POSITIVE,
            value=1.1
        )
    ],
    # >> Concealing Veil
    # Its only identifying property is the unique `invocationConditionsStateChange1` "Trigger on Crouch"
    360100: [
        SchemaEffect(
            attribute=AttributeName.INVISIBLE_AT_DISTANCE,
            conditions=[str(SpEffectType.TRIGGER_ON_CROUCH)],
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.POSITIVE,
            value=1
        )

    ],
    # >> Furled Finger's Trick-Mirror
    # Nothing is identifying this SpEffect besides its ID
    360800: [
        SchemaEffect(
            attribute=AttributeName.APPEAR_AS_HOST,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.NEUTRAL,
            value=1
        )
    ],
    # >> Host's Trick-Mirror
    # Nothing is identifying this SpEffect besides its ID
    360900: [
        SchemaEffect(
            attribute=AttributeName.APPEAR_AS_COOPERATOR,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.NEUTRAL,
            value=1
        )
    ],
    # >> Shabriri's Woe
    # Nothing is identifying this SpEffect besides its ID
    360500: [
        SchemaEffect(
            attribute=AttributeName.ATTRACT_ENEMY_AGGRESSION,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.NEUTRAL,
            value=1
        )
    ],
}

"""
Some SpEffects reference other SpEffects by themselves or their stateInfo. Some of them can be parsed,
while others can be problematic. This is the list of problematic SpEffects which hardcodes the offsets
of the effects they are referencing, along with a potential condition which activates them.
"""
_FROM_OFFSET: Dict[int, list[SpEffectConditionOffset]] = {
    350400: [ # Godskin Swaddling Cloth
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_HITS, 1)
    ],
    312500: [ # Millicent's Prosthesis
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_3_HITS, 5),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_6_HITS, 6),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_9_HITS, 7),
    ],
    320800: [ # Winged Sword Insignia
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_3_HITS, 4),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_6_HITS, 5),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_9_HITS, 6),
    ],
    320810: [ # Rotten Winged Sword Insignia
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_3_HITS, 4),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_6_HITS, 5),
        SpEffectConditionOffset(AttackCondition.SUCCESSIVE_9_HITS, 6),
    ],
    350500: [ # Assassin's Crimson Dagger
        SpEffectConditionOffset(None, 2) # None -- the referenced effect contains conditions
    ],
    350600: [ # Assassin's Cerulean Dagger
        SpEffectConditionOffset(None, 2) # None -- the referenced effect contains conditions
    ]
}

"""
Some SpEffects types define effects themselves without affecting any attributes.
"""
_FROM_TYPE: Dict[SpEffectType, List[SchemaEffect]] = {
    # >> Crucible Knot Talisman + IDs: 9648, 6044000
    # Crucible Knot Talisman does not seem to define exactly how much the damage is reduced.
    SpEffectType.REDUCE_HEADSHOT_IMPACT: [
        SchemaEffect(
            attribute=AttributeName.REDUCE_HEADSHOT_IMPACT,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.POSITIVE,
            value=1
        )
    ],
    # >> Entwining Umbilical Cord
    SpEffectType.SWITCH_ANIMATION_GENDER: [
        SchemaEffect(
            attribute=AttributeName.SWITCH_ANIMATION_GENDER,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.NEUTRAL,
            value=1
        )
    ],
    # >> Sacrificial Twig
    SpEffectType.DESTROY_ACCESSORY_BUT_SAVE_RUNES: [
        SchemaEffect(
            attribute=AttributeName.PRESERVE_RUNES_ON_DEATH,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.POSITIVE,
            value=1
        ),
        SchemaEffect(
            attribute=AttributeName.DESTROY_ITEM_ON_DEATH,
            effect_model=EffectModel.ADDITIVE,
            effect_type=EffectType.NEGATIVE,
            value=1
        ),
    ],
}

def get(index: int, sp_effect_type) -> List[SchemaEffect]:
    return _FROM_ID.get(index, []) + _FROM_TYPE.get(sp_effect_type, [])

def get_conditions(index: int) -> List[SpEffectConditionOffset]:
    return _FROM_OFFSET.get(index, [])

def get_status_effect_ranges() -> SpEffectRanges:
    return SpEffectRanges.construct((6400, 6810), (105000, 109000))