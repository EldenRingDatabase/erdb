details = {
    "iconId": {
        "DisplayName": "Icon ID",
        "Description": "Icon ID (When -1, no icon is required)",
        "Minimum": "-1",
        "Maximum": "999999",
        "SortID": "1000"
    },
    "conditionHp": {
        "DisplayName": "Trigger at HP Below %",
        "Description": "Set what percentage of maxHP the remaining HP will be activated",
        "Minimum": "-1",
        "Maximum": "100",
        "Increment": "0.1",
        "SortID": "18000"
    },
    "effectEndurance": {
        "DisplayName": "Duration",
        "Description": "Change duration / -1 for permanent / 0 for one moment only",
        "Minimum": "-1",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "19000"
    },
    "motionInterval": {
        "DisplayName": "Trigger Interval",
        "Description": "Set how many seconds it occurs",
        "Minimum": "-1",
        "Maximum": "999",
        "Increment": "0.1",
        "SortID": "20000"
    },
    "maxHpRate": {
        "DisplayName": "Max HP %",
        "Description": "Correct the maximum HP",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "21000"
    },
    "maxMpRate": {
        "DisplayName": "Max FP %",
        "Description": "Correct the maximum MP",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "22000"
    },
    "maxStaminaRate": {
        "DisplayName": "Max Stamina %",
        "Description": "Correct the maximum SP",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "23000"
    },
    "slashDamageCutRate": {
        "DisplayName": "Absorption %: Slash",
        "Description": "Slash damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "29100"
    },
    "blowDamageCutRate": {
        "DisplayName": "Absorption %: Strike",
        "Description": "Batter damage ratio: The calculated damage is corrected by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "29200"
    },
    "thrustDamageCutRate": {
        "DisplayName": "Absorption %: Thrust",
        "Description": "Puncture damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "29300"
    },
    "neutralDamageCutRate": {
        "DisplayName": "Absorption %: Standard",
        "Description": "Non-attribute damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "29400"
    },
    "magicDamageCutRate": {
        "DisplayName": "Absorption %: Magic",
        "Description": "Magic damage multiplier: The calculated damage is corrected by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "30000"
    },
    "fireDamageCutRate": {
        "DisplayName": "Absorption %: Fire",
        "Description": "Flame damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31000"
    },
    "thunderDamageCutRate": {
        "DisplayName": "Absorption %: Lightning",
        "Description": "Electric shock damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31100"
    },
    "physicsAttackRate": {
        "DisplayName": "Attack %: Physical",
        "Description": "Physical damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "32000"
    },
    "magicAttackRate": {
        "DisplayName": "Attack %: Magic",
        "Description": "Magic damage multiplier: The calculated damage is corrected by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "33000"
    },
    "fireAttackRate": {
        "DisplayName": "Attack %: Fire",
        "Description": "Flame damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "34000"
    },
    "thunderAttackRate": {
        "DisplayName": "Attack %: Lightning",
        "Description": "Electric shock damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "34100"
    },
    "physicsAttackPowerRate": {
        "DisplayName": "Power %: Physical",
        "Description": "Multiply the physical attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "35000"
    },
    "magicAttackPowerRate": {
        "DisplayName": "Power %: Magic",
        "Description": "Multiply the magic attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "36000"
    },
    "fireAttackPowerRate": {
        "DisplayName": "Power %: Fire",
        "Description": "Multiply the fire attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "37000"
    },
    "thunderAttackPowerRate": {
        "DisplayName": "Power %: Lightning",
        "Description": "Multiply the electric shock attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "37100"
    },
    "physicsAttackPower": {
        "DisplayName": "Damage +: Physical",
        "Description": "Add or subtract the value set for physical attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "38000"
    },
    "magicAttackPower": {
        "DisplayName": "Damage +: Magic",
        "Description": "Add or subtract the value set for the magic attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "39000"
    },
    "fireAttackPower": {
        "DisplayName": "Damage +: Fire",
        "Description": "Add or subtract the value set for the flame attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "40000"
    },
    "thunderAttackPower": {
        "DisplayName": "Damage +: Lighting",
        "Description": "Add or subtract the value set for the electric shock attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "40100"
    },
    "physicsDiffenceRate": {
        "DisplayName": "Defence %: Physical",
        "Description": "Multiply the set value for physical defense",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "41000"
    },
    "magicDiffenceRate": {
        "DisplayName": "Defence %: Magic",
        "Description": "Multiply the value set for magic defense",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "42000"
    },
    "fireDiffenceRate": {
        "DisplayName": "Defence %: Fire",
        "Description": "Multiply the fire defense by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "43000"
    },
    "thunderDiffenceRate": {
        "DisplayName": "Defence %: Lightning",
        "Description": "Multiply the value set for the electric shock defense",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "43100"
    },
    "physicsDiffence": {
        "DisplayName": "Defence +: Physical",
        "Description": "Add or subtract the value set for physical defense",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "44000"
    },
    "magicDiffence": {
        "DisplayName": "Defence +: Magic",
        "Description": "Add or subtract the value set for magic defense",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "45000"
    },
    "fireDiffence": {
        "DisplayName": "Defence +: Fire",
        "Description": "Add or subtract the value set for the fire defense",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46000"
    },
    "thunderDiffence": {
        "DisplayName": "Defence +: Lightning",
        "Description": "Add or subtract the value set for the electric shock defense",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46100"
    },
    "NoGuardDamageRate": {
        "DisplayName": "No Guard Damage %",
        "Description": "Replace the damage ratio at the time of the gap with the set value (set on the damage side)",
        "Minimum": "-100",
        "Maximum": "100",
        "SortID": "47000"
    },
    "vitalSpotChangeRate": {
        "DisplayName": "Vital Spot Change %",
        "Description": "Replaces the damage calculation of the sweet spot with the specified value (key point damage correction) -Invalid at 1.0",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "48000"
    },
    "normalSpotChangeRate": {
        "DisplayName": "Normal Hit Change %",
        "Description": "Replaces normal hit damage calculation with the specified number -Invalid at 1.0",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "49000"
    },
    "lookAtTargetPosOffset": {
        "DisplayName": "Look-At Target Position Offset",
        "Description": "Offset the target position when the enemy looks at. Set to crouch or mount on the side to be seen",
        "Minimum": "-99.99",
        "Maximum": "99.99",
        "SortID": "75600"
    },
    "behaviorId": {
        "DisplayName": "Behavior ID",
        "Description": "Specified -1 when dealing damage using action ID from special effects\nNPC Behavior - Requires State Info 142\nPlayer Behavior - Requires State Info 275\nBullet Behavior - Requires State Info 33",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "50100",
        "ParamRef1": "BehaviorParam_PC",
        "ParamRef2": "BehaviorParam"
    },
    "changeHpRate": {
        "DisplayName": "Current HP %",
        "Description": "Set what percentage of the maximum HP to subtract (or add) with one activation",
        "Minimum": "-100",
        "Maximum": "100",
        "Increment": "0.1",
        "SortID": "51000"
    },
    "changeHpPoint": {
        "DisplayName": "Current HP +",
        "Description": "Set how many points to subtract (or add) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "52000"
    },
    "changeMpRate": {
        "DisplayName": "Current FP %",
        "Description": "Set what percentage of the maximum MP to subtract (or add) with one activation",
        "Minimum": "-100",
        "Maximum": "100",
        "Increment": "0.1",
        "SortID": "53000"
    },
    "changeMpPoint": {
        "DisplayName": "Current FP +",
        "Description": "Set how many points to subtract (or add) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "54000"
    },
    "mpRecoverChangeSpeed": {
        "DisplayName": "FP Recovery Speed",
        "Description": "Change the recovery speed. Add or subtract to the standard recovery speed and initial recovery speed of the recovery formula.",
        "Minimum": "-100",
        "Maximum": "100",
        "SortID": "55000"
    },
    "changeStaminaRate": {
        "DisplayName": "Current Stamina %",
        "Description": "Set what percentage of the maximum stamina to subtract (or add) with one activation",
        "Minimum": "-100",
        "Maximum": "100",
        "Increment": "1",
        "SortID": "56000"
    },
    "changeStaminaPoint": {
        "DisplayName": "Current Stamina +",
        "Description": "Set how many points to subtract (or add) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "57000"
    },
    "staminaRecoverChangeSpeed": {
        "DisplayName": "Stamina Recovery Speed",
        "Description": "Change the recovery speed. Add or subtract to the standard recovery speed and initial recovery speed of the recovery formula.",
        "Minimum": "-100",
        "Maximum": "100",
        "SortID": "58000"
    },
    "magicEffectTimeChange": {
        "DisplayName": "Magic Effect Time Change",
        "Description": "Add / subtract the time set for the effect duration only for magic that has the effect duration set to 0.1 seconds or more.",
        "Minimum": "-999",
        "Maximum": "999",
        "Increment": "0.1",
        "SortID": "59000"
    },
    "insideDurability": {
        "DisplayName": "Current Durability +",
        "Description": "Add or subtract the numerical value to the internal wear degree",
        "Minimum": "-999",
        "Maximum": "999",
        "SortID": "60000"
    },
    "maxDurability": {
        "DisplayName": "Max Durability",
        "Description": "Add the set value to the maximum value of the internal wear degree of durability.",
        "Minimum": "0",
        "Maximum": "999",
        "SortID": "61000"
    },
    "staminaAttackRate": {
        "DisplayName": "Attack %: Stamina",
        "Description": "Multiply the stamina attack power by a factor (1.0 1 times 0.5 half)",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "62000"
    },
    "poizonAttackPower": {
        "DisplayName": "Aux Inflict +: Poison",
        "Description": "A value to be added to the target's [poison resistance value] when it hits\nRequires State Info 2",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "64000"
    },
    "diseaseAttackPower": {
        "DisplayName": "Aux Inflict +: Scarlet Rot",
        "Description": "Numerical value to be added to the target [Plague resistance value] when hit\nRequires State Info 5",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "65000"
    },
    "bloodAttackPower": {
        "DisplayName": "Aux Inflict +: Hemorrhage",
        "Description": "A value to be added to the target's [bleeding resistance value] when it hits\nRequires State Info 6",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "66000"
    },
    "curseAttackPower": {
        "DisplayName": "Aux Inflict +: Blight",
        "Description": "A number to be added to the target [curse resistance value] when hit\nRequires State Info 116",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "66100"
    },
    "fallDamageRate": {
        "DisplayName": "Fall Damage %",
        "Description": "Multiply the damage calculation when falling",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "67000"
    },
    "soulRate": {
        "DisplayName": "Rune Gain %",
        "Description": "The amount of soul acquired when defeating an enemy is added by the specified multiple.\nRequires State Info 76",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "68000"
    },
    "equipWeightChangeRate": {
        "DisplayName": "Max Equip Load %",
        "Description": "Multiply the maximum equipment weight by the set magnification",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "69000"
    },
    "allItemWeightChangeRate": {
        "DisplayName": "Item Weight %",
        "Description": "Multiply the maximum weight you have by the set magnification",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "70000"
    },
    "soul": {
        "DisplayName": "Rune Gain +",
        "Description": "Add the set value to the possessed soul",
        "Minimum": "-99999999",
        "Maximum": "2100000000",
        "SortID": "71000"
    },
    "animIdOffset": {
        "DisplayName": "Anim ID Offset",
        "Description": "Anime ID offset (invalid-1)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "111500"
    },
    "haveSoulRate": {
        "DisplayName": "Rune Possession Amount %",
        "Description": "For enemy lap effect. It is applied when the soul goes out from the set character.",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "72000"
    },
    "targetPriority": {
        "DisplayName": "Target Priority",
        "Description": "During multiplayer, the enemy will give priority to being targeted as a target. Addition of priority. 0 is the default. It will be often targeted with a positive value. Minus is up to -1.",
        "Minimum": "-1",
        "Maximum": "10",
        "SortID": "73000"
    },
    "sightSearchEnemyRate": {
        "DisplayName": "Enemy Vision Adjustment",
        "Description": "Correct the ease of finding by a magnification",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "73620"
    },
    "hearingSearchEnemyRate": {
        "DisplayName": "Enemy Listen Adjustment",
        "Description": "Correct the loudness of the AI sound emitted by the magnification",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "73920"
    },
    "grabityRate": {
        "DisplayName": "Gravity %",
        "Description": "Gravity rate",
        "Minimum": "0",
        "Maximum": "1",
        "Increment": "0.001",
        "SortID": "87000"
    },
    "registPoizonChangeRate": {
        "DisplayName": "Aux Resist %: Poison",
        "Description": "Multiply the poison resistance value by the set multiplier",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88000"
    },
    "registDiseaseChangeRate": {
        "DisplayName": "Aux Resist %: Scarlet Rot",
        "Description": "Multiply the plague resistance value by the set magnification",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88100"
    },
    "registBloodChangeRate": {
        "DisplayName": "Aux Resist %: Hemorrhage",
        "Description": "Multiply the bleeding resistance value by the set magnification",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88200"
    },
    "registCurseChangeRate": {
        "DisplayName": "Aux Resist %: Blight",
        "Description": "Multiply the spell resistance value by the set multiplier",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88300"
    },
    "soulStealRate": {
        "DisplayName": "Soul Steal %",
        "Description": "Defense against HP robbed by NPCs in Soul Steel",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "91000"
    },
    "lifeReductionRate": {
        "DisplayName": "Effect Duration %",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "100000"
    },
    "hpRecoverRate": {
        "DisplayName": "HP Recovery Effectiveness %",
        "Description": "It doesn't work when HP decreases.",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "101000"
    },
    "replaceSpEffectId": {
        "DisplayName": "Chain SpEffect ID",
        "Description": "Special effect ID added at the end of life (-1 is ignored)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "111000",
        "ParamRef1": "SpEffectParam"
    },
    "cycleOccurrenceSpEffectId": {
        "DisplayName": "Cycle SpEffect ID",
        "Description": "Special effect ID that occurs in each activation cycle (-1 is ignored)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "111010",
        "ParamRef1": "SpEffectParam"
    },
    "atkOccurrenceSpEffectId": {
        "DisplayName": "Attack SpEffect ID",
        "Description": "Special effect ID that occurs when hitting an attack (-1 is ignored)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "111020",
        "ParamRef1": "SpEffectParam"
    },
    "guardDefFlickPowerRate": {
        "DisplayName": "Guard Defense - Weapon Repel Power %",
        "Description": "Repellent defense correction value when guarding",
        "DisplayFormat": "%.2f",
        "Minimum": "-99",
        "Maximum": "99",
        "SortID": "27530"
    },
    "guardStaminaCutRate": {
        "DisplayName": "Guard Stability %",
        "Description": "Stamina cut rate correction value when guarding",
        "DisplayFormat": "%.2f",
        "Minimum": "-99",
        "Maximum": "99",
        "SortID": "62100"
    },
    "rayCastPassedTime": {
        "DisplayName": "Raycast Passed Time",
        "Description": "Passing the line of sight: Activation time [ms] (for evil eye)",
        "Minimum": "-1",
        "Maximum": "30000",
        "SortID": "108000"
    },
    "magicSubCategoryChange1": {
        "DisplayName": "Conditional Category [1]",
        "Enum": "ATK_SUB_CATEGORY",
        "Description": "Vs to subcategory parameter change 1",
        "SortID": "26300"
    },
    "magicSubCategoryChange2": {
        "DisplayName": "Conditional Category [2]",
        "Enum": "ATK_SUB_CATEGORY",
        "Description": "Vs to subcategory parameter change 2",
        "SortID": "26310"
    },
    "bowDistRate": {
        "DisplayName": "Bow Distance %",
        "Description": "Correction value added to the flight distance correction of the weapon",
        "Minimum": "-100",
        "Maximum": "999",
        "SortID": "62200"
    },
    "spCategory": {
        "DisplayName": "Effect Category",
        "Enum": "SP_EFFECT_SPCATEGORY",
        "Description": "Categories that determine behavior such as overwriting special effects",
        "Maximum": "60000",
        "SortID": "2100"
    },
    "categoryPriority": {
        "DisplayName": "Category Priority",
        "Description": "Priority within the same category (lower one has priority)",
        "SortID": "2200"
    },
    "saveCategory": {
        "DisplayName": "Save Category",
        "Enum": "SP_EFFECT_SAVE_CATEGORY",
        "Description": "Category to save special effects",
        "Minimum": "-1",
        "SortID": "2300"
    },
    "changeMagicSlot": {
        "DisplayName": "Magic Attunement Slot",
        "Description": "You can increase the specified number of magic registration slots",
        "Maximum": "3",
        "SortID": "83000"
    },
    "changeMiracleSlot": {
        "DisplayName": "Miracle Attunement Slot",
        "Description": "You can increase the specified number of trajectory registration frames.",
        "Maximum": "3",
        "SortID": "84000"
    },
    "heroPointDamage": {
        "DisplayName": "Humanity Damage",
        "Description": "Damage value given to human nature value",
        "Minimum": "-99",
        "Maximum": "99",
        "SortID": "112000"
    },
    "defFlickPower": {
        "DisplayName": "Weapon Repel Defence +",
        "Description": "Set a value that overwrites the repelling defense",
        "SortID": "27510"
    },
    "flickDamageCutRate": {
        "DisplayName": "Weapon Repel Absorption %",
        "Description": "Set a value that overwrites the damage attenuation rate at the time of repelling",
        "Maximum": "100",
        "SortID": "27520"
    },
    "bloodDamageRate": {
        "DisplayName": "Damage Correction %: Hemorrhage",
        "Description": "Point damage of state change type [bleeding], correction value used only when% damage",
        "SortID": "90000"
    },
    "dmgLv_None": {
        "DisplayName": "Damage Level: No Impact",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv0",
        "Minimum": "0",
        "SortID": "27110"
    },
    "dmgLv_S": {
        "DisplayName": "Damage Level: Small Impact",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv1",
        "Minimum": "0",
        "SortID": "27130"
    },
    "dmgLv_M": {
        "DisplayName": "Damage Level: Medium Impact",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv2",
        "Minimum": "0",
        "SortID": "27140"
    },
    "dmgLv_L": {
        "DisplayName": "Damage Level: Large Impact",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv3",
        "Minimum": "0",
        "SortID": "27150"
    },
    "dmgLv_BlowM": {
        "DisplayName": "Damage Level: Medium Blow",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv4",
        "Minimum": "0",
        "SortID": "27170"
    },
    "dmgLv_Push": {
        "DisplayName": "Damage Level: Push",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv5",
        "Minimum": "0",
        "SortID": "27200"
    },
    "dmgLv_Strike": {
        "DisplayName": "Damage Level: Strike",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv6",
        "Minimum": "0",
        "SortID": "27180"
    },
    "dmgLv_BlowS": {
        "DisplayName": "Damage Level: Small Blow",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv7",
        "Minimum": "0",
        "SortID": "27160"
    },
    "dmgLv_Min": {
        "DisplayName": "Damage Level: Minimal",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv8",
        "Minimum": "0",
        "SortID": "27120"
    },
    "dmgLv_Uppercut": {
        "DisplayName": "Damage Level: Uppercut",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv9",
        "Minimum": "0",
        "SortID": "27190"
    },
    "dmgLv_BlowLL": {
        "DisplayName": "Damage Level: Blow Backward",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv10",
        "Minimum": "0",
        "SortID": "27200"
    },
    "dmgLv_Breath": {
        "DisplayName": "Damage Level: Breath",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "Specify the type to replace the damage Lv11",
        "Minimum": "0",
        "SortID": "27210"
    },
    "atkAttribute": {
        "DisplayName": "Attack Attribute",
        "Enum": "ATKPARAM_ATKATTR_TYPE",
        "Description": "Physical attributes to set for special effects",
        "SortID": "27400"
    },
    "spAttribute": {
        "DisplayName": "SpEffect Attribute",
        "Enum": "ATKPARAM_SPATTR_TYPE",
        "Description": "Special attributes to set for special effects",
        "SortID": "27500"
    },
    "stateInfo": {
        "DisplayName": "State Info",
        "Enum": "SP_EFFECT_TYPE",
        "Description": "State change judgment flag",
        "Maximum": "60000",
        "SortID": "2000"
    },
    "wepParamChange": {
        "DisplayName": "Weapon Parameter Change",
        "Enum": "SP_EFE_WEP_CHANGE_PARAM",
        "Description": "Specify which weapon is effective. If there is no limit, all attacks and defenses including enemies are targeted",
        "SortID": "24000"
    },
    "moveType": {
        "DisplayName": "Move Type",
        "Enum": "SP_EFFECT_MOVE_TYPE",
        "Description": "Movement type. Change the movement speed.",
        "SortID": "85000"
    },
    "lifeReductionType": {
        "DisplayName": "Effect Duration Multiplier - State Info",
        "Enum": "SP_EFFECT_TYPE",
        "Maximum": "255",
        "SortID": "99000"
    },
    "throwCondition": {
        "DisplayName": "Throw Trigger",
        "Enum": "SP_EFFECT_THROW_CONDITION_TYPE",
        "Description": "Throwing conditions. Affects the throwing mask.",
        "SortID": "110000"
    },
    "addBehaviorJudgeId_condition": {
        "DisplayName": "Add Behavior Judge ID - Trigger",
        "Description": "Condition value to add a value to the action judgment ID (Def: -1)",
        "Minimum": "-1",
        "Maximum": "9",
        "SortID": "113000"
    },
    "freezeDamageRate": {
        "DisplayName": "Damage Correction %: Frostbite",
        "Description": "Correction value used only for point damage and% damage of state change type [cold air]",
        "SortID": "90100"
    },
    "effectTargetSelf": {
        "DisplayName": "Target Self",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "3000"
    },
    "effectTargetFriend": {
        "DisplayName": "Target Friend",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "4000"
    },
    "effectTargetEnemy": {
        "DisplayName": "Target Enemy",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "5000"
    },
    "effectTargetPlayer": {
        "DisplayName": "Target Player",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "6000"
    },
    "effectTargetAI": {
        "DisplayName": "Target AI",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "7000"
    },
    "effectTargetLive": {
        "DisplayName": "Target Live",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "8000"
    },
    "effectTargetGhost": {
        "DisplayName": "Target Ghost",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "9000"
    },
    "disableSleep": {
        "DisplayName": "Disable Sleep",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If this effect is applied, you will not sleep",
        "Maximum": "1",
        "SortID": "104070"
    },
    "disableMadness": {
        "DisplayName": "Disable Madness",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "With this effect, you won't go mad",
        "Maximum": "1",
        "SortID": "104080"
    },
    "effectTargetAttacker": {
        "DisplayName": "Target Attacker",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Apply special effects to attackers after damage (cannot enter defenders)",
        "Maximum": "1",
        "SortID": "12000"
    },
    "dispIconNonactive": {
        "DisplayName": "Display Icon when Inactive",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "The icon is displayed even in the state of waiting for activation.",
        "Maximum": "1",
        "SortID": "13000"
    },
    "regainGaugeDamage": {
        "DisplayName": "Generate Regain Gauge",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether to generate a regain gauge",
        "Maximum": "1",
        "SortID": "161000"
    },
    "bAdjustMagicAblity": {
        "DisplayName": "Use Intelligence Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you want to correct the magic power?",
        "Maximum": "1",
        "SortID": "15000"
    },
    "bAdjustFaithAblity": {
        "DisplayName": "Use Faith Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you correct your faith?",
        "Maximum": "1",
        "SortID": "16000"
    },
    "bGameClearBonus": {
        "DisplayName": "Enable for Game Clear",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether it is for the game clear lap bonus.",
        "Maximum": "1",
        "SortID": "17000"
    },
    "magParamChange": {
        "DisplayName": "Affects Sorcery",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Set whether or not it is effective against magic",
        "Maximum": "1",
        "SortID": "25000"
    },
    "miracleParamChange": {
        "DisplayName": "Affects Incantation",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Set whether or not it is effective against miracles",
        "Maximum": "1",
        "SortID": "26000"
    },
    "clearSoul": {
        "DisplayName": "Clear Held Runes",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Possession soul becomes 0.",
        "Maximum": "1",
        "SortID": "27000"
    },
    "requestSOS": {
        "DisplayName": "Request: Friendly Phantom Summon",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, issue an SOS sign request when activated",
        "Maximum": "1",
        "SortID": "76000"
    },
    "requestBlackSOS": {
        "DisplayName": "Request: Hostile Phantom Summon",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, issue a black SOS sign request when activated",
        "Maximum": "1",
        "SortID": "77000"
    },
    "requestForceJoinBlackSOS": {
        "DisplayName": "Request: Invasion",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, issue an intrusion_A request when activated",
        "Maximum": "1",
        "SortID": "78000"
    },
    "requestKickSession": {
        "DisplayName": "Request: Kick",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, a kick request will be issued at the time of activation.",
        "Maximum": "1",
        "SortID": "79000"
    },
    "requestLeaveSession": {
        "DisplayName": "Request: Return to Own World",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, an exit request will be issued at the time of activation.",
        "Maximum": "1",
        "SortID": "80000"
    },
    "requestNpcInveda": {
        "DisplayName": "Request: NPC Invasion",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, an intrusion request to the NPC will be issued at the time of activation.",
        "Maximum": "1",
        "SortID": "80100"
    },
    "noDead": {
        "DisplayName": "Is No Dead",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether you can be corpse. With this check, you will not be dead",
        "Maximum": "1",
        "SortID": "81000"
    },
    "bCurrHPIndependeMaxHP": {
        "DisplayName": "Current HP independent Max HP",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Does HP now affect even if the maximum HP increases or decreases?",
        "Maximum": "1",
        "SortID": "82000"
    },
    "corrosionIgnore": {
        "DisplayName": "Ignore Durability Loss",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "[State change type] ignores [Durability] decrease due to [Corrosion]",
        "Maximum": "1",
        "SortID": "92000"
    },
    "sightSearchCutIgnore": {
        "DisplayName": "Ignore Vision Reductions",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Ignore visual search invalidity",
        "Maximum": "1",
        "SortID": "93000"
    },
    "hearingSearchCutIgnore": {
        "DisplayName": "Ignore Listen Reductions",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Ignore auditory search invalidity",
        "Maximum": "1",
        "SortID": "94000"
    },
    "antiMagicIgnore": {
        "DisplayName": "Ignore Anti-Magic Effect",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "You can use magic even in the anti-magic range",
        "Maximum": "1",
        "SortID": "95000"
    },
    "fakeTargetIgnore": {
        "DisplayName": "Ignore Fake Targets",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Don't get caught in the fake target that occurred",
        "Maximum": "1",
        "SortID": "96000"
    },
    "fakeTargetIgnoreUndead": {
        "DisplayName": "Ignore Fake Human Targets",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "You will not be caught by the fake target of the human system that occurred",
        "Maximum": "1",
        "SortID": "96500"
    },
    "fakeTargetIgnoreAnimal": {
        "DisplayName": "Ignore Fake Animal Targets",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "You will not be caught by the fake target of the beast system that occurred",
        "Maximum": "1",
        "SortID": "96600"
    },
    "grabityIgnore": {
        "DisplayName": "Ignore Gravity Change",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Gravity effect disabled",
        "Maximum": "1",
        "SortID": "97000"
    },
    "disablePoison": {
        "DisplayName": "Disable Poison",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If this effect is applied, it will not be poisoned.",
        "Maximum": "1",
        "SortID": "102000"
    },
    "disableDisease": {
        "DisplayName": "Disable Scarlet Rot",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If this effect is applied, you will not get plague",
        "Maximum": "1",
        "SortID": "103000"
    },
    "disableBlood": {
        "DisplayName": "Disable Hemorrhage",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "With this effect, you won't get bleeding",
        "Maximum": "1",
        "SortID": "104000"
    },
    "disableCurse": {
        "DisplayName": "Disable Blight",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "With this effect, you won't be cursed",
        "Maximum": "1",
        "SortID": "104050"
    },
    "enableCharm": {
        "DisplayName": "Enable Charm",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If this effect is applied, you will be fascinated.",
        "Maximum": "1",
        "SortID": "104100"
    },
    "enableLifeTime": {
        "DisplayName": "Enable Lifetime",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Will the life be extended when the flag is set by TAE?",
        "Maximum": "1",
        "SortID": "105000"
    },
    "bAdjustStrengthAblity": {
        "DisplayName": "Use Strength Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you want to correct your strength?",
        "Maximum": "1",
        "SortID": "16100"
    },
    "bAdjustAgilityAblity": {
        "DisplayName": "Use Dexterity Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you want to correct your workmanship?",
        "Maximum": "1",
        "SortID": "16200"
    },
    "eraseOnBonfireRecover": {
        "DisplayName": "Erase on Bonfire Rest",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Will it be extinguished by bonfire recovery?",
        "Maximum": "1",
        "SortID": "20600"
    },
    "throwAttackParamChange": {
        "DisplayName": "Throw Attack Param Change",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Set whether or not it is effective against throwing attacks",
        "Maximum": "1",
        "SortID": "26200"
    },
    "requestLeaveColiseumSession": {
        "DisplayName": "Request: Leave Arena",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, a request to leave the arena will be issued at the time of activation.",
        "Maximum": "1",
        "SortID": "80000"
    },
    "isExtendSpEffectLife": {
        "DisplayName": "Has Effect Duration Adjustment Applied",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether to be eligible for extension when the life extension effect is applied",
        "Maximum": "1",
        "SortID": "105100"
    },
    "hasTarget": {
        "DisplayName": "Has Target",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you know the enemy? : [Activation condition] (for evil eye users)",
        "Maximum": "1",
        "SortID": "109000"
    },
    "replanningOnFire": {
        "DisplayName": "Cancel on Fire Damage",
        "Enum": "BOOL_CIRCLECROSS_TYPE",
        "Description": "Whether to replan at the time of activation",
        "Maximum": "1",
        "SortID": "72700"
    },
    "vowType0": {
        "DisplayName": "Trigger for Vow Type [0]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 0",
        "Maximum": "1",
        "SortID": "130000"
    },
    "vowType1": {
        "DisplayName": "Trigger for Vow Type [1]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 1",
        "Maximum": "1",
        "SortID": "130100"
    },
    "vowType2": {
        "DisplayName": "Trigger for Vow Type [2]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 2",
        "Maximum": "1",
        "SortID": "130200"
    },
    "vowType3": {
        "DisplayName": "Trigger for Vow Type [3]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 3",
        "Maximum": "1",
        "SortID": "130300"
    },
    "vowType4": {
        "DisplayName": "Trigger for Vow Type [4]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 4",
        "Maximum": "1",
        "SortID": "130400"
    },
    "vowType5": {
        "DisplayName": "Trigger for Vow Type [5]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 5",
        "Maximum": "1",
        "SortID": "130500"
    },
    "vowType6": {
        "DisplayName": "Trigger for Vow Type [6]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 6",
        "Maximum": "1",
        "SortID": "130600"
    },
    "vowType7": {
        "DisplayName": "Trigger for Vow Type [7]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 7",
        "Maximum": "1",
        "SortID": "130700"
    },
    "vowType8": {
        "DisplayName": "Trigger for Vow Type [8]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 8",
        "Maximum": "1",
        "SortID": "130800"
    },
    "vowType9": {
        "DisplayName": "Trigger for Vow Type [9]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 9",
        "Maximum": "1",
        "SortID": "130900"
    },
    "vowType10": {
        "DisplayName": "Trigger for Vow Type [10]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 10",
        "Maximum": "1",
        "SortID": "131000"
    },
    "vowType11": {
        "DisplayName": "Trigger for Vow Type [11]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 11",
        "Maximum": "1",
        "SortID": "131100"
    },
    "vowType12": {
        "DisplayName": "Trigger for Vow Type [12]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 12",
        "Maximum": "1",
        "SortID": "131200"
    },
    "vowType13": {
        "DisplayName": "Trigger for Vow Type [13]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 13",
        "Maximum": "1",
        "SortID": "131300"
    },
    "vowType14": {
        "DisplayName": "Trigger for Vow Type [14]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 14",
        "Maximum": "1",
        "SortID": "131400"
    },
    "vowType15": {
        "DisplayName": "Trigger for Vow Type [15]",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Pledge 15",
        "Maximum": "1",
        "SortID": "131500"
    },
    "repAtkDmgLv": {
        "DisplayName": "Change Attacker Damage Level",
        "Enum": "ATKPARAM_REP_DMGTYPE",
        "Description": "The damage level of the attacking side changes to this value",
        "Minimum": "0",
        "SortID": "152000"
    },
    "sightSearchRate": {
        "DisplayName": "AI Vision Correction",
        "Description": "Correct the ease of finding with a magnification\nRequires State Info 267",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "73720"
    },
    "effectTargetOpposeTarget": {
        "DisplayName": "Trigger for Opponent",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "12100"
    },
    "effectTargetFriendlyTarget": {
        "DisplayName": "Trigger for Friendly",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "12200"
    },
    "effectTargetSelfTarget": {
        "DisplayName": "Trigger for Self",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "12300"
    },
    "effectTargetPcHorse": {
        "DisplayName": "Trigger for Horse",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "12350"
    },
    "effectTargetPcDeceased": {
        "DisplayName": "Trigger for Dead Player",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Only the target for which this judgment is checked is effective, the default is ×",
        "Maximum": "1",
        "SortID": "12400"
    },
    "isContractSpEffectLife": {
        "DisplayName": "Can Duration be Reduced",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether it will be shortened when the life shortening effect is applied",
        "Maximum": "1",
        "SortID": "105110"
    },
    "isWaitModeDelete": {
        "DisplayName": "Delete in Wait Mode",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do you want to delete it the moment you are in a waiting state?",
        "Maximum": "1",
        "SortID": "411000"
    },
    "isIgnoreNoDamage": {
        "DisplayName": "Apply through No Damage",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether to apply the damage from this special effect even in the invincible state only when the state change type \"Apply the activation function even when invincible\" is applied.",
        "Maximum": "1",
        "SortID": "411100"
    },
    "changeTeamType": {
        "DisplayName": "Team Type",
        "Enum": "SP_EFFECT_CHANGE_TEAM_TYPE",
        "Description": "Overwrites the specified team type\nRequires State Info 132",
        "Minimum": "-1",
        "Maximum": "99",
        "SortID": "84900"
    },
    "dmypolyId": {
        "DisplayName": "Bullet Behavior ID - DmyPoly ID",
        "Description": "Damipoli ID. Damipoli ID range is 0 to 999.1000, 10000 is the category number.",
        "Minimum": "-1",
        "Maximum": "31999",
        "SortID": "50200"
    },
    "vfxId": {
        "DisplayName": "Effect VFX [0]",
        "Description": "Special effect VfxId (-1 disabled)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14100",
        "ParamRef1": "SpEffectVfxParam"
    },
    "accumuOverFireId": {
        "DisplayName": "Accumulator - Over Value - SpEffect ID",
        "Description": "Special effect Id activated at the upper limit of the spirit ball",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "114200"
    },
    "accumuOverVal": {
        "DisplayName": "Accumulator - Over Value",
        "Description": "Genkitama upper limit",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "114100"
    },
    "accumuUnderFireId": {
        "DisplayName": "Accumulator - Under Value - SpEffect ID",
        "Description": "Special effect Id activated at the lower limit of the spirit ball",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "114400"
    },
    "accumuUnderVal": {
        "DisplayName": "Accumulator - Under Value",
        "Description": "Genkitama lower limit",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "114300"
    },
    "accumuVal": {
        "DisplayName": "Accumulator - Increment Value",
        "Description": "Genkitama accumulation value",
        "Minimum": "-99999999",
        "Maximum": "2100000000",
        "SortID": "114500"
    },
    "eye_angX": {
        "DisplayName": "Vision - Overwrite Height Angle",
        "Description": "Override the findability angle x",
        "Maximum": "180",
        "SortID": "73730"
    },
    "eye_angY": {
        "DisplayName": "Vision - Overwrite Width Angle",
        "Description": "Override the findability angle y",
        "Maximum": "180",
        "SortID": "73740"
    },
    "addDeceasedLv": {
        "DisplayName": "Add Deceased Level",
        "Description": "Add this value to the degree of death",
        "Minimum": "-999",
        "Maximum": "999",
        "SortID": "115000"
    },
    "vfxId1": {
        "DisplayName": "Effect VFX [1]",
        "Description": "Special effect VfxId1 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14110",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId2": {
        "DisplayName": "Effect VFX [2]",
        "Description": "Special effect VfxId2 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14120",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId3": {
        "DisplayName": "Effect VFX [3]",
        "Description": "Special effect VfxId3 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14130",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId4": {
        "DisplayName": "Effect VFX [4]",
        "Description": "Special effect VfxId4 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14140",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId5": {
        "DisplayName": "Effect VFX [5]",
        "Description": "Special effect VfxId5 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14150",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId6": {
        "DisplayName": "Effect VFX [6]",
        "Description": "Special effect VfxId6 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14160",
        "ParamRef1": "SpEffectVfxParam"
    },
    "vfxId7": {
        "DisplayName": "Effect VFX [7]",
        "Description": "Special effect VfxId7 (-1 invalid)",
        "Minimum": "-1",
        "Maximum": "2100000000",
        "SortID": "14170",
        "ParamRef1": "SpEffectVfxParam"
    },
    "freezeAttackPower": {
        "DisplayName": "Aux Inflict +: Frostbite",
        "Description": "Numerical value to be added to the target [Cold air resistance value] when hit\nRequires State Info 260",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "66200"
    },
    "AppearAiSoundId": {
        "DisplayName": "Generated AI Sound ID",
        "Description": "Generates AI sound parameters with set values",
        "Minimum": "0",
        "Maximum": "2100000000",
        "SortID": "75200"
    },
    "addFootEffectSfxId": {
        "DisplayName": "Automatic Foot Effect - SFX ID Offset",
        "Description": "The identifier of the foot effect that is additionally generated during special effects. XYYZZZ ZZZ",
        "Minimum": "-1",
        "Maximum": "999",
        "SortID": "14500",
        "ParamRef1": "FootSfxParam"
    },
    "dexterityCancelSystemOnlyAddDexterity": {
        "DisplayName": "Cast Speed +",
        "Description": "Add this value when calculating the end timing of the TAE flag of \"Skill Cancel\".",
        "Minimum": "-99",
        "Maximum": "99",
        "SortID": "410000"
    },
    "teamOffenseEffectivity": {
        "DisplayName": "Team Attack Effectivity",
        "Description": "Overwrite and change the target [Team Attack Influence] value. Do not change the default value (-1).",
        "Minimum": "-1",
        "Maximum": "100",
        "SortID": "75300"
    },
    "toughnessDamageCutRate": {
        "DisplayName": "Toughness Absorption %",
        "Description": "Toughness version cut rate",
        "Minimum": "0",
        "Maximum": "10",
        "Increment": "0.001",
        "SortID": "90500"
    },
    "weakDmgRateA": {
        "DisplayName": "Damage Multiplier %: Type A",
        "Description": "Special Attack A Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46500"
    },
    "weakDmgRateB": {
        "DisplayName": "Damage Multiplier %: Type B",
        "Description": "Special attack B Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46510"
    },
    "weakDmgRateC": {
        "DisplayName": "Damage Multiplier %: Type C",
        "Description": "Special attack C Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46520"
    },
    "weakDmgRateD": {
        "DisplayName": "Damage Multiplier %: Type D",
        "Description": "Special attack D Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46530"
    },
    "weakDmgRateE": {
        "DisplayName": "Damage Multiplier %: Type E",
        "Description": "Special attack E Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46540"
    },
    "weakDmgRateF": {
        "DisplayName": "Damage Multiplier %: Type F",
        "Description": "Special attack F Damage multiplier is corrected. 1 is normal.",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46550"
    },
    "darkDamageCutRate": {
        "DisplayName": "Absorption %: Holy",
        "Description": "Dark damage multiplier: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31200"
    },
    "darkDiffenceRate": {
        "DisplayName": "Defence %: Holy",
        "Description": "Multiply the darkness defense by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "43200"
    },
    "darkDiffence": {
        "DisplayName": "Defence +: Holy",
        "Description": "Add or subtract the value set for darkness defense",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46200"
    },
    "darkAttackRate": {
        "DisplayName": "Attack %: Holy",
        "Description": "Dark damage multiplier: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "34200"
    },
    "darkAttackPowerRate": {
        "DisplayName": "Power %: Holy",
        "Description": "Multiply the dark attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "37200"
    },
    "darkAttackPower": {
        "DisplayName": "Damage +: Holy",
        "Description": "Add or subtract the value set for the dark attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "40200"
    },
    "antiDarkSightRadius": {
        "DisplayName": "Full View in Darkness - Radius",
        "Description": "Radius of full view of darkness [m]. If you are within this distance, you will be able to see at normal distance even in the dark.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "150000"
    },
    "antiDarkSightDmypolyId": {
        "DisplayName": "Full View in Darkness - Dummy Poly ID",
        "Description": "Damipoli ID (-1: Master) with full view of darkness. Create a full view area around this Damipoli",
        "Minimum": "-1",
        "Maximum": "99999",
        "SortID": "151000"
    },
    "conditionHpRate": {
        "DisplayName": "Trigger on HP Above %",
        "Description": "Activates only when you have HP above the specified value",
        "Minimum": "-1",
        "Maximum": "100",
        "SortID": "18500"
    },
    "consumeStaminaRate": {
        "DisplayName": "Weapon Stamina Consumption %",
        "Description": "Multiply by multiplying the consumption stamina value of the behavior parameter",
        "Minimum": "0",
        "Maximum": "99.99",
        "SortID": "55900"
    },
    "itemDropRate": {
        "DisplayName": "Item Discovery %",
        "Description": "The set value is added to [Item Drop Correction]\nRequires State Info 66",
        "Minimum": "-99.99",
        "Maximum": "99.99",
        "SortID": "72500"
    },
    "changePoisonResistPoint": {
        "DisplayName": "Aux Resist +: Poison",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89000"
    },
    "changeDiseaseResistPoint": {
        "DisplayName": "Aux Resist +: Scarlet Rot",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89100"
    },
    "changeBloodResistPoint": {
        "DisplayName": "Aux Resist +: Hemorrhage",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89200"
    },
    "changeCurseResistPoint": {
        "DisplayName": "Aux Resist +: Blight",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89300"
    },
    "changeFreezeResistPoint": {
        "DisplayName": "Aux Resist +: Frostbite",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89400"
    },
    "slashAttackRate": {
        "DisplayName": "Attack %: Slash",
        "Description": "Slash damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "32100"
    },
    "blowAttackRate": {
        "DisplayName": "Attack %: Strike",
        "Description": "Batter damage ratio: The calculated damage is corrected by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "32200"
    },
    "thrustAttackRate": {
        "DisplayName": "Attack %: Thrust",
        "Description": "Puncture damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "32300"
    },
    "neutralAttackRate": {
        "DisplayName": "Attack %: Standard",
        "Description": "Non-attribute damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "32400"
    },
    "slashAttackPowerRate": {
        "DisplayName": "Power %: Slash",
        "Description": "Multiply the slashing attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "35100"
    },
    "blowAttackPowerRate": {
        "DisplayName": "Power %: Strike",
        "Description": "Multiply the hit attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "35200"
    },
    "thrustAttackPowerRate": {
        "DisplayName": "Power %: Thrust",
        "Description": "Multiply the piercing attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "35300"
    },
    "neutralAttackPowerRate": {
        "DisplayName": "Power %: Standard",
        "Description": "Multiply the non-attribute attack power by the set value",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "35400"
    },
    "slashAttackPower": {
        "DisplayName": "Damage +: Slash",
        "Description": "Add or subtract the value set for the slashing attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "38100"
    },
    "blowAttackPower": {
        "DisplayName": "Damage +: Strike",
        "Description": "Add or subtract the value set for the batter attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "38200"
    },
    "thrustAttackPower": {
        "DisplayName": "Damage +: Thrust",
        "Description": "Add or subtract the value set for the piercing attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "38300"
    },
    "neutralAttackPower": {
        "DisplayName": "Damage +: Standard",
        "Description": "Add or subtract the value set for non-attribute attack power",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "38400"
    },
    "changeStrengthPoint": {
        "DisplayName": "Correction +: STR",
        "Description": "Add or subtract the correction value of the weapon",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46600"
    },
    "changeAgilityPoint": {
        "DisplayName": "Correction +: DEX",
        "Description": "Add or subtract the correction value of the weapon",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46610"
    },
    "changeMagicPoint": {
        "DisplayName": "Correction +: INT",
        "Description": "Add or subtract the correction value of the weapon",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46700"
    },
    "changeFaithPoint": {
        "DisplayName": "Correction +: FTH",
        "Description": "Add or subtract the correction value of the weapon",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46800"
    },
    "changeLuckPoint": {
        "DisplayName": "Correction +: ARC",
        "Description": "Add or subtract the correction value of the weapon",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "46900"
    },
    "recoverArtsPoint_Str": {
        "DisplayName": "Weapon Art Restore: STR",
        "Description": "Arts Point Restores strength",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "153000"
    },
    "recoverArtsPoint_Dex": {
        "DisplayName": "Weapon Art Restore: DEX",
        "Description": "Restores arts point workmanship",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "153100"
    },
    "recoverArtsPoint_Magic": {
        "DisplayName": "Weapon Art Restore: INT",
        "Description": "Restores arts point magic",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "153200"
    },
    "recoverArtsPoint_Miracle": {
        "DisplayName": "Weapon Art Restore: FTH",
        "Description": "Recover arts point miracles",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "153300"
    },
    "madnessDamageRate": {
        "DisplayName": "Damage Correction %: Madness",
        "Description": "Correction value used only for point damage and% damage of state change type [madness]",
        "SortID": "90300"
    },
    "isUseStatusAilmentAtkPowerCorrect": {
        "DisplayName": "Use Status Ailment Attack Power Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If ○, the abnormal state attack power multiplier correction of the attack para is applied.",
        "Maximum": "1",
        "SortID": "17500"
    },
    "isUseAtkParamAtkPowerCorrect": {
        "DisplayName": "Use AtkParam Attack Power Correction",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If ○, the attack power multiplier correction of the attack para is applied.",
        "Maximum": "1",
        "SortID": "17550"
    },
    "dontDeleteOnDead": {
        "DisplayName": "Don't Delete on Dead",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If it is ○, it will not be deleted even if the character dies. Mainly used for death effects.",
        "Maximum": "1",
        "SortID": "20500"
    },
    "disableFreeze": {
        "DisplayName": "Disable Frostbite",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "When this effect is applied, it will not be cold",
        "Maximum": "1",
        "SortID": "104060"
    },
    "isDisableNetSync": {
        "DisplayName": "Do not Sync in Multiplayer",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Do not synchronize with the net. It does not mean that you will be able to call it locally, but simply do not send it online. For example, a remote character does not activate locally, so nothing happens in that case.",
        "Maximum": "1",
        "SortID": "420000"
    },
    "shamanParamChange": {
        "DisplayName": "Affects Pyromancy",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Set whether or not it is effective against spells",
        "Maximum": "1",
        "SortID": "26100"
    },
    "isStopSearchedNotify": {
        "DisplayName": "Stop Platoon Notifications",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Whether to stop notifications targeting your army (used by EventMaker decisions and buddy platoons)",
        "Maximum": "1",
        "SortID": "75500"
    },
    "isCheckAboveShadowTest": {
        "DisplayName": "Apply outside of Rain Shield",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If it is ○, it will not be applied when it is judged to be shielded (× is always applied)",
        "Maximum": "1",
        "SortID": "450000"
    },
    "addBehaviorJudgeId_add": {
        "DisplayName": "Add Behavior Judgment ID - Addition Value",
        "Description": "If the addition value of the action judgment ID is 0, the action is not switched and the action is stopped.",
        "Maximum": "999",
        "SortID": "114001"
    },
    "saReceiveDamageRate": {
        "DisplayName": "Absorption %: Poise Damage",
        "Description": "Multiplier for SA damage",
        "Minimum": "0",
        "Maximum": "100",
        "Increment": "0.1",
        "SortID": "90800"
    },
    "defPlayerDmgCorrectRate_Physics": {
        "DisplayName": "PVP Absorption %: Physical",
        "Description": "Damage correction for the damage value received from the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46300"
    },
    "defPlayerDmgCorrectRate_Magic": {
        "DisplayName": "PVP Absorption %: Magic",
        "Description": "Damage correction for the damage value received from the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46310"
    },
    "defPlayerDmgCorrectRate_Fire": {
        "DisplayName": "PVP Absorption %: Fire",
        "Description": "Damage correction for the damage value received from the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46320"
    },
    "defPlayerDmgCorrectRate_Thunder": {
        "DisplayName": "PVP Absorption %: Lightning",
        "Description": "Damage correction for the damage value received from the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46330"
    },
    "defPlayerDmgCorrectRate_Dark": {
        "DisplayName": "PVP Absorption %: Holy",
        "Description": "Damage correction for the damage value received from the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46340"
    },
    "defEnemyDmgCorrectRate_Physics": {
        "DisplayName": "Absorption %: Physical",
        "Description": "Damage correction for the damage value received from the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46350"
    },
    "defEnemyDmgCorrectRate_Magic": {
        "DisplayName": "Absorption %: Magic",
        "Description": "Damage correction for the damage value received from the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46360"
    },
    "defEnemyDmgCorrectRate_Fire": {
        "DisplayName": "Absorption %: Fire",
        "Description": "Damage correction for the damage value received from the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46370"
    },
    "defEnemyDmgCorrectRate_Thunder": {
        "DisplayName": "Absorption %: Lightning",
        "Description": "Damage correction for the damage value received from the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46380"
    },
    "defEnemyDmgCorrectRate_Dark": {
        "DisplayName": "Absorption %: Holy",
        "Description": "Damage correction for the damage value received from the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46390"
    },
    "defObjDmgCorrectRate": {
        "DisplayName": "Absorption %: Object",
        "Description": "Damage correction for the damage value received from OBJ.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46400"
    },
    "atkPlayerDmgCorrectRate_Physics": {
        "DisplayName": "PVP Damage %: Physical",
        "Description": "Damage correction for the damage value given to the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46290"
    },
    "atkPlayerDmgCorrectRate_Magic": {
        "DisplayName": "PVP Damage %: Magic",
        "Description": "Damage correction for the damage value given to the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46291"
    },
    "atkPlayerDmgCorrectRate_Fire": {
        "DisplayName": "PVP Damage %: Fire",
        "Description": "Damage correction for the damage value given to the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46292"
    },
    "atkPlayerDmgCorrectRate_Thunder": {
        "DisplayName": "PVP Damage %: Lightning",
        "Description": "Damage correction for the damage value given to the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46293"
    },
    "atkPlayerDmgCorrectRate_Dark": {
        "DisplayName": "PVP Damage %: Holy",
        "Description": "Damage correction for the damage value given to the player.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46294"
    },
    "atkEnemyDmgCorrectRate_Physics": {
        "DisplayName": "Damage %: Physical",
        "Description": "Damage correction for the damage value given to the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46295"
    },
    "atkEnemyDmgCorrectRate_Magic": {
        "DisplayName": "Damage %: Magic",
        "Description": "Damage correction for the damage value given to the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46296"
    },
    "atkEnemyDmgCorrectRate_Fire": {
        "DisplayName": "Damage %: Fire",
        "Description": "Damage correction for the damage value given to the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46297"
    },
    "atkEnemyDmgCorrectRate_Thunder": {
        "DisplayName": "Damage %: Lightning",
        "Description": "Damage correction for the damage value given to the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46298"
    },
    "atkEnemyDmgCorrectRate_Dark": {
        "DisplayName": "Damage %: Holy",
        "Description": "Damage correction for the damage value given to the enemy.",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "46299"
    },
    "registFreezeChangeRate": {
        "DisplayName": "Aux Resist %: Frostbite",
        "Description": "Multiply the cold resistance value by the set magnification",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88400"
    },
    "invocationConditionsStateChange1": {
        "DisplayName": "Trigger on State Info [1]",
        "Enum": "SP_EFFECT_TYPE",
        "Description": "Trigger condition state change type 1",
        "Maximum": "60000",
        "SortID": "165100"
    },
    "invocationConditionsStateChange2": {
        "DisplayName": "Trigger on State Info [2]",
        "Enum": "SP_EFFECT_TYPE",
        "Description": "Trigger condition state change type 2",
        "Maximum": "60000",
        "SortID": "165200"
    },
    "invocationConditionsStateChange3": {
        "DisplayName": "Trigger on State Info [3]",
        "Enum": "SP_EFFECT_TYPE",
        "Description": "Trigger condition state change type 3",
        "Maximum": "60000",
        "SortID": "165300"
    },
    "hearingAiSoundLevel": {
        "DisplayName": "Listen - AI Sound Level",
        "Description": "Overwrite how good your ears are",
        "Minimum": "-1",
        "Maximum": "128",
        "SortID": "73850"
    },
    "chrProxyHeightRate": {
        "DisplayName": "Proxy Height Capsule %",
        "Description": "Magnification over the height of the character capsule",
        "DisplayFormat": "%0.2f",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "75700"
    },
    "addAwarePointCorrectValue_forMe": {
        "DisplayName": "Search Awareness - Addition Correction - Self",
        "Description": "Search side addition correction_viewer",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73500"
    },
    "addAwarePointCorrectValue_forTarget": {
        "DisplayName": "Search Awareness - Addition Correction - Target",
        "Description": "Searching degree addition correction _ side to be seen",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73510"
    },
    "sightSearchEnemyAdd": {
        "DisplayName": "Vision Search - Enemy Addition",
        "Description": "Correct the ease of finding with a real number",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73610"
    },
    "sightSearchAdd": {
        "DisplayName": "Vision Search Addition",
        "Description": "Correct the ease of finding with a real number",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73710"
    },
    "hearingSearchAdd": {
        "DisplayName": "Listen Search Addition",
        "Description": "Correct the hearing of AI sounds with real numbers",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73810"
    },
    "hearingSearchRate": {
        "DisplayName": "Listen Search Correction",
        "Description": "Correct the audibility of AI sound by magnification",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "73820"
    },
    "hearingSearchEnemyAdd": {
        "DisplayName": "Listen Search - Enemy Addition",
        "Description": "Correct the loudness of the emitted AI sound with a real number",
        "DisplayFormat": "%0.2f",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "73910"
    },
    "value_Magnification": {
        "DisplayName": "Sale Price Correction %",
        "Description": "Sales price correction: Magnification",
        "Minimum": "1",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "200000"
    },
    "artsConsumptionRate": {
        "DisplayName": "Skill FP Consumption %",
        "Description": "Arts MP consumption multiplier [%]",
        "Minimum": "0",
        "Maximum": "990",
        "Increment": "0.001",
        "SortID": "300000"
    },
    "magicConsumptionRate": {
        "DisplayName": "Sorcery FP Consumption %",
        "Description": "Magic consumption MP multiplier [%]",
        "Minimum": "0",
        "Maximum": "990",
        "Increment": "0.001",
        "SortID": "300010"
    },
    "shamanConsumptionRate": {
        "DisplayName": "Pyromancy FP Consumption %",
        "Description": "Magic consumption MP multiplier [%]",
        "Minimum": "0",
        "Maximum": "990",
        "Increment": "0.001",
        "SortID": "300020"
    },
    "miracleConsumptionRate": {
        "DisplayName": "Incantation FP Consumption %",
        "Description": "Miracle consumption MP magnification [%]",
        "Minimum": "0",
        "Maximum": "990",
        "Increment": "0.001",
        "SortID": "300030"
    },
    "changeHpEstusFlaskRate": {
        "DisplayName": "HP Flask - HP Restore %",
        "Description": "Set what percentage of the maximum HP to add (or subtract) with one activation",
        "Minimum": "-100",
        "Maximum": "100",
        "SortID": "55200"
    },
    "changeHpEstusFlaskPoint": {
        "DisplayName": "HP Flask - HP Restore +",
        "Description": "Set how many points to add (or subtract) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "55210"
    },
    "changeMpEstusFlaskRate": {
        "DisplayName": "FP Flask - FP Restore %",
        "Description": "Set what percentage of the maximum MP to add (or subtract) with one activation",
        "Minimum": "-100",
        "Maximum": "100",
        "SortID": "55220"
    },
    "changeMpEstusFlaskPoint": {
        "DisplayName": "FP Flask - FP Restore +",
        "Description": "Set how many points to add (or subtract) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "SortID": "55230"
    },
    "changeHpEstusFlaskCorrectRate": {
        "DisplayName": "HP Flask - HP Restore Correction",
        "Description": "Correct the damage amount of the HP Est bottle",
        "Minimum": "0",
        "Maximum": "99999",
        "Increment": "0.001",
        "SortID": "55240"
    },
    "changeMpEstusFlaskCorrectRate": {
        "DisplayName": "FP Flask - HP Restore Correction",
        "Description": "Correct the damage amount of MP Est Bottle",
        "Minimum": "0",
        "Maximum": "99999",
        "Increment": "0.001",
        "SortID": "55250"
    },
    "applyIdOnGetSoul": {
        "DisplayName": "Kill SpEffect ID",
        "Description": "When the special effect of the state change type \"HP drain\" is enabled, when the enemy is defeated, the special effect ID set in the \"HP drain activation special effect\" of the same special effect is called (0: ignore).",
        "Minimum": "0",
        "Maximum": "2100000000",
        "SortID": "111030",
        "ParamRef1": "SpEffectParam"
    },
    "extendLifeRate": {
        "DisplayName": "Extend SpEffect Duration %",
        "Description": "Extension coefficient of state change type \"life extension\"",
        "Minimum": "0",
        "Maximum": "9900",
        "SortID": "105101"
    },
    "contractLifeRate": {
        "DisplayName": "Contract SpEffect Duration %",
        "Description": "Shortening coefficient of state change type \"life shortening\"",
        "Minimum": "0",
        "Maximum": "9900",
        "SortID": "105111"
    },
    "defObjectAttackPowerRate": {
        "DisplayName": "Object Damage %",
        "Description": "Corrects the attack power against the damage received from OBJ. (Not damage compensation)",
        "DisplayFormat": "%0.3f",
        "Minimum": "0",
        "Maximum": "99.999",
        "Increment": "0.001",
        "SortID": "46450"
    },
    "effectEndDeleteDecalGroupId": {
        "DisplayName": "Decal Deletion Group ID",
        "Description": "When the special effect disappears (lifetime / overwritten / erased ... etc.), the paint decal is deleted if the special effect of the same group ID is not applied.",
        "Minimum": "-1",
        "Maximum": "9999",
        "SortID": "410000"
    },
    "addLifeForceStatus": {
        "DisplayName": "Vigor",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401000"
    },
    "addWillpowerStatus": {
        "DisplayName": "Mind",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401100"
    },
    "addEndureStatus": {
        "DisplayName": "Endurance",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401200"
    },
    "addVitalityStatus": {
        "DisplayName": "Vitality",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401300"
    },
    "addStrengthStatus": {
        "DisplayName": "Strength",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401400"
    },
    "addDexterityStatus": {
        "DisplayName": "Dexterity",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401500"
    },
    "addMagicStatus": {
        "DisplayName": "Intelligence",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401600"
    },
    "addFaithStatus": {
        "DisplayName": "Faith",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401700"
    },
    "addLuckStatus": {
        "DisplayName": "Arcane",
        "Description": "Add value to growth status",
        "Minimum": "0",
        "Maximum": "99",
        "SortID": "401800"
    },
    "deleteCriteriaDamage": {
        "DisplayName": "Delete Criteria Damage",
        "Enum": "SP_EFFECT_PARAM_DELETE_DAMAGE_TYPE",
        "Description": "Reason for damage under the condition to remove special effects",
        "SortID": "18600"
    },
    "magicSubCategoryChange3": {
        "DisplayName": "Conditional Category [3]",
        "Enum": "ATK_SUB_CATEGORY",
        "Description": "Vs to subcategory parameter change 3",
        "SortID": "26320"
    },
    "spAttributeVariationValue": {
        "DisplayName": "SpEffect Attribute Variation Value",
        "Description": "This value is used to give variation to abnormal state SFX, SE, etc. in combination with the special attribute set for the special effect. SEQ16473",
        "Maximum": "99",
        "SortID": "27501"
    },
    "atkFlickPower": {
        "DisplayName": "Weapon Repel Power +",
        "Description": "Set a value that overwrites the repelling attack power",
        "SortID": "27505"
    },
    "wetConditionDepth": {
        "DisplayName": "Wet Condition Depth",
        "Enum": "SP_EFFECT_WET_CONDITION_DEPTH",
        "Description": "TimeAct Determines whether special effects are applied in combination with \"at what water level you get wet\"",
        "SortID": "460000"
    },
    "changeSaRecoveryVelocity": {
        "DisplayName": "Poise Recovery Time %",
        "Description": "Change the recovery speed of SA durability",
        "Minimum": "-99.99",
        "Maximum": "99.99",
        "Increment": "0.1",
        "SortID": "58300"
    },
    "regainRate": {
        "DisplayName": "Regain Correction %",
        "Description": "Regain magnification",
        "Minimum": "0",
        "Maximum": "99.99",
        "SortID": "162000"
    },
    "saAttackPowerRate": {
        "DisplayName": "Poise Damage %",
        "Description": "SA attack power multiplier",
        "Minimum": "0",
        "Maximum": "99",
        "Increment": "0.1",
        "SortID": "58400"
    },
    "sleepAttackPower": {
        "DisplayName": "Aux Inflict +: Sleep",
        "Description": "Numerical value to be added to the target's [Sleep tolerance] when hit",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "66300"
    },
    "madnessAttackPower": {
        "DisplayName": "Aux Inflict +: Madness",
        "Description": "A number to be added to the target's [madness resistance value] when it hits",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "66400"
    },
    "registSleepChangeRate": {
        "DisplayName": "Aux Resist %: Sleep",
        "Description": "Multiply the sleep tolerance value by the set magnification",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88500"
    },
    "registMadnessChangeRate": {
        "DisplayName": "Aux Resist %: Madness",
        "Description": "Multiply the madness resistance value by the set multiplier",
        "Minimum": "-1",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "88600"
    },
    "changeSleepResistPoint": {
        "DisplayName": "Aux Resist +: Sleep",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89500"
    },
    "changeMadnessResistPoint": {
        "DisplayName": "Aux Resist +: Madness",
        "Description": "Increase or decrease the state resistance value",
        "Minimum": "-99999",
        "Maximum": "99999",
        "SortID": "89600"
    },
    "sleepDamageRate": {
        "DisplayName": "Damage Correction %: Sleep",
        "Description": "Point damage of state change type [Sleep], correction value used only when% damage",
        "SortID": "90200"
    },
    "applyPartsGroup": {
        "DisplayName": "Apply Parts Group",
        "Enum": "SP_EFFECT_APPLY_PARTS_GROUP",
        "Description": "The effect is limited by the part where the attack hits. Only defensive items in damage calculation are subject to restriction",
        "Maximum": "31",
        "SortID": "26400"
    },
    "clearTarget": {
        "DisplayName": "Clear Target",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "Does not recognize the target while the special effect is applied (excluding the riding target)",
        "Maximum": "1",
        "SortID": "72710"
    },
    "fakeTargetIgnoreAjin": {
        "DisplayName": "Ignore Fake Target - Human",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "You will not be caught by the fake target of the subhuman system that occurred",
        "Maximum": "1",
        "SortID": "96602"
    },
    "fakeTargetIgnoreMirageArts": {
        "DisplayName": "Ignore Fake Target - Phantom",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "You will not be caught by the fake target of the phantom arts system that occurred",
        "Maximum": "1",
        "SortID": "96604"
    },
    "requestForceJoinBlackSOS_B": {
        "DisplayName": "Force Invasion",
        "Enum": "SP_EFFECT_BOOL",
        "Description": "If checked, issue an intrusion_B request when activated",
        "Maximum": "1",
        "SortID": "78100"
    },
    "unk353_4": {
        "DisplayName": "Blank",
        "Enum": "SP_EFFECT_BOOL",
        "Maximum": "1"
    },
    "pad2[1]": {
        "DisplayName": "pad",
        "SortID": "470001"
    },
    "changeSuperArmorPoint": {
        "DisplayName": "Poise +",
        "Description": "Value to add to the super armor value",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "58100"
    },
    "changeSaPoint": {
        "DisplayName": "Apply Poise Damage +",
        "Description": "Set how many points to subtract (or add) with one activation",
        "Minimum": "-9999",
        "Maximum": "9999",
        "Increment": "0.1",
        "SortID": "58200"
    },
    "hugeEnemyPickupHeightOverwrite": {
        "DisplayName": "Giant Enemy Height Overwrite",
        "Description": "Giant enemy lift height overwrite [m]",
        "Minimum": "0",
        "Maximum": "99.9",
        "Increment": "0.1",
        "SortID": "470000"
    },
    "poisonDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Poison",
        "Description": "Poison resistance damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31300"
    },
    "diseaseDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Scarlet Rot",
        "Description": "Epidemic resistance damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31400"
    },
    "bloodDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Hemorrhage",
        "Description": "Bleeding resistance damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31500"
    },
    "curseDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Blight",
        "Description": "Curse resistance damage multiplier: Corrects the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31600"
    },
    "freezeDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Frostbite",
        "Description": "Cold resistance damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31700"
    },
    "sleepDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Sleep",
        "Description": "Sleep resistance damage ratio: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31800"
    },
    "madnessDefDamageRate": {
        "DisplayName": "Aux Damage Correction %: Madness",
        "Description": "Madness resistance damage multiplier: Correct the calculated damage by XX times. 1 is normal.",
        "Minimum": "-99",
        "Maximum": "99",
        "Increment": "0.001",
        "SortID": "31900"
    },
    "overwrite_maxBackhomeDist": {
        "DisplayName": "Override - Max Back Home Distance",
        "Description": "Distance to go home no matter what [m] _ overwrite",
        "SortID": "74000"
    },
    "overwrite_backhomeDist": {
        "DisplayName": "Override - Back Home Distance",
        "Description": "Distance to return home while fighting [m] _ Overwrite",
        "SortID": "74010"
    },
    "overwrite_backhomeBattleDist": {
        "DisplayName": "Override - Back Home Battle Distance",
        "Description": "Distance to give up and fight to return to the nest [m] _ overwrite",
        "SortID": "74020"
    },
    "overwrite_BackHome_LookTargetDist": {
        "DisplayName": "Override - Look Target Distance",
        "Description": "When returning home: Distance to see the target [m] _ Overwrite",
        "SortID": "74030"
    },
    "goodsConsumptionRate": {
        "DisplayName": "Item FP Consumption %",
        "Description": "Item consumption MP multiplier",
        "Minimum": "0",
        "Maximum": "990",
        "Increment": "0.001",
        "SortID": "300040"
    },
    "pad3[8]": {
        "DisplayName": "pad",
        "DisplayFormat": "%f",
        "EditFlags": "Wrap",
        "SortID": "470002"
    }
}