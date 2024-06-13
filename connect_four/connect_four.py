import sys
import enum

class GridPosition(enum.Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2

class Player:
    def __init__(self, name, grid_piece: GridPosition):
        self._name = name
        self._grid_piece = grid_piece # GridPosition object

    def get_name(self):
        return self._name

    def get_grid_piece(self):
        return self._grid_piece

class Grid:
    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._grid = []
        self.reset_grid()

    def reset_grid(self):
        self._grid = [[GridPosition.EMPTY for col in range(self._cols)]
                      for row in range(self._rows)]

    def get_rows(self):
        return self._rows

    def get_cols(self):
        return self._cols

    def get_grid(self):
        return self._grid

    def place_piece(self, col, grid_piece):
        # Find empty col, then change grid position to specific color
        if col < 0 or col >= self._cols:
            raise ValueError('Col < 0 or >= grid columns')
        for row in range(self._rows-1, -1, -1):
            if self._grid[row][col] == GridPosition.EMPTY:
                self._grid[row][col] = grid_piece
                return row
        raise ValueError('Col completely filled already')

    def check_win(self, connectN, row, col, grid_piece) -> bool:
        # Check whole grid or only locally based on col?
        # Check on row/col spot with piece returns if win or not
        # Horizontal
        count = 0
        for c in range(self._cols):
            if self._grid[row][c] == grid_piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        # Vert
        count = 0
        for r in range(self._rows):
            if self._grid[r][col] == grid_piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
        # Matrix Diagonal goes top left to bottom right
        count = 0
        new_col, new_row = col, row
        # Move pt to top left
        while new_col > 0 and new_row > 0:
            new_col -= 1
            new_row -= 1
        while new_col < self._cols and new_row < self._rows:
            if self._grid[new_row][new_col] == grid_piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
            new_col += 1
            new_row += 1
        # Anti-diag
        count = 0
        new_col, new_row = col, row
        # Move pt to top right
        while new_col < self._cols and new_row < 0:
            new_col += 1
            new_row -= 1
        while new_col >= 0 and new_row < self._rows:
            if self._grid[new_row][new_col] == grid_piece:
                count += 1
            else:
                count = 0
            if count == connectN:
                return True
            new_col -= 1
            new_row += 1
        return False

class Game:
    def __init__(self, grid, connect_n, target_score):
        self._grid = grid
        self._connect_n = connect_n
        self._target_score = target_score
        self._players = [
            Player('one', GridPosition.RED),
            Player('two', GridPosition.YELLOW)
        ]
        self._score = {}
        self.reset_score()

    def reset_score(self):
        for player in self._players:
            self._score[player.get_name()] = 0

    def play(self):
        while True:
            play = input('Play y / n?')
            if play == 'y':
                self.reset_score()
                while True:
                    print('Start Round')
                    self._grid.reset_grid()
                    print('---------------------------')
                    winner = self.play_round()
                    self._score[winner.get_name()] += 1
                    print(f'*** {winner.get_name()} wins this round!')
                    if self._score[winner.get_name()] == self._target_score:
                        print(f'!!! {winner.get_name()} wins the game!')
                        break
            elif play == 'n':
                sys.exit(0)

    def play_round(self):
        self._grid.reset_grid()
        while True:
            for player in self._players:
                move_row, move_col = self.play_move(player)
                if self._grid.check_win(self._connect_n,
                                        move_row,
                                        move_col,
                                        player.get_grid_piece()):
                    return player

    def play_move(self, player):
        self.print_grid()
        print(f"{player.get_name()}'s turn:")
        move_col = int(input(f'Pick a column between. 0 - {self._grid.get_cols() - 1}: '))
        move_row = self._grid.place_piece(move_col, player.get_grid_piece())
        return (move_row, move_col)

    def print_grid(self):
        grid = self._grid.get_grid()
        for row in range(len(grid)):
            print(f'{row}: ', end= '')
            for col in range(len(grid[0])):
                piece = grid[row][col]
                if piece == GridPosition.EMPTY:
                    print(' 0 ', end=' | ')
                elif piece == GridPosition.YELLOW:
                    print(' Y ', end=' | ')
                elif piece == GridPosition.RED:
                    print(' R ', end=' | ')
            print('')

def main():
    grid = Grid(rows=2, cols=4)
    game = Game(grid, connect_n=2, target_score=2)
    game.play()

if __name__ == '__main__':
    main()
    