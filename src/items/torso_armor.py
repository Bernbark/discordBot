from src.items.armor import Armor


class TorsoArmor(Armor):
    def __init__(self, item_id: str, name: str = "Torso Armor", cost: int = 5000,
                 description: str = "It better protect me...", defense: int = 2):
        self.type = "torso"
        super(TorsoArmor, self).__init__(item_id,name,cost,description,defense)

