from room import Room
from player import Player
from item import Item

# Declare items

items = {
    'herb': Item('herb', 'Eating this makes you feel funny.'),

    'ring': Item('ring', 'Looks shiny and precious.'),

    'potion': Item('potion', 'Drink this and find out what happens.')
}

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),

    'secret': Room("Secret Room", """You've happened upon a secret room. At the end of the room a sign posted on the wall reads: "Congratulations! You've reached the secret room and found the real treasure: finishing your stretch goals!" W-Wait... Huh?""")
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']


# Add items to rooms

room['outside'].items = [items['herb']]
room['foyer'].items = [items['ring'], items['potion']]

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

new_player = Player('Jeff', room['outside'])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

directions = ['n', 's', 'e', 'w']

while True:
    print(f'\nCurrent room: {new_player.current_room.name}.')

    if new_player.current_room.name == "Grand Overlook" and new_player.enlightened == True:
        print(f'\nThe effects of the potion allow you to see magic platforms that traverse the chasm.\n')

    print(f'"{new_player.current_room.description}"\n')

    if new_player.current_room.items:
        print(f'Loot available: {new_player.current_room.items}\n')

    command = input("How will you proceed? ").lower()
    command = command.split()

    if len(command) == 2:
        verb = command[0]
        item = command[1]

        if verb == 'get' or verb =='take':
            for i in new_player.current_room.items:
                if i.name == item:
                    new_player.current_room.items.remove(i)
                    new_player.inventory.append(i)
                    i.on_take()
                else:
                    print('\nError: item not found.')
        if verb == 'drop':
            for i in new_player.inventory:
                if i.name == item:
                    new_player.inventory.remove(i)
                    new_player.current_room.items.append(i)
                    i.on_drop()
        if verb == 'use':
            for i in new_player.inventory:
                if i.name == item:
                    if item == 'potion':
                        new_player.inventory.remove(i)
                        print('\nYou begin to sense magical energy around you.')
                        room['overlook'].n_to = room['secret']
                        new_player.enlightened = True

    if len(command) == 1:
        command = command[0]

        if command in directions:
            if command == 'n' and new_player.current_room.n_to != None:
                new_player.current_room = new_player.current_room.n_to
            elif command == 's' and new_player.current_room.s_to != None:
                new_player.current_room = new_player.current_room.s_to
            elif command == 'e' and new_player.current_room.e_to != None:
                new_player.current_room = new_player.current_room.e_to
            elif command == 'w' and new_player.current_room.w_to != None:
                new_player.current_room = new_player.current_room.w_to
            else:
                command = input("An obstacle prevents you from going that way. (Press Enter to continue)\n").lower()
        elif command == 'i' or command == 'inventory':
            print(f'\nInventory: {new_player.inventory}')
        elif command == 'q':
            print(f'Goodbye {new_player.name}! (You have quit the game)')
            break
        else:
            print("Invalid input. Try again. (Hint: N, S, E, or W)\n")