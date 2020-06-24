#!/usr/bin/env python
from random import randint

import numpy as np
from tabulate import tabulate


class Board:
    def __init__(self, width=4, height=4):
        self.array = np.zeros((width, height), dtype=np.uint64)
        self.score = 0
        self.gameOver = False

        self.initialize()

    def shift(self, direction):
        if not self.gameOver:
            if direction == 'left':
                for i, row in enumerate(self.array):
                    self.array[i] = self.shiftRow(row)
            elif direction == 'right':
                self.array = np.flip(self.array, 1)
                for i, row in enumerate(self.array):
                    self.array[i] = self.shiftRow(row)
                self.array = np.flip(self.array, 1)
            elif direction == 'up':
                self.array = np.transpose(self.array)
                for i, row in enumerate(self.array):
                    self.array[i] = self.shiftRow(row)
                self.array = np.transpose(self.array)
            else:
                self.array = np.transpose(self.array)
                self.array = np.flip(self.array, 1)
                for i, row in enumerate(self.array):
                    self.array[i] = self.shiftRow(row)
                self.array = np.flip(self.array, 1)
                self.array = np.transpose(self.array)

            # Check if game is over
            self.gameOver = self.checkGameOver()
            if not self.gameOver:
                self.summonNewTile()

    def shiftRow(self, row, debug=False):
        # Shifts elements in a row, combining as necessary
        # Shifts the list "row" to the left

        # Find first nonzero element
        minIndex = -1
        for i in range(1, len(row)):  # First element either needs to stay put or is 0 and will be overwritten later
            if debug:
                print(row)
            if row[i] != 0:
                # Find previous nonzero element
                prevNonzeroIndex = -1
                for j in range(i - 1, minIndex, -1):
                    if row[j] != 0:
                        prevNonzeroIndex = j
                        break

                if debug:
                    print(i, prevNonzeroIndex, minIndex)
                    input()

                # If prevNonzeroIndex is -1, just move the element to the left (minIndex + 1)
                if prevNonzeroIndex == -1:
                    if debug:
                        print('shift to minIndex + 1')
                    row[minIndex + 1] = row[i]
                    row[i] = 0
                    nexIndex = 1

                # If row at i and prevNonzeroIndex are the same, combine them
                elif row[i] == row[prevNonzeroIndex]:
                    if debug:
                        print('combine')
                    self.score += int(row[prevNonzeroIndex] * 2)
                    row[prevNonzeroIndex] *= 2
                    row[i] = 0
                    nextIndex = prevNonzeroIndex + 1
                    minIndex += 1

                # Otherwise, they're different nonzero numbers. Move the right one as left as possible
                elif i - prevNonzeroIndex > 1:
                    if debug:
                        print('move left')
                    row[prevNonzeroIndex + 1] = row[i]
                    row[i] = 0
                    nextIndex = prevNonzeroIndex + 2
        return row

    def checkGameOver(self):
        for row in range(len(self.array)):
            for col in range(len(self.array[0])):
                if self.array[row][col] == 0:
                    return False
                if row + 1 < len(self.array):
                    if self.array[row + 1][col] == self.array[row][col]:
                        return False
                if row - 1 >= 0:
                    if self.array[row - 1][col] == self.array[row][col]:
                        return False
                if col + 1 < len(self.array[0]):
                    if self.array[row][col + 1] == self.array[row][col]:
                        return False
                if col - 1 >= 0:
                    if self.array[row][col - 1] == self.array[row][col]:
                        return False
        return True

    def summonNewTile(self):
        # Check that there's an open space to summon a tile
        openSpace = False
        for row in range(len(self.array)):
            for col in range(len(self.array[0])):
                if self.array[row][col] == 0:
                    openSpace = True
                    break

        # If there's an open space, summon a tile:
        if openSpace:
            row = randint(0, len(self.array) - 1)
            col = randint(0, len(self.array[0]) - 1)
            while self.array[row][col] != 0:
                row = randint(0, len(self.array) - 1)
                col = randint(0, len(self.array[0]) - 1)
            self.array[row][col] = 2 if randint(0, 9) != 0 else 4

    def initialize(self):
        for _ in range(2):
            self.summonNewTile()
        self.score = 0
        self.gameOver = False

    def __str__(self):
        return f'Score: {self.score}\n' + tabulate(self.array, tablefmt='plain')


if __name__ == '__main__':
    b = Board()

    print(b)

    while True:
        direction = ['left', 'right', 'up', 'down'][randint(0, 3)]
        print(str(b.gameOver) + '\n' + direction + '\n')
        b.shift(direction)
        print(b)
        if b.gameOver:
            print('Game over')
            break
        input()