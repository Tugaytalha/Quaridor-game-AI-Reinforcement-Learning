## TODO LIST:
# 1. Implement reset method to reset the game state
# 2. Implement reward system for the RL agent
# 3. Implement play(action)-> state, reward, done, info method for RL agent

class Quoridor:
    def __init__(self, training_mode=False):
        # 9x9 game board
        self.board_size = 9
        self.training_mode = training_mode  # Training mode toggle
        self.reset()

    def reset(self):
        # Reset the game state
        self.p1_pos = [0, 4]  # Player 1 starts at row 0, column 4
        self.p2_pos = [8, 4]  # Player 2 starts at row 8, column 4
        self.p1_walls = 10
        self.p2_walls = 10
        self.horizontal_walls = set()  # Format: (x, y)
        self.vertical_walls = set()    # Format: (x, y)
        self.current_player = 1  # Player 1 starts the game

    def display_board(self):
        if self.training_mode:
            return  # Skip displaying the board in training mode

        # Normal gameplay board display
        for row in range(self.board_size):
            for col in range(self.board_size):
                end = ' '
                if (row, col) in self.vertical_walls or (row - 1, col) in self.vertical_walls:
                    end = '|'
                if [row, col] == self.p1_pos:
                    print('1', end=end)
                elif [row, col] == self.p2_pos:
                    print('2', end=end)
                else:
                    print('.', end=end)
            print()  # Newline after each row

            if row < self.board_size - 1:
                for col in range(self.board_size):
                    if (row, col) in self.horizontal_walls:
                        print('---', end=' ')
                    else:
                        print(' ', end=' ')
                print()

        print(f"Player 1 Walls: {self.p1_walls} | Player 2 Walls: {self.p2_walls}\n")

    def check_wall_between(self, player_pos, new_pos):
        x, y = player_pos
        nx, ny = new_pos

        # Moving horizontally
        if x == nx:
            if y < ny and ((x, y) in self.vertical_walls or (x - 1, y) in self.vertical_walls):
                return False
            if y > ny and ((x, y - 1) in self.vertical_walls or (x - 1, y - 1) in self.vertical_walls):
                return False
        # Moving vertically
        elif y == ny:
            if x < nx and ((x, y) in self.horizontal_walls or (x, y - 1) in self.horizontal_walls):  # Down move blocked
                return False
            if x > nx and (
                    (x - 1, y) in self.horizontal_walls or (x - 1, y - 1) in self.horizontal_walls):  # Up move blocked
                return False
        return True

    def jump_over(self, player_pos, jump_pos, opponent_pos):
        """Handle jumping over the opponent"""
        if not (0 <= jump_pos[0] < self.board_size and 0 <= jump_pos[1] < self.board_size):
            return False  # Jump position out of bounds

        # If the jump is valid (no walls between opponent and jump position)
        if self.check_wall_between(opponent_pos, jump_pos):
            return True

        # # If we can't jump directly, check for diagonal jump
        # x, y = player_pos
        # ox, oy = opponent_pos
        #
        # if x == ox:  # Same row, check left and right diagonal
        #     if self.is_valid_move(player_pos, [x - 1, y]) or self.is_valid_move(player_pos, [x + 1, y]):
        #         return True
        # elif y == oy:  # Same column, check up and down diagonal
        #     if self.is_valid_move(player_pos, [x, y - 1]) or self.is_valid_move(player_pos, [x, y + 1]):
        #         return True

        return False

    def is_valid_move(self, player_pos, new_pos):
        x, y = player_pos
        nx, ny = new_pos
        opponent_pos = self.p1_pos if self.current_player == 2 else self.p2_pos

        # Check if within bounds
        if not (0 <= nx < self.board_size and 0 <= ny < self.board_size):
            return 0

        # Check for jump over opponent
        if [nx, ny] == opponent_pos:
            # Determine direction of the opponent relative to the player
            ox, oy = opponent_pos

            if ox == x - 1 and oy == y:  # Opponent above
                return 2 if self.jump_over(player_pos, [x - 2, y], [x - 1, y]) else 0
            elif ox == x + 1 and oy == y:  # Opponent below
                return 2 if self.jump_over(player_pos, [x + 2, y], [x + 1, y]) else 0
            elif ox == x and oy == y - 1:  # Opponent to the left
                return 2 if self.jump_over(player_pos, [x, y - 2], [x, y - 1]) else 0
            elif ox == x and oy == y + 1:  # Opponent to the right
                return 2 if self.jump_over(player_pos, [x, y + 2], [x, y + 1]) else 0

        # Check for a direct adjacent move (without jumping)
        if abs(nx - x) + abs(ny - y) == 1:
            return 1 if self.check_wall_between(player_pos, new_pos) else 0

        return 0

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
        if self.training_mode:
            return None  # Skip input handling in training mode

        while True:
            choice = input(f"Player {self.current_player}, Move (M) or Place Wall (W)? ").strip().upper()
            if choice == 'M':
                direction = input("Move (U)p, (D)own, (L)eft, (R)ight: ").strip().upper()
                x, y = self.p1_pos if self.current_player == 1 else self.p2_pos
                if direction == 'U':
                    amount = self.is_valid_move([x, y], [x - 1, y])
                    if amount:
                        return 'M', [x - amount, y]
                elif direction == 'D':
                    amount = self.is_valid_move([x, y], [x + 1, y])
                    if amount:
                        return 'M', [x + amount, y]
                elif direction == 'L':
                    amount = self.is_valid_move([x, y], [x, y - 1])
                    if amount:
                        return 'M', [x, y - amount]
                elif direction == 'R':
                    amount = self.is_valid_move([x, y], [x, y + 1])
                    if amount:
                        return 'M', [x, y + amount]
                else:
                    print("Invalid move. Try again.")
            elif choice == 'W':
                if (self.current_player == 1 and self.p1_walls == 0) or (self.current_player == 2 and self.p2_walls == 0):
                    print("No walls left!")
                    continue
                direction = input("Wall direction (H)orizontal or (V)ertical: ").strip().upper()
                if direction not in ['H', 'V']:
                    print("Invalid wall direction.")
                    continue
                x = int(input("Row position (0-7): "))
                y = int(input("Column position (0-7): "))
                return 'W', (direction, x, y)

    def play_game(self):
        while True:
            if not self.training_mode:
                self.display_board()

            if self.training_mode:
                # In training mode, input will be handled differently by the RL algorithm
                action, move = None, None
                # Assuming you provide a method or action list for RL training
            else:
                action, move = self.get_player_input()

            if action == 'M':
                self.move_player(move)
                if self.check_win():
                    break
            elif action == 'W':
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

    def get_game_state(self):
        """Expose the game state for training mode."""
        return {
            "player_1": self.p1_pos,
            "player_2": self.p2_pos,
            "p1_walls": self.p1_walls,
            "p2_walls": self.p2_walls,
            "horizontal_walls": list(self.horizontal_walls),
            "vertical_walls": list(self.vertical_walls),
            "current_player": self.current_player
        }


if __name__ == "__main__":
    game = Quoridor()
    game.play_game()
