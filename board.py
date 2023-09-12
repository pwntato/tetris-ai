import random
import copy

import draw
from piece import Square, Tee, RightL, LeftL, RightZ, LeftZ, Bar

class Board():
  def __init__(self, width=10, height=20, square_size=25):
    self.width = width
    self.height = height + 2
    self.square_size = square_size
    self.x_offest = self.square_size
    self.y_offest = self.square_size * 3
    self.empty = None
    self.board = []
    for x in range(self.width):
      self.board.append([])
      for y in range(self.height):
        self.board[x].append(self.empty)
    self.next_piece = None
    self.start_x = 4
    self.start_y = 1
    self.pieces = [Square, Tee, RightL, LeftL, RightZ, LeftZ, Bar]
    self.add_piece()
    self.game_over = False

  def add_piece(self):
    self.current_piece = self.next_piece
    if self.current_piece is None:
      self.current_piece = random.choice(self.pieces)(self.start_x, self.start_y)
    self.next_piece = random.choice(self.pieces)(self.start_x, self.start_y)

  def drop_current(self):
    self.current_piece.move_down()
    if not self.valid_location():
      self.current_piece.move_up()
      # landed
      score = 0
      for coords in self.current_piece.get_position():
        self.board[coords[0]][coords[1]] = self.current_piece.get_color()

        #score += coords[1] # * 10
        score += 1

        if coords[1] < 2:
          self.game_over = True
          return -1
      self.add_piece()
      return score
    return 0

  def move_right(self):
    self.current_piece.move_right()
    if not self.valid_location():
      self.current_piece.move_left()

  def move_left(self):
    self.current_piece.move_left()
    if not self.valid_location():
      self.current_piece.move_right()
  
  def rotate(self):
    self.current_piece.rotate()
    if not self.valid_location():
      self.current_piece.unrotate()

  def valid_location(self):
    for coords in self.current_piece.get_position():
      if coords[0] < 0 or coords[0] >= self.width:
        return False
      if coords[1] < 0 or coords[1] >= self.height:
        return False
      if self.board[coords[0]][coords[1]] != self.empty:
        return False

    return True

  def clear_rows(self):
    rows = []
    for y in range(self.height):
      if self.is_full(y):
        rows.append(y)
    for y in rows:
      self.delete_row(y)
    return len(rows)

  def delete_row(self, y):
    for x in range(self.width):
      self.board[x][y] = self.board[x][y - 1]
    if y > 2:
      self.delete_row(y - 1)

  def is_full(self, y):
    for x in range(self.width):
      if self.board[x][y] == self.empty:
        return False
    return True

  def is_empty(self, y):
    for x in range(self.width):
      if self.board[x][y] != self.empty:
        return False
    return True

  def get_state(self):
    state = copy.deepcopy(self.board)

    for coords in self.current_piece.get_position():
      state[coords[0]][coords[1]] = self.current_piece.get_color()

    for coords in self.next_piece.get_position():
      state[coords[0]][coords[1]] = self.next_piece.get_color()

    return state
  
  def holes(self):
    holes = 0
    for x in range(self.width):
      found = False
      for y in range(self.height):
        if self.board[x][y] != self.empty:
          found = True
        elif found:
          holes += 1
    return holes

  def bumpiness(self):
    bumpiness = 0
    heights = self.heights()
    for x in range(self.width - 1):
      bumpiness += abs(heights[x] - heights[x + 1])
    return bumpiness
  
  def heights(self):
    heights = []
    for x in range(self.width):
      max_y = self.height
      for y in range(self.height):
        if self.board[x][y] != self.empty:
          max_y = y
          break
      heights.append(self.height - max_y)
    return heights
  
  def max_height(self):
    return max(self.heights())
  
  def get_stats(self):
    # add current piece
    for coords in self.current_piece.get_position():
        self.board[coords[0]][coords[1]] = self.current_piece.get_color()

    lines = self.clear_rows()
    holes = self.holes()
    bumpiness = self.bumpiness()
    max_height = self.max_height()

    # remove current piece
    for coords in self.current_piece.get_position():
        self.board[coords[0]][coords[1]] = self.empty

    return  lines, \
            holes, \
            bumpiness, \
            max_height

  def render(self, surface):
    state = self.get_state()

    for x in range(len(state)):
      for y in range(len(state[x])):
        if state[x][y] is not None:
          draw.full_square(
            surface, 
            state[x][y],
            (x * self.square_size) + self.x_offest,
            (y * self.square_size) + self.y_offest - (2 * self.square_size),
            self.square_size,
            self.square_size
          )
        draw.empty_square(
          surface, 
          (128, 128, 128),
          (x * self.square_size) + self.x_offest,
          (y * self.square_size) + self.y_offest - (2 * self.square_size),
          self.square_size,
          self.square_size
        )
