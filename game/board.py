import random
from models.inventory import Item

class NPC:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Merchant(NPC):
    def __init__(self, name):
        super().__init__(name, "Merchant")
        self.item = Item("Strength Potion", 50, lambda p: setattr(p, 'strength', p.strength + 10), "Increases strength by 10")

    def trade(self, player):
        # Shows the item the NPC has
        print(f"{self.name} has a {self.item.name} for sale at {self.item.value} gold")
        # Asks the player if they want to buy the item
        buy = input("Do you want to buy it? (Y/N) ")
        if buy == "Y":
            # If the player has enough gold, they can buy the item
            if player.spend_gold(self.item.value):
                player.inventory.add_item(self.item)
                print(f"{player.name} bought a {self.item.name}")
            else:
                print(f"{player.name} does not have enough gold")
        else:
            print("No problem")


class Location:
    def __init__(self, name, color, event_probability=0.3, npcs=None):
        self.name = name
        self.color = color
        self.event_probability = event_probability
        self.npcs = npcs

    def check_for_npc(self):
        if self.npcs:
            return True
        else:
            return False

    def trigger_event(self):
        probability = random.random()
        if probability <= self.event_probability:
            return True
        else:
            return False

    def __str__(self):
        return f"{self.name}"

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.locations = [
            Location("Winterfell", "#444444", npcs=[
                NPC("Ser Rodrik Cassel", "Guard")
            ]),
            Location("King's Landing", "#f1c232", npcs=[
                Merchant("Street Vendor"),
            ]),
            Location("The Wall", "#fffafa", npcs=[
                NPC("Castle Black Cook", "Innkeeper"),
            ])]
        self.wilderness = Location("Wilderness", "#4a6741")
        self.board_representation = self.generate_board()

    def generate_board(self):
        board_representation = [[self.wilderness for _ in range(self.size)] for _ in range(self.size)]
        available_positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        
        for location in self.locations:
            if available_positions:
                x, y = random.choice(available_positions)
                board_representation[y][x] = location
                available_positions.remove((x, y))
            else:
                break  # No more available positions
        
        return board_representation

    def get_location(self, x, y):
        return self.board_representation[x][y]

    def convert_row_to_str(self,row):
        return ' | '.join([location.name for location in row])

    @property
    def board(self):
        for row in self.board_representation:
            print(self.convert_row_to_str(row))
        print()

