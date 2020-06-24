from math import log2

from Board import Board


class Bot:
    def __init__(self, boardSize=(4, 4)):
        self.board = Board(boardSize[0], boardSize[1])

        # For learning
        self.fitness = self.board.score
        self.brain = None
        self.genome = None
        self.genomeID = None

    def reset(self):
        self.board = Board(len(board), len(board[0]))

    def useBrain(self, light):
        # 16 inputs: each cell of the board scaled by log2(x)/(width*height)
        # 4 outputs: how much it wants to go in each direction (take the highest value output)

        # Define input vector
        maxPossibleTileValue = len(self.board) * len(self.board[0])
        inputs = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                inputs.append(log2(self.board[row][col]) / maxPossibleTileValue)
        inputs.append(1.0)

        # Do the black magic and get outputs
        outputs = self.brain.activate(inputs) if self.brain is not None else (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        # Get the index of the max value of outputs and convert to string
        direction = ['left', 'right', 'up', 'down'][outputs.index(max(outputs))]

        # Update board
        self.board.shift(direction)

        # Update fitness
        self.fitness = self.board.score
