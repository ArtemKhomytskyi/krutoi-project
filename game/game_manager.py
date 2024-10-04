import random

class GameManager:
    def __init__(self, player, board, bosses, quests):
        self.player = player
        self.board = board
        self.bosses = bosses 
        self.quests = quests
        self.place_bosses(bosses)
        self.options = ["Move", "Check inventory", "Use item", "View quests", "Exit game", "Buy from merchant", "Fight boss", "Complete quest"]
    
    @property
    def get_player_position(self):
        return self.player.position
       
    def get_board_location(self, x, y):
        return self.board.get_location(x, y)

    def move_player(self, direction):
        if direction == 'N':
            self.player.move('north')
        elif direction == 'S':
            self.player.move('south')
        elif direction == 'E':
            self.player.move('east')
        elif direction == 'W':
            self.player.move('west')
        else:
            print("Invalid direction")

    def place_bosses(self, bosses):
        # Place the bosses on the board randomly, but not on the player's location (0,0)
        # Also, bosses cannot be placed on the same location
        available_positions = [(x, y) for x in range(self.board.size) for y in range(self.board.size)]
        available_positions.remove((0, 0))
        for boss in bosses:
            x, y = random.choice(available_positions)
            boss.position = (x, y)
            available_positions.remove((x, y))

    @property
    def show_board(self):
        for i, row in enumerate(self.board.board_representation):
            row_str = '| '
            for j, location in enumerate(row):
                if (i, j) == self.player.position:
                    location_str = f"\033[32m{location.name}\033[0m"
                    "\033[32m{self.location.name}\033[0m"
                elif (i, j) in [boss.position for boss in self.bosses]:
                    location_str = f"\033[31m{location.name}\033[0m"
                elif location.name == "King's Landing":
                    location_str = f"\033[30m{location.name}\033[0m"
                else:
                    location_str = location.name
                row_str += f"{location_str} | "
            print(row_str)
        print()

    def handle_player_turn(self, option):
        if option not in self.options:
            print("Invalid option.")
            return
        else:
            if option == 'Exit game':
                print("Exiting the game.")
                exit()
            elif option == 'Move':
                direction = input("Enter direction (N, S, E, W): ")
                self.move_player(direction)
            elif option == 'Check inventory':
                print("\nYour Inventory:")
                for item in self.player.inventory.items:
                    print(f"- {item}")
            elif option == 'Use item':
                self.handle_use_item()
            elif option == 'View quests':
                print("\nYour Quests:")
                for quest in self.quests:
                    print(f"- {quest}")
            elif option == 'Buy from merchant':
                print(f"\nYou have {self.player.gold} gold.")
                current_location = self.get_board_location(*self.get_player_position)
                for npc in current_location.npcs:
                    if npc.type == "Merchant":
                        npc.trade(self.player)
            elif option == 'Complete quest':
                current_location = self.get_board_location(*self.get_player_position)
                for quest in self.quests:
                    if quest.location == current_location.name:
                        quest.complete(self.player)
            elif option == 'Fight boss':
                current_location = self.get_board_location(*self.get_player_position)
                for boss in self.bosses:
                    if boss.position == self.get_player_position:
                        self.handle_boss_combat(boss, self.player)

    def handle_use_item(self):
        if self.player.inventory.items:
            print("\nSelect an item to use:")
            for i, item in enumerate(self.player.inventory.items, 1):
                print(f"{i}. {item}")
            choice = int(input("Enter the number of the item: "))
            if 1 <= choice <= len(self.player.inventory):
                print(f"\nYou used {self.inventory[choice - 1]}.")
                self.inventory.pop(choice - 1)
            else:
                print("Invalid choice.")
        else:
            print("Your inventory is empty.")



    def handle_boss_combat(self, boss, player):
        print('\n')
        print(f"Boss encounter: {boss.name}")

        # Prepare for combat
        self.player.defending = False

        while True:
            print(f"Player health: {player.health}")
            print(f"Boss health: {boss.health}\n")
            
            # If player is not defending, print player options
            if not self.player.defending:
                # Print player options
                print("Player options:")
                print("1. Use item")
                print("2. Run")
                print("3. Attack")
                choice = input("Enter choice: ")
                
                print('\n')

                if choice == "1":
                    self.handle_use_item()
                elif choice == "2":
                    print("You ran away.")
                    break
                
                # coeffiecent to by applied on the boss damage
                coeff = random.uniform(0.5, 1)  
                damage = int(player.strength * coeff)
                boss.take_damage(damage)
                print(f"{player.name} attacks {boss.name} for {damage} damage.")

                # Check if boss is dead
                if boss.health <= 0:
                    print(f"{player.name} defeated {boss.name}!")
                    reward = 200
                    player.earn_gold(reward)
                    print(f"{player.name} earned {reward} gold.")
                    break
                else:
                    self.player.defending = True

            # If player is defending the boss attacks
            else:
                probability_of_special_attack = random.random()
                if probability_of_special_attack < 0.05:
                    boss.use_special_ability(player)
                else:
                    # coeffiecent to by applied on the boss damage
                    coeff = random.uniform(0.5, 1)
                    damage = int(boss.strength * coeff)
                    player.take_damage(damage)
                    print(f"{boss.name} attacks {player.name} for {damage} damage.")
            
                # Check if player is dead
                if player.health <= 0:
                    print(f"{boss.name} defeated {player.name}!")
                    print("Game Over.")
                    exit()
                else:
                    self.player.defending = False
                    



