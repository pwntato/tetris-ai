import colors

class Shape():
  def __init__(self, x = 0, y = 0, color = colors.WHITE):
    self.x = x
    self.y = y
    self.color = color
    self.rotation = 0

  def set_y(self, y):
    self.y = y

  def move_down(self):
    self.y += 1

  def move_up(self):
    self.y -= 1

  def set_x(self, x):
    self.x = x

  def move_left(self):
    self.x -= 1

  def move_right(self):
    self.x += 1
  
  def get_color(self):
    return self.color

  def get_position(self):
    pass

  def possible_rotations(self):
    return 4
  
  def set_rotation(self, rotation):
    self.rotation = rotation
    if self.rotation < 0:
      self.rotation = 0
    if self.rotation > self.possible_rotations():
      self.rotation = self.possible_rotations() - 1

  def rotate(self):
    self.rotation += 1
    if self.rotation > 3:
      self.rotation = 0

  def unrotate(self):
    self.rotation -= 1
    if self.rotation < 0:
      self.rotation = 3

class Square(Shape):
  def __init__(self, x = 0, y = 0, color = colors.WHITE):
    super().__init__(x, y - 1, color)

  def possible_rotations(self):
    return 1

  def get_position(self):
    return [
      [self.x, self.y], 
      [self.x + 1, self.y], 
      [self.x, self.y + 1], 
      [self.x + 1, self.y + 1]
    ]

class Tee(Shape):
  def __init__(self, x = 0, y = 0, color = colors.RED):
    super().__init__(x + 1, y, color)

  def get_position(self):
    if self.rotation == 0:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x, self.y - 1], 
      ]
    elif self.rotation == 1:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x + 1, self.y], 
      ]
    elif self.rotation == 2:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x, self.y + 1], 
      ]
    elif self.rotation == 3:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x - 1, self.y], 
      ]

class RightL(Shape):
  def __init__(self, x = 0, y = 0, color = colors.BLUE):
    super().__init__(x + 1, y, color)

  def get_position(self):
    if self.rotation == 0:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x + 1, self.y - 1], 
      ]
    elif self.rotation == 1:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x + 1, self.y + 1], 
      ]
    elif self.rotation == 2:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x - 1, self.y + 1], 
      ]
    elif self.rotation == 3:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x - 1, self.y - 1], 
      ]

class LeftL(Shape):
  def __init__(self, x = 0, y = 0, color = colors.PURPLE):
    super().__init__(x + 1, y, color)

  def get_position(self):
    if self.rotation == 0:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x - 1, self.y - 1], 
      ]
    elif self.rotation == 1:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x + 1, self.y - 1], 
      ]
    elif self.rotation == 2:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x + 1, self.y + 1], 
      ]
    elif self.rotation == 3:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1],
        [self.x - 1, self.y + 1], 
      ]

class RightZ(Shape):
  def __init__(self, x = 0, y = 0, color = colors.YELLOW):
    super().__init__(x + 1, y, color)

  def possible_rotations(self):
    return 2

  def get_position(self):
    if self.rotation % 2 == 0:
      return [
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x, self.y - 1],
        [self.x + 1, self.y - 1], 
      ]
    elif self.rotation % 2 == 1:
      return [
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x + 1, self.y],
        [self.x + 1, self.y + 1], 
      ]

class LeftZ(Shape):
  def __init__(self, x = 0, y = 0, color = colors.ORANGE):
    super().__init__(x + 1, y, color)

  def possible_rotations(self):
    return 2

  def get_position(self):
    if self.rotation % 2 == 0:
      return [
        [self.x - 1, self.y - 1],
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x + 1, self.y], 
      ]
    elif self.rotation % 2 == 1:
      return [
        [self.x + 1, self.y - 1],
        [self.x + 1, self.y],
        [self.x, self.y],
        [self.x, self.y + 1], 
      ]

class Bar(Shape):
  def __init__(self, x = 0, y = 0, color = colors.INDIGO):
    super().__init__(x + 2, y, color)

  def possible_rotations(self):
    return 2

  def get_position(self):
    if self.rotation % 2 == 0:
      return [
        [self.x - 2, self.y],
        [self.x - 1, self.y],
        [self.x, self.y],
        [self.x + 1, self.y], 
      ]
    elif self.rotation % 2 == 1:
      return [
        [self.x, self.y - 2],
        [self.x, self.y - 1],
        [self.x, self.y],
        [self.x, self.y + 1], 
      ]
