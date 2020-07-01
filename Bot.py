from math import log2
from random import randint

import numpy as np

from Board import Board


class Bot:
    def __init__(self, boardSize=(4, 4)):
        self.board = Board(boardSize)

        # For learning
        self.fitness = self.board.score
        self.brain = None

    def useBrain(self, printGame=False):
        # 17 inputs: each cell of the board
        #            reference 1.0
        # 4 outputs: directions to move

        if printGame:
            print(self.board, '\n')

        # Run the bot until the game is over
        while not self.board.isGameOver():
            # ===== Define input vector =====

            # The board itself
            inputs = []
            for row in range(len(self.board.tiles)):
                for col in range(len(self.board.tiles[0])):
                    inputs.append(self.board.tiles[row][col])

            # Reference value
            inputs.append(1.0)

            # ===== End Define Input Vector =====

            # Do the black magic and get output
            outputs = self.brain.activate(inputs) if self.brain is not None else [0] * 4

            # Pick the best possible move
            maxActivation = -10000000
            direction = -1
            for i in range(len(outputs)):
                if outputs[i] > maxActivation and self.board.canMove(i):
                    maxActivation = outputs[i]
                    direction = i

            # Move and place a new tile
            self.board.move(direction)
            self.board.placeTile()

            if printGame:
                print(self.board, '\n', direction, '\n')

        # Update fitness
        self.fitness = self.board.score
