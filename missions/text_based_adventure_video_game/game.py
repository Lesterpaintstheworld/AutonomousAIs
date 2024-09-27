# Text-Based Adventure Game

import random

class Game:
    def __init__(self):
        self.player = Player()
        self.current_room = None
        self.rooms = self.initialize_rooms()

    def initialize_rooms(self):
        # Initialize and return a dictionary of Room objects
        pass

    def start_game(self):
        print("Welcome to the Text-Based Adventure Game!")
        self.current_room = self.rooms['start']
        self.game_loop()

    def game_loop(self):
        while True:
            self.current_room.describe()
            action = input("What would you like to do? ").lower()
            if action == 'quit':
                print("Thanks for playing!")
                break
            self.process_action(action)

    def process_action(self, action):
        actions = action.split()
        if not actions:
            print("Please enter a valid action.")
            return

        command = actions[0].lower()

        if command == "inventory":
            self.player.show_inventory()
        elif command == "take" and len(actions) > 1:
            item = " ".join(actions[1:])
            if item in self.current_room.items:
                self.player.add_to_inventory(item)
                self.current_room.items.remove(item)
            else:
                print(f"There is no {item} here to take.")
        elif command == "drop" and len(actions) > 1:
            item = " ".join(actions[1:])
            if item in self.player.inventory:
                self.player.remove_from_inventory(item)
                self.current_room.items.append(item)
                print(f"You dropped {item}.")
            else:
                print(f"You don't have {item} in your inventory.")
        elif command == "use" and len(actions) > 1:
            item = " ".join(actions[1:])
            self.player.use_item(item)
        else:
            print("I don't understand that command.")

class Player:
    def __init__(self):
        self.inventory = []
        self.health = 100

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

class Room:
    def __init__(self, name, description, exits):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = []

    def describe(self):
        print(f"\nYou are in {self.name}.")
        print(self.description)
        print("Exits:", ", ".join(self.exits.keys()))
        if self.items:
            print("Items in the room:", ", ".join(self.items))

if __name__ == "__main__":
    game = Game()
    game.start_game()