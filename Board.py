#!/usr/bin/env python
import numpy as np
from tabulate import tabulate
from random import randint


class Board:
    def __init__(self, width=4, height=4):
        self.array = np.zeros((width, height), dtype=np.uint64)

    def shift(self, direction):
        pass

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

    def __str__(self):
        return tabulate(self.array, tablefmt='plain')


def randMult2():
    return [0, 2, 4, 8, 16][randint(0, 4)]


if __name__ == '__main__':
    b = Board()

    debug = False

    a = [16, 0, 2, 0, 2, 16, 16, 0]
    if not debug:
        a = [randMult2() for _ in range(len(a))]
    print(a)
    a = b.shiftRow(a, debug=debug)

    print(a)
