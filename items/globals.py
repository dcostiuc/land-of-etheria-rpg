from .item import Item
from .weapon import Weapon
from .potion import Potion
from .effect import Effect
from .armor import Armor


# Player Starting Items
fists = Weapon("Fists", -1, 2, 0)
cloth = Armor("Torn Cloth", 0, 0, 0)
#############################

#### Initializing items ####
stickName = "A Sharp Stick"
stickRarity = 1
stickDmg = 1

stick = Weapon(stickName, stickRarity, stickDmg, 0)

#############################

# General Consumables
burnDesc = "For 3 turns, the enemy takes 3 Damage."
burnEffect = Effect("Burning", burnDesc, 3, 3, "enemy")
burnEffect.effectActivator = "dmg"

potFlames = Potion("Potion of Flames", 3, burnEffect)

regenDesc = "The player will be healed for 2-5 HP for 4 turns."
regenEffect = Effect("Regeneration", regenDesc, 4, 5, "player", True)
regenEffect.setRandLimits(2, 5)
regenEffect.effectActivator = "heal"

elixirRecov = Potion("Elixir of Recovery", 4, regenEffect)

# Bat Items
claw = Weapon("Small Claw", 2, 3, 0)
batBat = Weapon("The Bat Bat", 6, 10, 0)
batWing = Item("Bat Wing", 2)
vampArmor = Armor("Vampiric Sheath", 5, 4, 0)

# Serpent Items
fang = Item("Snake Fang", 2)
eyeSerpent = Item("Eye of the Serpent", 3)
vipBlade = Weapon("Viperous Blade", 4, 6, 0)
snakeHide = Armor("Snakeskin Hide", 3, 5, 0)

venomDesc = "Poisons the target for 4 Damage, lasting 1 turn."
venomEffect = Effect("Venom", venomDesc, 1, 4, "enemy")
venomEffect.effectActivator = "dmg"
vileVenom = Potion("Vial of Venom", 4, venomEffect)

# Ant Army Items
bottleAnts = Item("Bottle of Ants", 4)
deadAnt = Item("Dead Ant", 1)
giantPincers = Weapon("Giant Pincers", 3, 3, 0)

# Dust Elemental Items
elemSoul = Item("Elemental Soul", 3)

# Creature of the Depths Items
organs = Item("Noxious Intestinal Organs", 0)
skull = Item("Fiendish Skull", 1)
slayerBeast = Weapon("Slayer of the Beast", 3, 7, 1)
spikedPelt = Armor("Spiked Pelt", 2, 4, 0)

furyDesc = "The player’s next 3 attacks will deal x2 Damage."
furyEffect = Effect("Growing Rage", furyDesc, 4, 2, "player")
furyEffect.effectActivator = "dmginc"

potFury = Potion("Potion of Fury", 5, furyEffect)

# TREANT Items
timber = Item("Ghostly Timber", 4)
lumber = Item("Lumber", 1)
clubThorns = Weapon("Club of Thorns", 3, 7, 0)
protEffectDesc = "Once per battle, restore 3-7 HP."
protectorEffect = Effect("Essence of the Forest", protEffectDesc, 1, 7, "player", True)
protectorEffect.setRandLimits(3, 7)
protectorEffect.effectActivator = "heal"

protector = Armor("Woodlandian Protector", 4, 5, 0, protectorEffect)

# QUEEN BEE Items
nectar = Item("Candy-Coated Nectar", 2)
honeycomb = Item("Hulking Honeycomb", 1)
sting = Weapon("The Empress' Sting", 4, 8, 0)

sweetDesc = "Heals the player for 3-4 HP."
sweetEffect = Effect("Sweetness", sweetDesc, 1, 4, "player", True)
sweetEffect.setRandLimits(3, 4)
sweetEffect.effectActivator = "heal"
sweetEffect.oneUse = True

jarHoney = Potion("Jar of Luscious Honey", 3, sweetEffect)

# Initializing Potions
# hpPot = Potion("Healing Potion", 2, heal(10))
# flamePot = Potion("Potion of Flames", 4, dmg(15, hjk))
