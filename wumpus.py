import random

NUM_ROOMS = 20
STARTING_ARROWS = 5
NEIGHBORS = {
     1:(2,5,8),     2:(1,3,10),   3:(2,4,12),    4:(3,5,14),
     5:(1,4,6),     6:(5,7,15),   7:(6,8,17),    8:(1,7,9),
     9:(8,10,18),  10:(2,9,11),  11:(10,12,19), 12:(3,11,13),
    13:(12,14,20), 14:(4,13,15), 15:(6,14,16),  16:(15,17,20),
    17:(7,16,18),  18:(9,17,19), 19:(11,18,20), 20:(13,16,19),
}
WUMPUS_MOVE_PROBABILITY = 0.75

def describe(player, wumpus, bats, pits, arrows):
    if wumpus in NEIGHBORS[player]:
        print("I smell a Wumpus...")
    if any(bat in NEIGHBORS[player] for bat in bats):
        print("Bats nearby...")
    if any(pit in NEIGHBORS[player] for pit in pits):
        print("I feel a draft...")

    print(f"You are in room {player}")
    print(f"Rooms nearby: {NEIGHBORS[player]}")
    print(f"Arrows: {arrows}")

def check_death(player, wumpus, pits):
    if player == wumpus:
        print("WUMPUS ATE YOU!")
        return True
    if player in pits:
        print("YOU FELL INTO A PIT!")
        return True
    return False

def handle_command(player):
    while True:
        c = input("> ").lower().split()
        if len(c) == 2 and c[0] in {"m", "s"} and c[1].isdigit():
            action, room = c[0][0], int(c[1])
            if room not in NEIGHBORS[player]:
                print(f"Not connected to room {room}")
                continue
            break
        print("Use: m <room> or s <room>")

    return action, room

arrows = STARTING_ARROWS
starting_rooms = random.sample(range(1, NUM_ROOMS + 1), 6)
player, wumpus, bat1, bat2, pit1, pit2 = starting_rooms
bats = (bat1, bat2)
pits = (pit1, pit2)

while True:
    describe(player, wumpus, bats, pits, arrows)

    action, room = handle_command(player)

    if action == "s":          # Shoot arrow
        if room == wumpus:
            print("YOU KILLED THE WUMPUS!")
            break
        print("You missed!")
        arrows -= 1
        if arrows == 0:
            print("OUT OF ARROWS!")
            break
        if random.random() <= WUMPUS_MOVE_PROBABILITY:
            wumpus = random.choice(NEIGHBORS[wumpus])
            if wumpus == player:
                print("Wumpus moved to your room!")
                print("WUMPUS ATE YOU!")
                break
    else:                       # Move to new room
        player = room

    if check_death(player, wumpus, pits):
        break

    if player in bats:
        while player in bats:
            player = random.randint(1, NUM_ROOMS)
        print(f"Bats lift you to another room {player}")
        if check_death(player, wumpus, pits):
            break
