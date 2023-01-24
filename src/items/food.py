from src.items.item import Item


class Food(Item):
    """
    Food class to determine value of food
    """
    def __init__(self, name, cost, description, healing: int = 5, stamina: int = 5):
        super().__init__(name, cost, description)
        self.healing = healing
        self.stamina = stamina
