class Item:
    """
    Base class for Items, from here we build up and make food, drinks, armor, and weapons
    """
    def __init__(self, name: str = "Default Item", cost: int = 999, description: str = "Unknown"):
        # self.rarity = SOME RANDOM RARITY
        self.name = name
        self.cost = cost
        self.description = description
