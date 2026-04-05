import random

neighbors = {
     1:(2,5,8),     2:(1,3,10),   3:(2,4,12),    4:(3,5,14),
     5:(1,4,6),     6:(5,7,15),   7:(6,8,17),    8:(1,7,9),
     9:(8,10,18),  10:(2,9,11),  11:(10,12,19), 12:(3,11,13),
    13:(12,14,20), 14:(4,13,15), 15:(6,14,16),  16:(15,17,20),
    17:(7,16,18),  18:(9,17,19), 19:(11,18,20), 20:(13,16,19),
}

arrows = 5

random_rooms = random.sample(range(1, 21), 6)
player, wumpus, bat1, bat2, pit1, pit2 = random_rooms

def describe():
    if wumpus in neighbors[player]: print("I smell a Wumpus...")
    if bat1 in neighbors[player] or bat2 in neighbors[player]:
        print("Bats nearby...")
    if pit1 in neighbors[player] or pit2 in neighbors[player]:
        print("I feel a draft...")
    print("You are in room", player)
    print("Rooms nearby:", neighbors[player], "Arrows:", arrows)

while True:
    if player == wumpus: print("WUMPUS ATE YOU!"); break
    if player in (pit1, pit2): print("FELL IN PIT"); break
    if player in (bat1, bat2):
        player = random.randint(1,20)
        print("Bats lift you to another room..."); continue

    describe()
    c = input("> ").lower().split()
    if len(c) != 2 or c[0][0] not in "ms" or not c[1].isdigit():
        print("Use: m <room> or s <room>"); continue
    room = int(c[1])
    if room not in neighbors[player]:
        print("Not connected."); continue

    if c[0][0] == "s":          # Shoot arrow
        if room == wumpus: print("YOU KILLED THE WUMPUS!"); break
        print("You missed!")
        arrows -= 1
        if arrows == 0: print("OUT OF ARROWS!"); break
        if random.random() < 0.75:
            wumpus = random.choice(neighbors[wumpus])
            if wumpus == player:
                print("Wumpus moved to your room!")
    else:                       # Move to new room
        player = room
