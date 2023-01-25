import random

from src.items.food import Food
from src.items.drink import Drink

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


def randomize_food():
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


def randomize_drink():
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