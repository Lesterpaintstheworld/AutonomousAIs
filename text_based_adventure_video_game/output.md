# Text-based Adventure Video Game Prototype

## Game Overview
In this text-based RPG, the player begins in a jail cell within a goblin-infested dungeon. The objective is to escape the cell, reacquire lost gear, and explore the dungeon to find a way out.

## Game Code
```python
import random

class Game:
    def __init__(self):
        self.player_location = "jail cell"
        self.inventory = []
        self.health = 100
        self.locations = {
            "jail cell": "You are in a dark, damp jail cell. You can hear goblins outside.",
            "dungeon": "You are now in the dungeon. It's dark and filled with goblins!",
            "treasure room": "You have entered a treasure room filled with gold and jewels!"
        }

    def start(self):
        print("Welcome to the Goblin Dungeon!")
        self.show_location()

    def show_location(self):
        print(self.locations[self.player_location])
        if self.player_location == "jail cell":
            print("What will you do? (1: Look around, 2: Try to escape)")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.look_around()
            elif choice == "2":
                self.try_to_escape()
            else:
                print("Invalid choice. Try again.")
                self.show_location()
        elif self.player_location == "dungeon":
            print("What will you do? (1: Explore, 2: Go to treasure room, 3: Fight goblin)")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.go_to_treasure_room()
            elif choice == "3":
                self.fight_goblin()
            else:
                print("Invalid choice. Try again.")
                self.show_location()
        elif self.player_location == "treasure room":
            print("What will you do? (1: Take gold, 2: Go back to dungeon)")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.take_gold()
            elif choice == "2":
                self.player_location = "dungeon"
                self.show_location()
            else:
                print("Invalid choice. Try again.")
                self.show_location()

    def look_around(self):
        if "rusty key" not in self.inventory:
            print("You see a rusty key on the floor.")
            self.inventory.append("rusty key")
            print("You picked up a rusty key.")
        else:
            print("You already have the rusty key.")
        self.show_location()

    def try_to_escape(self):
        if "rusty key" in self.inventory:
            print("You use the rusty key to unlock the cell door and escape!")
            self.player_location = "dungeon"
            self.show_location()
        else:
            print("The door is locked. You need a key to escape.")
            self.show_location()

    def explore(self):
        print("You explore the dungeon and find a hidden passage.")
        self.player_location = "treasure room"
        self.show_location()

    def go_to_treasure_room(self):
        print("You enter the treasure room and find a pile of gold!")
        self.show_location()

    def take_gold(self):
        print("You take some gold from the treasure room. You feel rich!")
        self.show_location()

    def fight_goblin(self):
        goblin_health = 50
        print("A goblin appears! Prepare to fight!")
        while goblin_health > 0 and self.health > 0:
            action = input("Do you want to (1: Attack, 2: Run away): ")
            if action == "1":
                damage = random.randint(10, 30)
                goblin_health -= damage
                print(f"You attack the goblin and deal {damage} damage!")
                if goblin_health > 0:
                    goblin_damage = random.randint(5, 15)
                    self.health -= goblin_damage
                    print(f"The goblin attacks you and deals {goblin_damage} damage! Your health is now {self.health}.")
            elif action == "2":
                print("You run away from the goblin!")
                self.player_location = "dungeon"
                self.show_location()
                return
            else:
                print("Invalid choice. Try again.")
        
        if self.health <= 0:
            print("You have been defeated by the goblin. Game over.")
        else:
            print("You have defeated the goblin!")

if __name__ == "__main__":
    game = Game()
    game.start()
```

## Instructions
1. Save the code above in a file named `game.py`.
2. Run the game using Python 3: `python game.py`.
3. Follow the prompts to explore the dungeon.

## Documentation
### Setup Instructions
- Ensure you have Python 3 installed on your computer.
- Create a new directory for the game files.
- Save the provided game code in a file named `game.py` within the directory.

### Gameplay Guidance
- Start the game by running `python game.py` in your command line or terminal.
- You will begin in a jail cell. Choose to look around or try to escape.
- Collect items and make choices to navigate through the dungeon.
- The game will provide prompts for your actions.

## Next Steps
- Expand the game with more locations, items, and goblin encounters.
- Gather feedback from players to improve gameplay.

## Status
- Official release: Completed on Sept 22.
