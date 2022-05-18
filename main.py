import numpy as np

class Cell():
    def __init__(self, game, position, values) -> None:
        self.game = game
        self.position = position
        self.values = values

class Game():
    def __init__(self, size, num_squares) -> None:
        self.size = size
        self.num_squares = num_squares
        self.cells = np.array([Cell(self, (x, y), np.arange(1, self.num_squares + 1)) for x in range(self.size) for y in range(self.size)])

