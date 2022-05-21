from sp_effect_parser.effect_typing import EffectModel, EffectType, AttributeName, SchemaEffect
from typing import Dict, List

"""
Some SpEffects don't seem to have anything that identify what they do (Greatshield Talisman)
and/or are simply too difficult to parse (Winged Sword Insignia). They are listed here for visibility.

The list for each SpEffect ID should contain only the problematic effect(s). If any effect is parsable,
it will be appended to this list automatically during generation.

If an effect has a list of conditions, they must be adhere to whatever is defined in the JSON schema.
The validation process will show any mismatches.

!! THIS LIST MUST BE CONFIRMED AFTER EACH UPDATE !!
Last confirmed ER version: 1.04.1
"""
_HARDCODED_EFFECTS: Dict[int, List[SchemaEffect]] = {
    # >> Greatshield Talisman
    # This effect does not seem to utilize `guardStaminaCutRate`, unlike other shield buffs.
    341000: [
        SchemaEffect(
            attribute=AttributeName.STABILITY,
            effect_model=EffectModel.MULTIPLICATIVE,
            effect_type=EffectType.POSITIVE,
            value=1.1
        )
    ]
}

def get(index: int) -> List[SchemaEffect]:
    return _HARDCODED_EFFECTS.get(index, [])