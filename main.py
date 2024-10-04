from models.character import Warrior, bosses
from models.house import House
from models.quest import Quest

from game.board import GameBoard
from game.game_manager import GameManager
from game.menu import GameMenu

import random
random.seed(42)

def main():

    defend_wall = Quest("Defend The Wall",
                    "The Wall",
                    "Protect The Wall from the White Walkers.",
                    "You earned 100 gold.",
                    lambda p: p.earn_gold(100),
                    lambda p: game_board.board[p.position[0]][p.position[1]].name == 'The Wall')

    quests = [defend_wall]

    stark = House("Stark", "Direwolf", "Winter is coming")      
    character = Warrior('Tiago', stark, 10, 10, 10, 10)

    # Create the game board
    game_board = GameBoard(5)
    
    # Create the game manager
    game_manager = GameManager(character, game_board, bosses, quests)

    # Create the game menu
    game_menu = GameMenu()

    print("\n") 

    # Game loop
    while True: 
        boss_flag = False
        merchant_flag = False
        quest_flag = False

        # Get player position
        player_position = game_manager.get_player_position

        # Find the location of the player
        current_location = game_manager.get_board_location(*player_position)

        # Check if the trigger event is True
        if current_location.trigger_event():
            # Handle the event here
            # Randomly choose one of the two events, bandits or treasure.
            # Bandidts has probability of 0.2 and treasure has probability of 0.8
            event = random.choices(["bandits", "treasure"], weights=[0.2, 0.8])[0]

            print("Event:")

            if event == "bandits":
                print("You have been attacked by bandits!")
                # Handle bandit encounter
                # PLayer losses health
                character.take_damage(10)
                print(f"You lost 10 health. Your current health is: {character.health}\n")
            else:
                print("You found a treasure!")
                # Handle treasure encounter
                # Player earns gold
                character.earn_gold(20)
                print(f"You earned 20 gold. Your current gold is: {character.gold}\n")

        # Check if the current location has a quest
        if current_location.name == "The Wall" and not defend_wall.completed:
            print("Available Quest:")
            print(f"{defend_wall}\n")
            quest_flag = True
        else: 
            quest_flag = False

        # Check if the current location has an NPC
        if current_location.check_for_npc():
            # Check if the NPC is a merchant
            for npc in current_location.npcs:
                if npc.type == "Merchant":
                    print("NPC:")
                    print(f"Merchant encounter: {npc.name}\n")
                    merchant_flag = True
                else:
                    merchant_flag = False

        # Check if the current location has a boss
        for boss in bosses:
            if player_position == boss.position:
                print("Boss:")
                print(f"Boss encounter: {boss.name}\n")
                boss_flag = True
            else:
                boss_flag = False

        flags = {"quest": quest_flag, "merchant": merchant_flag, "boss": boss_flag}

        print("Map:")
        game_manager.show_board
        
        # Update the game menu with the flags
        game_menu.process_flags(flags)
        choice = game_menu.print_menu

        # Reset the menu
        game_menu.reset_menu

        # Handle player turn
        game_manager.handle_player_turn(choice)

        print("\n") 

main()