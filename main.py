from random import random, randint
#set up the player boards (hit boards are the places a player has fired at, ship boards are the places a player has placed their ships).
hit_board = []
enemy_ship_board = []
for x in range(10):
    hit_board.append(["0"] * 10)
    enemy_ship_board.append(["0"] * 10)

#prints a new screen with the title and the current player's hit board.
def new_screen():
    print("Battleship!")
    print_board(hit_board)
    
def print_board(board):
    for row in board:
        print(" ".join(row))
    print("\n")

#Creates a random point (x,y position) and returns it as a tuple.
def random_position(board, xBound, yBound):
    xCoordinate = randint(0, (len(board) - 1) - xBound)
    yCoordinate = randint(0, (len(board[0]) - 1) - yBound)
    return (xCoordinate, yCoordinate)

#Our ships are objects that are passed a name and a size.
class Ship:
    #Constructor function that sets up our local variables and makes positions our ship.
    def __init__(self, name, size):
        self.size = size
        self.name = name
        self.direction = (int)(random() * 2) * 90
        self.positions = []
        self.damage = 0
        
        #The following code finds a starting position and tries to position the ship based on that starting position, if one of the locations we try to place our ship is occupied, we find a new starting point.
        empty_space = False
        row = 0
        col = 0
        #This loop continues looking for an open space until one is found.
        while not empty_space:
            empty_space = True
            #The ship is vertical, we check adjacent vertical positions to ensure we can place the ship.
            if self.direction == 0:
                (row, col) = random_position(hit_board, self.size, 0)
                for i in range(self.size):
                    if enemy_ship_board[row + i][col] == 1:
                        empty_space = False
                        break
            #The ship is horizontal, we check adjacent horizontal positions to ensure we can place the ship.
            elif self.direction == 90:
                (row, col) = random_position(hit_board, 0, self.size)
                for i in range(self.size):
                    if enemy_ship_board[row][col + i] == 1:
                        empty_space = False
                        break
        #The ship is vertical and our locations are empty, so we place the ship.
        if self.direction == 0:
            for i in range(size):
                self.positions.append([row + i, col])
                enemy_ship_board[row + i][col] = 1
        #The ship is horizontal and our locations are empty, so we place the ship.
        elif self.direction == 90:
            for i in range(size):
                self.positions.append([row, col + i])
                enemy_ship_board[row][col + i] = 1
#Set up our ships list and add our ship objects
ships = []
ships.append(Ship("submarine", 1))
ships.append(Ship("corsair", 2))
ships.append(Ship("cruiser", 3))
ships.append(Ship("battleship", 4))
ships.append(Ship("carrier", 5))
#Debugging script so we can see the positions of each ship
#for ship in ships:
#    print(ship.name + " positions:")
#    for position in ship.positions:
#        print(str(position[0]) + "," + str(position[1]))

#The main game loop continues until the ships have all been destroyed (when a ship is destroyed it is removed from the ships list).
def main():
    while (len(ships) is not 0):
        new_screen()
        guess_row = int(input("Enter Row:"))
        guess_col = int(input("Enter Column:"))
        #Check if the guess was off the board.
        if (guess_row < 0 or guess_row > (len(hit_board) - 1) or guess_row == "") or (guess_col < 0 or guess_col > (len(hit_board[0]) - 1) or guess_col == ""):
            print("Har har har, that ain't on yonder board, try again!")
        #Check if the player has fired at that location already.
        elif(hit_board[guess_row][guess_col] != "0"):
            print("Yer tryin' ta shoot at the same spot twice are ye? Fool! Try again")
        #Check the position to see if a ship is there and a hit is registered.
        else:
            hit = False
            for ship in ships:
                for position in ship.positions:
                    #Check if a ship position is equal to the guessed position.
                    if guess_row == position[0] and guess_col == position[1]:
                        hit = True
                        ship.damage += 1
                        #Check if the ship is destroyed.
                        if ship.damage == ship.size:
                            print("Ye've sunk me " + ship.name + "! How could ye!")
                            #Loop through the ship's positions and set them to D for destroyed.
                            for section in ship.positions:
                                hit_board[section[0]][section[1]] = "D"
                            #Remove the ship from the array.
                            ships.remove(ship)
                        #Otherwise the ship has been hit, mark it with an H.
                        else:
                            print("Argggghhh, ye've hit me " + ship.name + ", ye scallywag!")
                            hit_board[guess_row][guess_col] = "H"
                        break
                #Break out of the outer loop if a hit was registered.
                if hit == True:
                    break
            #If no hit was registered after the outer for loop ends, the guess was a miss.
            if hit == False:
                print("Ye missed, har har har!")
                hit_board[guess_row][guess_col] = "X"
    print("Ye've sunk all me ships! I'm wrecked!")
    
#Runs the main game loop
if __name__ == "__main__":
    main()
