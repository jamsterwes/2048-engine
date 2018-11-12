import json
import numpy as np
from evaluator import MoveEvaluator, ChaosEvaluator
from packing import mat2bin, bin2mat, bin2human


class Game:
    def __init__(self, start, queue, id, level):
        self.id = id
        self.level = level
        self.queue = queue

    def run(self, moves, board, cache, cache_queue, logger):
        logger.info("moving...")
        self.board = np.array(board).reshape((4,4))
        self.board = self.move(self.board, cache, cache_queue, logger)
        board[:] = self.board.reshape((16,)).tolist()[:]
        self.queue.put([self.id, moves + 1, json.dumps(self.board.tolist()), bin2human(mat2bin(self.board))])


    def move(self, board, cache, cache_queue, logger):
        me = MoveEvaluator(mat2bin(board))
        ce = ChaosEvaluator(cache, self.level, cache_queue, logger)
        ce_res = ce.eval(mat2bin(board))[0]
        return bin2mat(ce.apply(me.sim(np.argmax(ce_res))[0]))
