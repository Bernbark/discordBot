from src.items.item import Item


class Food(Item):
    """
    Food class to determine value of food
    """
    def __init__(self, item_id: str, name: str = "Food", cost: int = 200, description: str = "Unknown",
                 healing: int = 5, stamina: int = 5):
        super().__init__(item_id, name, cost, description)
        self.healing = healing
        self.stamina = stamina
