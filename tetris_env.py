import torch
import random
import copy

from board import Board
from moves import Moves

class TetrisEnv():
  def __init__(self):
    self.board = Board()
    self.score = 0
  
  def get_possible_states(self):
    possible_rotations = self.board.current_piece.possible_rotations()
    current_rotation = self.board.current_piece.rotation

    possible_states = []
    remaining_moves = self.board.height - self.board.current_piece.y

    for r in range(possible_rotations):
      next_move = None

      min_x = max(self.board.current_piece.x - remaining_moves, 0)
      max_x = min(self.board.current_piece.x + remaining_moves, self.board.width)

      for x in range(min_x, max_x):
        tmp_board = copy.deepcopy(self.board)
        tmp_board.current_piece.set_rotation(r)
        tmp_board.current_piece.set_x(x)

        if not tmp_board.valid_location():
          continue

        # Move down until we can't anymore
        while tmp_board.valid_location():
          tmp_board.current_piece.move_down()
        tmp_board.current_piece.move_up()

        if r != current_rotation:
          next_move = Moves.ROTATE
        elif x < self.board.current_piece.x:
          next_move = Moves.LEFT
        elif x > self.board.current_piece.x:
          next_move = Moves.RIGHT
        else:
          next_move = Moves.NOOP
        
        possible_states.append((tmp_board, next_move))

    return possible_states
  
  def reset(self):
    self.board = Board()
    self.score = 0

  def step(self, action):
    reward = 0

    match action:
      case Moves.ROTATE:
        self.board.rotate()
      case Moves.LEFT:
        self.board.move_left()
      case Moves.RIGHT:
        self.board.move_right()
      case Moves.NOOP:
        pass
      case Moves.DROP:
        reward += self.board.drop_current()

    reward += self.board.drop_current()
    
    terminated = self.board.game_over
    rows_cleared = self.board.clear_rows()
    reward += rows_cleared * 1000
    self.score += reward

    return reward, terminated
