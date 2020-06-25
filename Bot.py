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

    def useBrain(self, printGame=False):
        # 86 inputs: each cell of the board
        #            the count of nonzero cells
        #            preview of each of the 4 possible next-state boards and their scores
        # 1 output: direction to move

        if printGame:
            print(self.board, '\n')

        # Run the bot until the game is over
        while not self.board.checkGameOver():
            # Define input vector

            # The board itself
            inputs = []
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    inputs.append(self.board.array[row][col])

            # The number of nonzero tiles
            nonZeroTileCount = 0
            for row in range(len(self.board.array)):
                for col in range(len(self.board.array[0])):
                    if self.board.array[row][col] != 0:
                        nonZeroTileCount += 1
            inputs.append(nonZeroTileCount)

            # Add peeks of the possible moves
            for direction in ['left', 'right', 'up', 'down']:
                arr, score = self.board.peek(direction)
                for row in arr:
                    for cell in row:
                        inputs.append(cell)
                inputs.append(score)

            # Reference value
            inputs.append(1.0)
            # print(inputs)

            # Do the black magic and get output
            outputs = self.brain.activate(inputs) if self.brain is not None else [0 for _ in range(86)]

            directions = ['left', 'right', 'up', 'down']

            # Make all unavailable moves have tiny activation values
            for i in range(len(outputs)):
                if np.array_equal(self.board.peek(directions[i])[0], self.board.array):
                    outputs[i] = -100000

            # Pick the best output
            maxActivation = max(outputs)
            maxActivationIndex = outputs.index(maxActivation)
            direction = directions[maxActivationIndex]

            # Update board
            self.board.move(direction)

            if printGame:
                print(self.board, '\n')

        # Update fitness
        self.fitness = self.board.score

        # Update isRunning of game is over
        self.isRunning = self.board.gameOver
