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

        # Save the previous 3 moves to make sure it doesn't do the same thing over and over
        moveHistory = []

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

            # Figure out which moves are available
            lockedMove = None
            if len(moveHistory) >= 3:
                for move in moveHistory:
                    if moveHistory.count(move) == len(moveHistory):
                        lockedMove = move
                        break

            # Pick a direction
            if outputs[0] <= 0.25:
                direction = 'left'
            elif outputs[0] <= 0.5:
                direction = 'right'
            elif outputs[0] <= 0.75:
                direction = 'up'
            else:
                direction = 'down'

            # Pick a random direction if the move selected is locked
            while direction == lockedMove:
                direction = ['left', 'right', 'up', 'down'][randint(0, 3)]

            # Update move history
            moveHistory.append(direction)
            if len(moveHistory) > 3:
                moveHistory.pop(0)

            # Update board
            self.board.move(direction)

            if printGame:
                print(self.board, '\n')

        # Update fitness
        self.fitness = self.board.score

        # Update isRunning of game is over
        self.isRunning = self.board.gameOver
