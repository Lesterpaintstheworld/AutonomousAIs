class Game:
    def __init__(self):
        self.rooms = {
            'jail': {
                'description': "You are in a dark jail cell. A key is on the ground.",
                'exits': {'guard_room': 'guard'},
                'item': 'key'
            },
            'guard_room': {
                'description': "You are in the guard room. A goblin is here guarding your sword.",
                'exits': {'jail': 'jail'},
                'item': 'sword'
            }
        }
        self.current_room = 'jail'
        self.inventory = []

    def describe_room(self):
        room = self.rooms[self.current_room]
        print(room['description'])
        if room['item']:
            print(f"You see a {room['item']} here.")

    def move(self, direction):
        if direction in self.rooms[self.current_room]['exits']:
            self.current_room = self.rooms[self.current_room]['exits'][direction]
            self.describe_room()
        else:
            print("You can't go that way.")

    def take_item(self):
        room = self.rooms[self.current_room]
        if room['item']:
            self.inventory.append(room['item'])
            print(f"You have taken the {room['item']}.")
            room['item'] = None
        else:
            print("There's nothing to take.")

    def play(self):
        self.describe_room()
        while True:
            command = input("What do you want to do? ").strip().lower()
            if command in ['quit', 'exit']:
                print("Thanks for playing!")
                break
            elif command in ['go guard_room', 'go jail']:
                self.move(command.split()[1])
            elif command == 'take item':
                self.take_item()
            else:
                print("Invalid command.")

if __name__ == "__main__":
    game = Game()
    game.play()
