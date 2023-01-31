import random
from enum import Enum


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    
    @classmethod
    def random(cls) -> 'Rarity':
        """
        Turn the Enum Rarity into a list and pick a random one from it
        :return: random Rarity
        """
        return random.choice(list(cls))


class Item:
    """
    Base class for Items, from here we build up and make food, drinks, armor, and weapons
    """
    def __init__(self, item_id: str = "", name: str = "Default Item", cost: int = 999, description: str = "Unknown"):
        self.rarity = Rarity.random()
        self.name = name
        self.cost = cost
        self.description = description
        self.item_id = item_id
        self.type = "Item"

    def set_cost(self, cost):
        self.cost = cost

    def set_description(self, description):
        self.description = description

