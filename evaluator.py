# Single-threaded non-shared move evaluator

from copy import deepcopy
from packing import bin2mat, mat2bin, bin2human
import numpy as np
import random
import csv

# Based off 2048 board logic written by github: @bfontaine
class MoveEvaluator:
    # Move constants
    L = 0
    R = 1
    U = 2
    D = 3

    # Load board
    def __init__(self, board):
        self.board = bin2mat(board)

    # Check for win in board
    def win(self, board):
        for row in board:
            for n in row:
                if n == 2048:
                    return True
        return False

    # Run move in simulation to get resultant board
    def sim(self, move):
        prev = deepcopy(self.board)
        mat, score = self.move(move)
        self.board = prev
        return mat2bin(mat), score, np.array_equal(self.board, mat)

    def merge1D(self, line, d):
        if (d == self.L or d == self.U):
            inc = 1
            R = range(3)
        else:
            inc = -1
            R = range(3, 0, -1)

        score = 0
        for i in R:
            if line[i] == 0:
                continue
            if line[i] == line[i + inc]:
                line[i] *= 2
                line[i + inc] = 0
                score += line[i]

        return (line, score)

    def fall1D(self, line, d):
        nl = [c for c in line if c != 0]
        if d == self.U or d == self.L:
            return nl + [0] * (4 - len(nl))
        return [0] * (4 - len(nl)) + nl

    def getCell(self, x, y):
        return self.board[y][x]

    def setCell(self, x, y, v):
        self.board[y][x] = v

    def getLine(self, y):
        return self.board[y]

    def getCol(self, x):
        return [self.getCell(x, i) for i in range(4)]

    def setLine(self, y, l):
        self.board[y] = l[:]

    def setCol(self, x, l):
        for i in range(4):
            self.setCell(x, i, l[i])

    def move(self, d):
        if d == self.L or d == self.R:
            chg, get = self.setLine, self.getLine
        elif d == self.U or d == self.D:
            chg, get = self.setCol, self.getCol
        else:
            return 0

        score = 0

        for i in range(4):
            origin = get(i)
            line = self.fall1D(origin, d)
            collapsed, pts = self.merge1D(line, d)
            new = self.fall1D(collapsed, d)
            chg(i, new)
            score += pts
        return (self.board, score)


class ChaosEvaluator:
    def __init__(self, cache, level, cache_lock, logger):
        self.cache = cache
        self.cache_lock = cache_lock
        self.level = level
        self.logger = logger
        self.cache_insertions = 0

    def eval(self, b_board, i=0):
        mt = [0, 0, 0, 0]

        for m in range(4):
            mt[m] = self.move(b_board, m, i)

        total = sum(mt)
        if total > 0:
            norm = [n / total for n in mt]
        else:
            norm = mt

        return norm, total

    def move(self, b_board, m, i):
        if i == 0:
            self.logger.info("im alive")
        me = MoveEvaluator(b_board)
        new, _, dead = me.sim(m)
        if not dead:
            if new in self.cache:
                return self.cache[new]
            empties = self.empty(new)
            twos = [self.apply(new, n, False) for n in range(empties)]
            fours = [self.apply(new, n, True) for n in range(empties)]
            if i < self.level:
                te = [self.eval(pos, i + 1)[1] for pos in twos]
                fe = [self.eval(pos, i + 1)[1] for pos in fours]
            else:
                te = [self.alive(pos) for pos in twos]
                fe = [self.alive(pos) for pos in fours]
            score = 0.9 * sum(te) + 0.1 * sum(fe)
            self.cache[new] = score
            self.write_cache(new, te, fe)
            return score
        else:
            return 0

    def write_cache(self, newboard, te, fe):
        self.cache_lock.acquire()
        with open("base.csv", "a", encoding="utf-8", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([bin2human(newboard), (sum(te) * 0.9) + (sum(fe) * 0.1)])
        self.cache_lock.release()

    def apply(self, b_new, n=None, four=None):
        if four is None:
            four = random.randint(0, 100) > 90
        cell = 2 + (2 * int(four))
        c = self.empty(b_new)
        if n is None:
            if c > 1:
                n = random.randint(0, c - 1)
            else:
                n = 1
        t = 0
        tb = bin2mat(b_new)
        for y in range(4):
            for x in range(4):
                if t == n and tb[y][x] == 0:
                    tb[y][x] = cell
                    t += 1
                elif tb[y][x] == 0:
                    t += 1
        return mat2bin(tb)

    def alive(self, b_pos):
        lives = 0
        me = MoveEvaluator(b_pos)
        for m in range(4):
            _, _, dead = me.sim(m)
            if not dead:
                lives += 1
        return lives

    def empty(self, board):
        return len(list(filter(lambda x: x == 0,
                               bin2mat(board).reshape((16,)).tolist())))
