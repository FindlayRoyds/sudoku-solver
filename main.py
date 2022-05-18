import numpy as np
from copy import deepcopy

class Cell():
    def __init__(self, game, position, values) -> None:
        self.game = game
        self.position = position
        self.values = values
    
    def set_values(self, values):
        self.values = values
    
    def analyse(self):
        self.analyse_row()
        self.analyse_column()
        self.analyse_square()

    def analyse_row(self):
        for cell in self.game.get_cells_in_row(self.position[0]):
            if cell == self: continue
            if len(cell.values) == 1:
                self.values = self.values[self.values != cell.values[0]]

    def analyse_column(self):
        for cell in self.game.get_cells_in_column(self.position[1]):
            if cell == self: continue
            if len(cell.values) == 1:
                self.values = self.values[self.values != cell.values[0]]
    
    def analyse_square(self):
        square_pos = self.game.get_square_position(self)
        cells = self.game.get_cells_in_square(square_pos)
        for cell in self.game.get_cells_in_square(square_pos):
            if cell == self: continue
            if len(cell.values) == 1:
                self.values = self.values[self.values != cell.values[0]]
    
    def __repr__(self):
        #return str(self.values)
        return str(self.values[0]) + ' ' if len(self.values) == 1 else '  '

class Game():
    def __init__(self, num_cells) -> None:
        self.num_cells = num_cells
        self.cells = np.empty([num_cells, num_cells], dtype=object)
        for x in range(num_cells):
            for y in range(num_cells):
                self.cells[y, x] = Cell(
                    self, np.array([y, x]), np.arange(1, num_cells + 1)
                )

        self.num_squares = np.sqrt(self.num_cells)
        self.square_size = self.num_cells / self.num_squares
    
    def get_cell(self, position):
        return self.cells[position[0], position[1]]
    
    def get_square_position(self, cell):
        return np.array([
            cell.position[0] // self.square_size,
            cell.position[1] // self.square_size
        ])
    
    def set_cell(self, position, values):
        self.get_cell(position).set_values(values)
    
    def set_state(self):
        for y in range(self.num_cells):
            line = input(f"{y}: ")
            for x, value in enumerate(line):
                if value == ' ':
                    self.set_cell((y, x), np.arange(1, self.num_cells + 1))
                else:
                    self.set_cell((y, x), np.array([int(value)]))
    
    def get_solved_state(self):
        return np.array([[len(cell.values) for cell in row] for row in self.cells])
    
    def analyse(self):
        i = 0
        for row in self.cells:
            for cell in row:
                i += 1
                cell.analyse()
    
    def complete_analysis(self):
        prev_state = self.get_solved_state()
        while True:
            self.analyse()
            state = self.get_solved_state()
            if (state == prev_state).all():
                return False
            else:
                solved = np.all(state == 1)
                print(self)
                input()
                if solved:
                    return True
    
    def get_cells_in_row(self, row):
        return self.cells[row]
    
    def get_cells_in_column(self, column):
        return self.cells[:, column]
    
    def get_cells_in_square(self, square_position):
        square_top_left = square_position * self.square_size
        cells = []
        for y in range(0, int(self.square_size)):
            for x in range(0, int(self.square_size)):
                cells.append(
                    self.get_cell((int(square_top_left[0] + y), int(square_top_left[1] + x)))
                )
        return cells

    def __repr__(self):
        return '\n'.join([''.join(str(cell) for cell in row) for row in self.cells])

game = Game(int(input("Size: ")))
game.set_state()
solved = game.complete_analysis()
print(f"Solved: {solved}")
print(game)