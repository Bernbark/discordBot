import random

from src.items.food import Food
from src.items.drink import Drink
from src.items.weapon import Weapon


suffixes = {
    "Shadowmaster":[5,20000],
    "Deathbringer":[10,40000],
    "The Avalanche":[8, 30000],
    "Dark Weaver":[3, 10000],
    "The Omen":[7, 25000],
    "Regret":[-1,1000],
    "Harmony":[10, 30000],
    "Disgrace":[-2,5000],
    "Honorbound":[6, 27000],
    "The Reaper":[15,75000],
}

prefixes = [
    "Disturbing",
    "Powerful",
    "Wicked",
    "Enchanted",
    "Cursed",
    "Simple",
    "Broken",
    "Polished"
]

weaponNames = [
    "Great Axe",
    "Sub-machine Gun",
    "Longbow",
    "Dart gun",
    "Dagger",
    "Sword",
    "Mace",
    "Maul",
    "Claws",
    "Scepter"
]

foodNames = [
    "Banana",
    "Apple",
    "Pizza"
]

drinkNames = [
    "Smoothie",
    "Alcohol",
    "Soda"
]

MIN_COST = 100
MAX_COST = 10000

MINIMUM_FOOD_HEALING = 100
MAX_FOOD_HEALING = 500

MIN_STAMINA_HEALING = 5
MAX_STAMINA_HEALING = 20


def randomize_food() -> Food:
    name = random.choice(foodNames)
    cost = random.randint(MIN_COST, MAX_COST)
    healing = random.randint(MINIMUM_FOOD_HEALING, MAX_FOOD_HEALING)
    stamina = random.randint(MIN_STAMINA_HEALING, MAX_STAMINA_HEALING)
    food = Food(name, cost, "No description properly serves this right.", healing, stamina)
    if food.rarity.value == 1:
        return food
    else:
        food.set_cost(food.cost * food.rarity.value)
        return food


def randomize_drink() -> Drink:
    name = random.choice(drinkNames)
    cost = random.randint(MIN_COST, MAX_COST)
    healing = random.randint(MINIMUM_FOOD_HEALING, MAX_FOOD_HEALING)
    stamina = random.randint(MIN_STAMINA_HEALING, MAX_STAMINA_HEALING)
    drink = Drink(name, cost, "No description properly serves this right.", healing, stamina)
    if drink.rarity.value == 1:
        return drink
    else:
        drink.set_cost(drink.cost * drink.rarity.value)
        return drink


def assign_prefixes(weapon,num) -> Weapon:
    randomNum = random.randint(1, num)
    for i in range(0, randomNum):
        weapon.set_prefix(random.choice(prefixes))
    return weapon


def assign_suffixes(weapon,num) -> Weapon:
    randomNum = random.randint(1, num)
    suffNames = []
    for i in range(0, randomNum):
        suffNames.append(random.choice(list(suffixes.keys())))
        weapon.set_suffixes(suffNames,suffixes)
    return weapon


def randomize_weapon():
    weapon = Weapon(random.choice(weaponNames))
    if weapon.rarity.value == 1:
        return weapon
    elif weapon.rarity.value == 2:
        weapon.set_prefix(random.choice(prefixes))
        suffNames = [random.choice(list(suffixes.keys()))]
        weapon.set_suffixes(suffNames,suffixes)
    else:
        weapon = assign_prefixes(weapon, weapon.rarity.value)
        weapon = assign_suffixes(weapon, weapon.rarity.value)
    weapon.set_dmg(weapon.damage * weapon.rarity.value)
    weapon.set_cost(weapon.cost * weapon.rarity.value)
    # Let's make this a separate value so we can show how much an item is being boosted beyond its normal stats.
    dmg = 0
    cost = 0
    for numArray in weapon.suffixes.values():
        cost += numArray[1]
        dmg += numArray[0]
    weapon.damage += dmg
    weapon.cost += cost
    weapon.adjust_name_for_prefsuf()
    return weapon

