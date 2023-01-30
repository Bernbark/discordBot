from src.items.item import Item


class Armor(Item):
    def __init__(self, item_id: str, name: str = "Shiny Armor", cost: int = 5000,
                 description: str = "It better protect me...", defense: int = 1):
        super(Armor, self).__init__(item_id,name,cost,description)
        self.defense = defense

