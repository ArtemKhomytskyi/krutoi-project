class GameMenu:
    def __init__(self):
        # Base menu options
        self.base_menu = ["Move", "Check inventory", "Use item", "View quests"]
        self.additional_menu = []  # Additional menu options that can be appended
        self.exit_option = ["Exit game"]

    @property
    def reset_menu(self):
        self.additional_menu = []

    def process_flags(self, flags):
        # Process flags and append additional menu options
        if flags["merchant"]:
            self.additional_menu.append("Buy from merchant")
        if flags["boss"]:
            self.additional_menu.append("Fight boss")
        if flags["quest"]:
            self.additional_menu.append("Complete quest")

    @property
    def print_menu(self):
        # Print the base menu and append additional options based on flags
        print("\nMain Menu:")
        option_number = 1
        for option in self.base_menu:
            print(f"{option_number}. {option}")
            option_number += 1
        for option in self.additional_menu:
            print(f"{option_number}. {option}")
            option_number += 1
        for option in self.exit_option:
            print(f"{option_number}. {option}")
            option_number += 1

        options = self.base_menu + self.additional_menu + self.exit_option
        choice = input("Choose an option: \n")

        # return the option 
        return options[int(choice) - 1]
        