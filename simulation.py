class Quoridor:
    def __init__(self):
        # 9x9 game board
        self.board_size = 9
        self.p1_pos = [0, 4]  # Player 1 starts at row 0, column 4
        self.p2_pos = [8, 4]  # Player 2 starts at row 8, column 4
        self.p1_walls = 10
        self.p2_walls = 10
        # Store vertical and horizontal walls as sets
        self.horizontal_walls = set()  # Format: (x, y) where wall is between (x,y) and (x+1,y)
        self.vertical_walls = set()    # Format: (x, y) where wall is between (x,y) and (x,y+1)
        self.current_player = 1  # Player 1 starts the game

    def display_board(self):
        # Display the board with players and walls
        for row in range(self.board_size):
            # Display the player positions
            for col in range(self.board_size):
                # Use end to display vertical walls between columns
                end = ' '
                if (row, col) in self.vertical_walls or (row - 1, col) in self.vertical_walls:
                    end = '|'  # Display vertical wall

                if [row, col] == self.p1_pos:
                    print('1', end=end)
                elif [row, col] == self.p2_pos:
                    print('2', end=end)
                else:
                    print('.', end=end)

            print()  # Newline after every row

            # Display horizontal walls between rows
            if row < self.board_size - 1:
                for col in range(self.board_size):
                    if (row, col) in self.horizontal_walls:
                        print('---', end=' ')
                    else:
                        print(' ', end=' ')
                print()

        # Display the number of walls left
        print(f"Player 1 Walls: {self.p1_walls} | Player 2 Walls: {self.p2_walls}\n")

    def is_valid_move(self, player_pos, new_pos):
        x, y = player_pos
        nx, ny = new_pos
        # Check if within bounds
        if not (0 <= nx < self.board_size and 0 <= ny < self.board_size):
            return False
        # Check if there is a wall between the current position and the new position
        if x == nx:  # Moving horizontally
            if y < ny and ((x, y) in self.vertical_walls or (x-1, y) in self.vertical_walls):
                return False
            if y > ny and ((x, y-1) in self.vertical_walls or (x-1, y-1) in self.vertical_walls):
                return False
        elif y == ny:  # Moving vertically
            if x < nx and ((x, y) in self.horizontal_walls or (x, y-1) in self.horizontal_walls):  # Down move blocked
                return False
            if x > nx and ((x-1, y) in self.horizontal_walls or (x-1, y-1) in self.horizontal_walls): # Up move blocked
                return False
        return True

    def get_valid_moves(self, pos):
        x, y = pos
        possible_moves = []
        # Check all four possible directions (up, down, left, right)
        if x > 0 and self.is_valid_move(pos, [x-1, y]):  # Up
            possible_moves.append([x-1, y])
        if x < 8 and self.is_valid_move(pos, [x+1, y]):  # Down
            possible_moves.append([x+1, y])
        if y > 0 and self.is_valid_move(pos, [x, y-1]):  # Left
            possible_moves.append([x, y-1])
        if y < 8 and self.is_valid_move(pos, [x, y+1]):  # Right
            possible_moves.append([x, y+1])
        return possible_moves

    def place_wall(self, wall_type, x, y):
        # Ensure the wall is within bounds and doesn't overlap
        if wall_type.upper() == 'H':  # Horizontal wall
            if (x, y) not in self.horizontal_walls and x < 8 and y < 8:
                self.horizontal_walls.add((x, y))
                return True
        elif wall_type.upper() == 'V':  # Vertical wall
            if (x, y) not in self.vertical_walls and x < 8 and y < 8:
                self.vertical_walls.add((x, y))
                return True
        return False

    def move_player(self, new_pos):
        if self.current_player == 1:
            self.p1_pos = new_pos
        else:
            self.p2_pos = new_pos

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_win(self):
        # Player 1 wins if they reach row 8
        if self.p1_pos[0] == 8:
            print("Player 1 wins!")
            return True
        # Player 2 wins if they reach row 0
        elif self.p2_pos[0] == 0:
            print("Player 2 wins!")
            return True
        return False

    def get_player_input(self):
        while True:
            choice = input(f"Player {self.current_player}, Move (M) or Place Wall (W)? ").strip().upper()
            if choice == 'M':
                # Ask for direction and perform a move
                direction = input("Move (U)p, (D)own, (L)eft, (R)ight: ").strip().upper()
                x, y = self.p1_pos if self.current_player == 1 else self.p2_pos
                if direction == 'U' and self.is_valid_move([x, y], [x-1, y]):
                    return 'M', [x-1, y]
                elif direction == 'D' and self.is_valid_move([x, y], [x+1, y]):
                    return 'M', [x+1, y]
                elif direction == 'L' and self.is_valid_move([x, y], [x, y-1]):
                    return 'M', [x, y-1]
                elif direction == 'R' and self.is_valid_move([x, y], [x, y+1]):
                    return 'M', [x, y+1]
                else:
                    print("Invalid move. Try again.")
            elif choice == 'W':
                if (self.current_player == 1 and self.p1_walls == 0) or (self.current_player == 2 and self.p2_walls == 0):
                    print("No walls left!")
                    continue
                # Ask for wall position and direction
                direction = input("Wall direction (H)orizontal or (V)ertical: ").strip().upper()
                if direction not in ['H', 'V']:
                    print("Invalid wall direction.")
                    continue
                x = int(input("Row position (0-7): "))
                y = int(input("Column position (0-7): "))
                return 'W', (direction, x, y)

    def play_game(self):
        while True:
            self.display_board()
            action, move = self.get_player_input()
            if action.upper() == 'M':
                self.move_player(move)
                if self.check_win():
                    break
            elif action.upper() == 'W':
                direction, x, y = move
                if self.place_wall(direction, x, y):
                    if self.current_player == 1:
                        self.p1_walls -= 1
                    else:
                        self.p2_walls -= 1
                else:
                    print("Invalid wall placement. Try again.")
                    continue
            self.switch_turn()


if __name__ == "__main__":
    game = Quoridor()
    game.play_game()
