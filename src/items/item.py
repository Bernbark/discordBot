import random
from enum import Enum


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


def assign_rarity():
    """
    Turn the Enum Rarity into a list and pick a random one from it
    :return: random Rarity
    """
    return random.choice(list(Rarity))
    # for data in Rarity:
    #    if randomNum == data.value:
    #        return data
    #    else:
    #        return Rarity.COMMON


class Item:
    """
    Base class for Items, from here we build up and make food, drinks, armor, and weapons
    """
    def __init__(self, name: str = "Default Item", cost: int = 999, description: str = "Unknown"):
        self.rarity = assign_rarity()
        self.name = name
        self.cost = cost
        self.description = description

    def set_cost(self, cost):
        self.cost = cost

    def set_description(self, description):
        self.description = description

