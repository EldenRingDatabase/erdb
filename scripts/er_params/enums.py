from enum import Enum, IntEnum

class ItemIDFlag(IntEnum):
    NON_EQUIPABBLE = 0 # params used only for references, ex. param sets
    WEAPONS = 0
    PROTECTORS = 1 << 28
    ACCESSORIES = 1 << 29
    GOODS = 1 << 30
    ASHES_OF_WAR = 1 << 31

class GoodsType(str, Enum):
    NORMAL_ITEM = "0"
    KEY_ITEM = "1"
    CRAFTING_MATERIAL = "2"
    REMEMBRANCE = "3"
    NONE_1 = "4"
    SORCERY_1 = "5"
    NONE_2 = "6"
    LESSER = "7"
    GREATER = "8"
    WONDROUS_PHYSICK = "9"
    WONDROUS_PHYSICK_TEAR = "10"
    REGENERATIVE_MATERIAL = "11"
    INFO_ITEM = "12"
    NONE_3 = "13"
    REINFORCEMENT_MATERIAL = "14"
    GREAT_RUNE = "15"
    INCANTATION_1 = "16"
    SORCERY_2 = "17"
    INCANTATION_2 = "18"

class GoodsRarity(IntEnum):
    COMMON = 1
    RARE = 2
    LEGENDARY = 3

class ReferenceCategory(str, Enum):
    ATTACK = "0"
    BULLET = "1"
    SP_EFFECT = "2"