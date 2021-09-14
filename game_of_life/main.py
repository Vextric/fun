from time import sleep, time
from datetime import datetime

import os
import argparse
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

clear_console = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

# TODO: use numpy and add ability to use pre-determined seeds or random ones
class GameOfLife():
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self.board = []

        self.create_board()

    def create_board(self):
        state_list = []

        for x in range(self.cols):
            for y in range(self.rows):
                state_list.append(1 if random.randint(1, 10) < 2 else 0)

            self.board.insert(x + y, state_list)
            state_list = []

    def iterate(self, frame_num, img):
        first_time = datetime.now()
        new_board = [list(range(self.rows)) for i in range(self.cols)]

        for x in range(self.cols):
            for y in range(self.rows):
                new_board[x][y] = self.apply_rules(
                    x, y,
                    self.board[x][y]
                )

        self.board = new_board
        img.set_data(self.board)
        lag = datetime.now() - first_time
        print('lag in each animation: ', lag)
        return img,

    def apply_rules(self, x: int, y: int, state: int):
        neighbors = 0

        for _x in range(x - 1, x + 2):
            for _y in range(y - 1, y + 2):
                neighbors += self.board[(_x + self.cols) % self.cols][(_y + self.rows) % self.rows]

        if state:
            neighbors -= 1;

        return 1 if neighbors == 3 or (neighbors == 2 and state) else 0

    def draw_board(self):
        clear_console()

        for y in range(self.rows):
            for x in range(self.cols):
                print('+' if self.board[x][y] else ' ', end='')
            print('\n', end='')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    parser.add_argument('-C', '--col', dest='col', type=int, default='100', required=False,
                        help='determine how many columns should the grid be. default: 100')
    parser.add_argument('-R', '--row', dest='row', type=int, default='150', required=False,
                        help='determine how many Rows should the grid be. default: 150')
    parser.add_argument('-I', '--itr', dest='itr', type=int, default='50',  required=False,
                        help='set interval of the animation. default: 50ms')
    args = parser.parse_args()

    game_of_life = GameOfLife(int(args.col), int(args.row))

    fig, ax = plt.subplots()
    img = ax.imshow(game_of_life.board, interpolation='nearest')
    ani = animation.FuncAnimation(fig, game_of_life.iterate, fargs=(img, ),
                                  frames=40, interval=args.itr, save_count=25)

    plt.show()
