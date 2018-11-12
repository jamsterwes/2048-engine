from game import Game
from multiprocessing import Process, Array, Lock, Queue
from packing import human2bin, bin2mat, bin2human
import csv
import time

def loop_game(i, start, queue, cache, cf_lock, level, logger):
    start = bin2mat(human2bin(start))
    game = Game(start, queue, i, level)
    board = Array('f', range(16))
    board[:] = start.reshape((16,)).tolist()[:]
    moves = 0
    while True:
        p = Process(target=game.run, args=(moves, board, cache, cf_lock, logger))
        p.start()
        p.join()
        del p
        moves += 1



class Hoard:
    def __init__(self, queue, n, level=2):
        self.queue = queue
        self.level = level
        self.n = n
        self.cf_lock = Lock()

    def run(self, start, cache, logger):
        t = []
        for i in range(self.n):
            thread = Process(target=loop_game, args=(i, start, self.queue, cache, self.cf_lock, self.level, logger))
            thread.start()
            t.append(thread)
