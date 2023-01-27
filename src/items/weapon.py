from src.items.item import Item

# Let's make a double prefix/suffix situation, where if you have two of the same prefix, the weapon gets a big buff
class Weapon(Item):
    """
    Weapon class to hold weapon stats
    """
    def __init__(self, item_id: str, name: str = "Weapon", cost: int = 200, description: str = "Unknown",
                 dmg: int = 5):
        super().__init__(item_id, name, cost, description)
        self.damage = dmg
        self.prefixes = []
        self.suffixes = {}

    def set_suffixes(self, suffixes: [str], all_suffixes: dict):
        for suffix in suffixes:
            self.suffixes[suffix] = all_suffixes[suffix]

    def set_prefix(self, prefix: str):
        self.prefixes.append(prefix)

    def set_dmg(self,damage: int):
        """
        Make sure to calculate current damage before replacing it.
        :param damage: int
        :return: Nothing
        """
        self.damage = damage

    def adjust_name_for_prefsuf(self):
        """
        Tell the program to adjust the weapons name because its prefixes and
        suffixes have been set.
        :return: Nothing
        """
        chars = []
        for pref in self.prefixes:
            chars.extend(str(pref))
            chars.extend(" ")
        chars.extend(str(self.name))
        for suf in self.suffixes.keys():
            chars.extend(", ")
            chars.extend(str(suf))

        self.name = ''.join(chars)
