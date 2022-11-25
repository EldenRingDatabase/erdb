from pydantic import Field, NonNegativeInt, PositiveInt
from pydantic.dataclasses import dataclass

from erdb.typing.models import dt_config
from erdb.typing.models.item import Item
from erdb.typing.models.common import StatRequirements
from erdb.typing.categories import SpellCategory
from erdb.typing.enums import SpellHoldAction


@dataclass(config=dt_config())
class Spell(Item):
    fp_cost: NonNegativeInt = Field(...,
        description="Cost of FP to cast.",
        example=40,
    )
    fp_cost_extra: NonNegativeInt = Field(...,
        description="Additional cost of FP for a charged/continued attack. This is on top of the regular cost, not the full cost. Always 0 for non-holdable Spells.",
        example=10,
    )
    sp_cost: NonNegativeInt = Field(...,
        description="Cost of stamina to cast.",
        example=34,
    )
    sp_cost_extra: NonNegativeInt = Field(...,
        description="Additional cost of stamina for a charged/continued attack. This is on top of the regular cost, not the full cost. Always 0 for non-holdable Spells.",
        example=0
    )
    category: SpellCategory = Field(...,
        description="Category of the Spell.",
        example=SpellCategory.SORCERY,
    )
    slots_used: PositiveInt = Field(...,
        description="Specifies the number of Memory Slots occupied.",
        example=3,
    )
    hold_action: SpellHoldAction = Field(...,
        description="Defines the behavior of the Spell when the cast is held.",
        example=SpellHoldAction.CONTINUOUS,
    )
    is_weapon_buff: bool = Field(...,
        description="Specifies whether the Spell buffs a weapon in the right hand.",
        example=False,
    )
    is_shield_buff: bool = Field(...,
        description="Specifies whether the Spell buffs a shield in the left hand.",
        example=False,
    )
    is_horseback_castable: bool = Field(...,
        description="Specifies whether the Spell can be cast while on horseback.",
        example=True,
    )
    requirements: StatRequirements = Field(...,
        description="Attribute requirements of the Spell.",
        example=StatRequirements(intelligence=60),
    )