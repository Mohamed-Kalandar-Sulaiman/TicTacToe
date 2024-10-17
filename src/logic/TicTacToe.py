from src.models import Game


class TicTacToeGame:
    def __init__(self, game: Game):
        self.game = game

    def make_move(self, position: int) -> str:
        """Player makes a move at the given position."""
        if self.game.boardState[position] != "_":
            return "Invalid move, position already taken."
        if self.game.isGameOver:
            return "Game is over."

        # Place the move on the board
        self.game.boardState[position] = self.game.currentShape

        # Check if the current player won
        if self.check_winner():
            self.game.isGameOver = True
            self.game.winner = self.game.currentPlayerToMove
            return f"Player {self.game.currentPlayerToMove} wins!"

        # Check if the game is a draw
        if self.check_draw():
            self.game.isGameOver = True
            return "It's a draw!"

        # Switch to the other player
        self.switch_player()
        return f"Player {self.game.currentPlayerToMove}'s turn."

    def switch_player(self):
        """Switch the turn to the other player."""
        self.game.currentPlayerToMove = (
            self.game.players[0]
            if self.game.currentPlayerToMove == self.game.players[1]
            else self.game.players[1]
        )

    def check_winner(self) -> bool:
        """Check if the current player has won the game."""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

        for combo in winning_combinations:
            if all(self.game.boardState[i] == self.game.currentPlayerToMove for i in combo):
                return True
        return False

    def check_draw(self) -> bool:
        """Check if the game is a draw."""
        return "_" not in self.game.boardState  # No empty cells and no winner

    def reset(self):
        """Reset the game board."""
        self.game.boardState = ["_" for _ in range(9)]
        self.game.currentPlayerToMove = self.game.players[0]
        self.game.isGameOver = False
        self.game.winner = None

    def get_board(self):
        """Return the current board state."""
        return self.game.boardState

    def print_board(self):
        """Print the current board in a 3x3 grid format."""
        for row in range(0, 9, 3):
            print(f"{self.game.boardState[row]} | {self.game.boardState[row+1]} | {self.game.boardState[row+2]}")
            if row < 6:
                print("---------")