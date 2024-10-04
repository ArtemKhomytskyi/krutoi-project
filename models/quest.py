class Quest:
    def __init__(self, name, location, description, reward_description, reward, completion_condition):
        self.name = name
        self.description = description
        self.reward_description = reward_description
        self.reward = reward
        self.completion_condition = completion_condition
        self.completed = False
        self.location = location

    def complete(self, player):
        if not self.completed:
            if self.completion_condition:
                self.completed = True
                self.reward(player)
                print(f"Quest completed: {self.name}")
                print(f"Reward: {self.reward_description}")
                return True
            else:
                print(f"Quest not completed: {self.name}")
                return False
        else:
            print("Quest already completed")
            return False   

    def __str__(self):
        # return name and description
        return f"{self.name}: {self.description}"