from math import log2
from random import randint

from Board import Board


class Bot:
    def __init__(self, boardSize=(4, 4)):
        self.board = Board(boardSize[0], boardSize[1])
        self.isRunning = True

        # For learning
        self.fitness = self.board.score
        self.brain = None

    def useBrain(self):
        # 16 inputs: each cell of the board scaled by log2(x)/(width*height)
        # 4 outputs: how much it wants to go in each direction (take the highest value output)

        # Run the bot until the game is over
        while not self.board.checkGameOver():
            # Define input vector
            maxPossibleTileValue = len(self.board.array) * len(self.board.array[0])
            inputs = []
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    if self.board.array[row][col] == 0:
                        inputs.append(0)
                    else:
                        inputs.append(log2(self.board.array[row][col]) / maxPossibleTileValue)
            inputs.append(1.0)

            # Do the black magic and get outputs
            outputs = self.brain.activate(inputs) if self.brain is not None else (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

            # Get max value of outputs
            maxVal = max(outputs)

            # Find indicies of maxVal
            options = []
            for i in range(len(outputs)):
                if outputs[i] == maxVal:
                    options.append(i)

            # Pick a random option
            selection = options[randint(0, len(options) - 1)]

            # Convert option to string
            direction = ['left', 'right', 'up', 'down'][selection]

            # Update board
            self.board.shift(direction)

        # Update fitness
        self.fitness = self.board.score

        # Update isRunning of game is over
        self.isRunning = self.board.gameOver
