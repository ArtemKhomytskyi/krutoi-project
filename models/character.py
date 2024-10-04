from models.inventory import Inventory

class Character:
    def __init__(self, name, house, strength, intelligence, charisma, defense):
        self.name = name
        self.house = house
        self.strength = max(1, strength)  # Ensure strength is at least 1
        self.intelligence = intelligence
        self.charisma = charisma
        self.defense = max(0, defense)  # Ensure defense is non-negative
        self._health = 100
        self.gold = 100
        self.inventory = Inventory()
        self.position = (0, 0)
        self.defending = False

    @property
    def speak_words(self):
        return f"{self.name} says: {self.house.words}"

    def move(self, direction):
        x, y = self.position
        if direction == 'north':
            self.position = (x-1, y)
        elif direction == 'south':
            self.position = (x+1, y)
        elif direction == 'east':
            self.position = (x, y+1)
        elif direction == 'west':
            self.position = (x, y-1)

    @property
    def total_stats(self):
        return self.strength + self.intelligence + self.charisma + self.defense

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            self._health = 0
        elif value > 100:
            self._health = 100
        else:
            self._health = value

    @health.deleter
    def health(self):
        del self._health

    @property
    def inventory_value(self):
        return self.inventory.get_total_value()

    def use_item(self, item_name):
        for item in self.inventory.items:
            if item.name == item_name:
                item.use(self)
                self.inventory.remove_item(item)
                return True
        print(f"{self.name} does not have {item_name}")
        return False


    def take_damage(self, amount):
        self.health = max(0, self.health - amount)


    def is_alive(self):
        return self.health > 0

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def earn_gold(self, amount):
        self.gold += amount

class Warrior(Character):

    def __init__(self, name, house, strength, intelligence, charisma, defense):
        super().__init__(name, house, strength, intelligence, charisma, defense)
        self.strength += 10  # Warriors are stronger

class Diplomat(Character):
    def __init__(self, name, house, strength, intelligence, charisma, defense):
        super().__init__(name, house, strength, intelligence, charisma, defense)
        self.charisma += 10  # Diplomat are more intelligent


class Maester(Character):
    def __init__(self, name, house, strength, intelligence, charisma, defense):
        super().__init__(name, house, strength, intelligence, charisma, defense)
        self.intelligence += 10  # Maesters are more intelligent


class Boss(Character):
    def __init__(self, name, strength, intelligence, charisma, defense, special_ability):
        super().__init__(name, None, strength, intelligence, charisma, defense)
        self.special_ability = special_ability
        self.health = 150

    def use_special_ability(self, target):
        return self.special_ability(self, target)

# Define boss characters
def cersei_ability(self, target):
    damage = self.intelligence * 2
    target.take_damage(damage)
    return f"Cersei uses 'Wildfire Plot' and deals {damage} damage!"

def night_king_ability(self, target):
    self.health += 20
    return f"The Night King uses 'Raise the Dead' and heals for 20 health!"

def dragon_ability(self, target):
    damage = self.strength * 3
    target.take_damage(damage)
    return f"Drogon uses 'Dragonfire' and deals {damage} damage!"

bosses = [
    Boss("Cersei Lannister", 10, 15, 18, 8, cersei_ability),
    Boss("Night King", 20, 15, 10, 15, night_king_ability),
    Boss("Drogon", 25, 10, 5, 20, dragon_ability)
]

