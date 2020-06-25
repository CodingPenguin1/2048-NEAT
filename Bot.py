from math import log2
from random import randint

import numpy as np

from Board import Board


class Bot:
    def __init__(self, boardSize=(4, 4)):
        self.board = Board(boardSize[0], boardSize[1])
        self.isRunning = True

        # For learning
        self.fitness = self.board.score
        self.brain = None

    def useBrain(self):
        # 86 inputs: each cell of the board scaled by log2(x)/(width*height+1)
        #            the count of nonzero cells
        #            each cell of the board that would result from each move and their scores
        # 4 outputs: how much it wants to go in each direction (take the highest value output)

        # Run the bot until the game is over
        while not self.board.checkGameOver():
            # Define input vector

            # The board itself
            maxPossibleTileValue = 2 ** (1 + len(self.board.array) * len(self.board.array[0]))
            inputs = []
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    if self.board.array[row][col] == 0:
                        inputs.append(0)
                    else:
                        inputs.append(log2(self.board.array[row][col]) / maxPossibleTileValue)

            # The number of nonzero tiles
            nonZeroTileCount = 0
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    if self.board.array[row][col] != 0:
                        nonZeroTileCount += 1
            nonZeroTileCount /= len(self.board.array) + len(self.board.array[0])
            inputs.append(nonZeroTileCount)

            # What each board would look like with each potential move from the current board
            for direction in ['left', 'right', 'up', 'down']:
                nextBoard = Board(len(self.board.array), len(self.board.array[0]))
                nextBoard.array = np.copy(self.board.array)
                nextBoard.move(direction)
                score = nextBoard.score

                # Move board array into a list and scale
                nextBoardValues = []
                for row in nextBoard.array:
                    for cell in row:
                        if cell != 0:
                            nextBoardValues.append(log2(cell) / maxPossibleTileValue)
                        else:
                            nextBoardValues.append(cell)

                # Add to score
                for i in nextBoardValues:
                    inputs.append(i)
                inputs.append(score)

            # Reference value
            inputs.append(1.0)
            # print(inputs)

            # Do the black magic and get outputs
            outputs = self.brain.activate(inputs) if self.brain is not None else [0 for _ in range(5 * (len(self.board.array) * len(self.board.array[0]) + 1) + 2)]

            # Try moves from highest to lowest value
            # If a proposed move does nothing, try the next most favored
            directions = ['left', 'right', 'up', 'down']
            while True:
                bestOption = outputs.index(max(outputs))
                direction = directions[bestOption]

                # See if move does anything
                candidateArray = self.board.shift(direction, changeScore=False)
                if not np.array_equal(candidateArray, self.board.array):
                    break
                else:
                    outputs[bestOption] = -1

            # Update board
            self.board.move(direction)

        # Update fitness
        self.fitness = self.board.score

        # Update isRunning of game is over
        self.isRunning = self.board.gameOver
