import erdb.effect_parser.parsers as parse
from erdb.typing.effects import EffectModel, EffectType, AttributeName, AttributeField
from erdb.typing.enums import AttackCondition


_ATTRIBUTE_FIELDS = {
    "maxHpRate": AttributeField.create(
        attribute=AttributeName.MAXIMUM_HEALTH,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeHpPoint": AttributeField.create(
        attribute=AttributeName.HEALTH_POINTS,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "changeHpRate": AttributeField.create(
        attribute=AttributeName.HEALTH_POINTS,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse_percentage,
        default_value=0
    ),
    "changeHpEstusFlaskCorrectRate": AttributeField.create(
        attribute=AttributeName.FLASK_HEALTH_RESTORATION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "maxMpRate": AttributeField.create(
        attribute=AttributeName.MAXIMUM_FOCUS,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeMpPoint": AttributeField.create(
        attribute=AttributeName.FOCUS_POINTS,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "changeMpRate": AttributeField.create(
        attribute=AttributeName.FOCUS_POINTS,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse_percentage,
        default_value=0
    ),
    "changeMpEstusFlaskCorrectRate": AttributeField.create(
        attribute=AttributeName.FLASK_FOCUS_RESTORATION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "maxStaminaRate": AttributeField.create(
        attribute=AttributeName.MAXIMUM_STAMINA,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "staminaRecoverChangeSpeed": AttributeField.create(
        attribute=AttributeName.STAMINA_RECOVERY_SPEED,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "equipWeightChangeRate": AttributeField.create(
        attribute=AttributeName.MAXIMUM_EQUIP_LOAD,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "toughnessDamageCutRate": AttributeField.create(
        attribute=AttributeName.POISE,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.poise
    ),
    "addLifeForceStatus": AttributeField.create(
        attribute=AttributeName.VIGOR,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addWillpowerStatus": AttributeField.create(
        attribute=AttributeName.MIND,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addEndureStatus": AttributeField.create(
        attribute=AttributeName.ENDURANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addStrengthStatus": AttributeField.create(
        attribute=AttributeName.STRENGHT,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addDexterityStatus": AttributeField.create(
        attribute=AttributeName.DEXTERITY,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addMagicStatus": AttributeField.create(
        attribute=AttributeName.INTELLIGENCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addFaithStatus": AttributeField.create(
        attribute=AttributeName.FAITH,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "addLuckStatus": AttributeField.create(
        attribute=AttributeName.ARCANE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "neutralDamageCutRate": AttributeField.create(
        attribute=AttributeName.STANDARD_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "blowDamageCutRate": AttributeField.create(
        attribute=AttributeName.STRIKE_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "slashDamageCutRate": AttributeField.create(
        attribute=AttributeName.SLASH_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "thrustDamageCutRate": AttributeField.create(
        attribute=AttributeName.PIERCE_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "defEnemyDmgCorrectRate_Physics": AttributeField.create(
        attribute=AttributeName.PHYSICAL_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "magicDamageCutRate": AttributeField.create(
        attribute=AttributeName.MAGIC_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "defEnemyDmgCorrectRate_Magic": AttributeField.create(
        attribute=AttributeName.MAGIC_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "fireDamageCutRate": AttributeField.create(
        attribute=AttributeName.FIRE_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "defEnemyDmgCorrectRate_Fire": AttributeField.create(
        attribute=AttributeName.FIRE_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "thunderDamageCutRate": AttributeField.create(
        attribute=AttributeName.LIGHTNING_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "defEnemyDmgCorrectRate_Thunder": AttributeField.create(
        attribute=AttributeName.LIGHTNING_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "darkDamageCutRate": AttributeField.create(
        attribute=AttributeName.HOLY_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "defEnemyDmgCorrectRate_Dark": AttributeField.create(
        attribute=AttributeName.HOLY_ABSORPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic_inverse
    ),
    "neutralAttackPowerRate": AttributeField.create(
        attribute=AttributeName.STANDARD_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "blowAttackPowerRate": AttributeField.create(
        attribute=AttributeName.STRIKE_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "slashAttackPowerRate": AttributeField.create(
        attribute=AttributeName.SLASH_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "thrustAttackPowerRate": AttributeField.create(
        attribute=AttributeName.PIERCE_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "physicsAttackPowerRate": AttributeField.create(
        attribute=AttributeName.PHYSICAL_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "physicsAttackRate": AttributeField.create(
        attribute=AttributeName.PHYSICAL_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "atkEnemyDmgCorrectRate_Physics": AttributeField.create(
        attribute=AttributeName.PHYSICAL_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "magicAttackRate": AttributeField.create(
        attribute=AttributeName.MAGIC_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "atkEnemyDmgCorrectRate_Magic": AttributeField.create(
        attribute=AttributeName.MAGIC_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "fireAttackRate": AttributeField.create(
        attribute=AttributeName.FIRE_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "atkEnemyDmgCorrectRate_Fire": AttributeField.create(
        attribute=AttributeName.FIRE_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "thunderAttackRate": AttributeField.create(
        attribute=AttributeName.LIGHTNING_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "atkEnemyDmgCorrectRate_Thunder": AttributeField.create(
        attribute=AttributeName.LIGHTNING_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "darkAttackRate": AttributeField.create(
        attribute=AttributeName.HOLY_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "atkEnemyDmgCorrectRate_Dark": AttributeField.create(
        attribute=AttributeName.HOLY_ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "staminaAttackRate": AttributeField.create(
        attribute=AttributeName.STAMINA_ATTACK_RATE,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "guardStaminaCutRate": AttributeField.create(
        attribute=AttributeName.STABILITY,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changePoisonResistPoint": AttributeField.create(
        attribute=AttributeName.POISON_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeDiseaseResistPoint": AttributeField.create(
        attribute=AttributeName.SCARLET_ROT_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeBloodResistPoint": AttributeField.create(
        attribute=AttributeName.BLEED_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeFreezeResistPoint": AttributeField.create(
        attribute=AttributeName.FROSTBITE_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeSleepResistPoint": AttributeField.create(
        attribute=AttributeName.SLEEP_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeMadnessResistPoint": AttributeField.create(
        attribute=AttributeName.MADNESS_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeCurseResistPoint": AttributeField.create(
        attribute=AttributeName.DEATH_BLIGHT_RESISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "changeMagicSlot": AttributeField.create(
        attribute=AttributeName.MEMORY_SLOTS,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "dexterityCancelSystemOnlyAddDexterity": AttributeField.create(
        attribute=AttributeName.CASTING_SPEED,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "extendLifeRate": AttributeField.create(
        attribute=AttributeName.SPELL_DURATION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "magicConsumptionRate": AttributeField.create(
        attribute=AttributeName.SORCERY_FOCUS_CONSUMPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "miracleConsumptionRate": AttributeField.create(
        attribute=AttributeName.INCANTATION_FOCUS_CONSUMPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "shamanConsumptionRate": AttributeField.create( # likely unused
        attribute=AttributeName.PYROMANCY_FOCUS_CONSUMPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "artsConsumptionRate": AttributeField.create(
        attribute=AttributeName.SKILL_FOCUS_CONSUMPTION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "bowDistRate": AttributeField.create(
        attribute=AttributeName.BOW_DISTANCE,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "hearingSearchEnemyRate": AttributeField.create(
        attribute=AttributeName.ENEMY_HEARING,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "fallDamageRate": AttributeField.create(
        attribute=AttributeName.FALL_DAMAGE,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.NEGATIVE,
        parser=parse.generic
    ),
    "itemDropRate": AttributeField.create(
        attribute=AttributeName.ITEM_DISCOVERY,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.item_discovery
    ),
    "soulRate": AttributeField.create(
        attribute=AttributeName.RUNE_ACQUISITION,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
    "soul": AttributeField.create(
        attribute=AttributeName.RUNE_ACQUISITION,
        effect_model=EffectModel.ADDITIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic
    ),
}

_WEAPON_ATTRIBUTE_FIELDS = {
    "weakA_DamageRate": AttributeField.create(
        attribute=AttributeName.ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic,
        conditions=[str(AttackCondition.VS_GRAVITY_ENEMIES)]
    ),
    "weakB_DamageRate": AttributeField.create(
        attribute=AttributeName.ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic,
        conditions=[str(AttackCondition.VS_UNDEAD_ENEMIES)]
    ),
    "weakC_DamageRate": AttributeField.create(
        attribute=AttributeName.ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic,
        conditions=[str(AttackCondition.VS_DRAGON_ENEMIES)]
    ),
    "weakD_DamageRate": AttributeField.create(
        attribute=AttributeName.ATTACK_POWER,
        effect_model=EffectModel.MULTIPLICATIVE,
        effect_type=EffectType.POSITIVE,
        parser=parse.generic,
        conditions=[str(AttackCondition.VS_ANCIENT_DRAGON_ENEMIES)]
    ),
}

def get(weapon: bool = False) -> dict[str, AttributeField]:
    return _WEAPON_ATTRIBUTE_FIELDS if weapon else _ATTRIBUTE_FIELDS