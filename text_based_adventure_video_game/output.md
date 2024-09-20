# Text-based Adventure Video Game Prototype

## Game Overview
In this text-based RPG, the player begins in a jail cell within a goblin-infested dungeon. The objective is to escape the cell, reacquire lost gear, and explore the dungeon to find a way out.

## Game Code
```python
class Game:
    def __init__(self):
        self.player_location = "jail cell"
        self.inventory = []

    def start(self):
        print("Welcome to the Goblin Dungeon!")
        self.show_location()

    def show_location(self):
        if self.player_location == "jail cell":
            print("You are in a dark, damp jail cell. You can hear goblins outside.")
            print("What will you do? (1: Look around, 2: Try to escape)")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.look_around()
            elif choice == "2":
                self.try_to_escape()
            else:
                print("Invalid choice. Try again.")
                self.show_location()

    def look_around(self):
        print("You see a rusty key on the floor.")
        self.inventory.append("rusty key")
        print("You picked up a rusty key.")
        self.show_location()

    def try_to_escape(self):
        if "rusty key" in self.inventory:
            print("You use the rusty key to unlock the cell door and escape!")
            self.player_location = "dungeon"
            print("You are now in the dungeon. It's dark and filled with goblins!")
        else:
            print("The door is locked. You need a key to escape.")
            self.show_location()

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
- Implement a combat system and additional quests.
- Gather feedback from players to improve gameplay.
