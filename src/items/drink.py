from src.items.food import Food


class Drink(Food):
    """
    Drinks should have special properties beyond normal food, but it's not implemented yet.
    """
    def __init__(self, name: str = "Tasty Beverage?", cost: int = 5000,
                 description: str = "I hope it tastes better than it looks...",
                 healing: int = 10, stamina: int = 10):
        super().__init__(name, cost, description, healing, stamina)

    # Create buff and add it

