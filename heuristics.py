from abc import ABC, abstractmethod
import determineBestMove

from detBestMoveHannes import getLegalMoves
"""
This file is where the heuristics are defined. All of them are returned normalized with values between zero and one with one being the best possible value.
"""


class BasicHeuristic(ABC):

  @abstractmethod
  def normalizedHeuristic(self, game_state) -> float:
    pass


class AreaAroundHead(BasicHeuristic):
  """
  Evaluates the space around our head in a 5x5 square.
  Returns one if we have the most space possible and zero if we have none.
  """

  def normalizedHeuristic(self, game_state):
    my_head = game_state.own_body[0]
    my_body = game_state.own_body
    op_body = game_state.opp_body

    upper_left = (my_head["x"] - 2, my_head["y"] + 2)
    upper_right = (my_head["x"] + 2, my_head["y"] + 2)
    lower_left = (my_head["x"] - 2, my_head["y"] - 2)
    obstacles = 0
    body = False
    for i in range(upper_left[0], upper_right[0] + 1):
      for j in range(lower_left[1], upper_left[1] + 1):
        for my_part in my_body:
          for op_part in op_body:
            if (my_part["x"] == i
                and my_part["y"] == j) or (op_part["x"] == i
                                           and op_part["y"] == j):
              body = True

        if body:
          obstacles += 1
          body = False
    return 1 - (obstacles / 22)


class OwnHealth(BasicHeuristic):
  """
  Returns one if we have full health and zero if we have none.
  If the opponent is larger than we are, we subtract the difference in length from our health 
  to make the snake more hungry.
  """

  def normalizedHeuristic(self, game_state):
    health = game_state.own_health
    health -= 50
    len_diff = len(game_state.opp_body) - len(game_state.own_body)
    if len_diff > 0:
      health -= len_diff * 4
    if health < 0:
      health = 0
    return health / 50


class DistanceOfHeads(BasicHeuristic):
  """
  Returns one, if heads are in opposite corners and zero if they are directly next to each other.
  """

  def normalizedHeuristic(self, game_state):
    my_head = game_state.own_body[0]
    op_head = game_state.opp_body[0]
    my_body = game_state.own_body
    op_body = game_state.opp_body

    opp_larger = False
    if len(op_body) >= len(my_body):
      opp_larger = True
      
    trueDistance = abs(my_head["x"] - op_head["x"]) + abs(my_head["y"] -
                                                            op_head["y"])
    
    min_val = 0
    max_val = 20
    if opp_larger:
      return (trueDistance - min_val) / (max_val - min_val)
    else:
      return 1 - (trueDistance - min_val) / (max_val - min_val)


class SpaceSimple(BasicHeuristic):
  """
  Evaluates the space around our head. Adds seven distances: front, left, right, front-left, front-right, back-left, back-right.
  Returns one if we have the most space possible and zero if we have none.
  """

  @staticmethod
  def is_in_body(x, y, body):
    return any(segment["x"] == x and segment["y"] == y for segment in body)

  def normalizedHeuristic(self, game_state):
    x_origin = game_state.own_body[0]["x"]
    y_origin = game_state.own_body[0]["y"]
    body1 = game_state.own_body
    body2 = game_state.opp_body

    spaces = 0
    # straight line checks
    # check in x direction
    for i in range(10 - x_origin):
      if self.is_in_body(x_origin + i + 1, y_origin, body1) or self.is_in_body(
          x_origin + i + 1, y_origin, body2):
        break
      spaces += 1
    for i in range(x_origin):
      if self.is_in_body(x_origin - i - 1, y_origin, body1) or self.is_in_body(
          x_origin - i - 1, y_origin, body2):
        break
      spaces += 1
    # check in y direction
    for i in range(10 - y_origin):
      if self.is_in_body(x_origin, y_origin + i + 1, body1) or self.is_in_body(
          x_origin, y_origin + i + 1, body2):
        break
      spaces += 1
    for i in range(y_origin):
      if self.is_in_body(x_origin, y_origin - i - 1, body1) or self.is_in_body(
          x_origin, y_origin - i - 1, body2):
        break
      spaces += 1
    # diagonal checks
    # to top right
    for i in range(min(10 - x_origin, 10 - y_origin)):
      if self.is_in_body(x_origin + i + 1,
                         y_origin + i + 1, body1) or self.is_in_body(
                             x_origin + i + 1, y_origin + i + 1, body2):
        break
      spaces += 1
    # to bottom right
    for i in range(min(10 - x_origin, y_origin)):
      if self.is_in_body(x_origin + i + 1,
                         y_origin - i - 1, body1) or self.is_in_body(
                             x_origin + i + 1, y_origin - i - 1, body2):
        break
      spaces += 1
    # to top left
    for i in range(min(x_origin, 10 - y_origin)):
      if self.is_in_body(x_origin - i - 1,
                         y_origin + i + 1, body1) or self.is_in_body(
                             x_origin - i - 1, y_origin + i + 1, body2):
        break
      spaces += 1
    # to bottom left
    for i in range(min(x_origin, y_origin)):
      if self.is_in_body(x_origin - i - 1,
                         y_origin - i - 1, body1) or self.is_in_body(
                             x_origin - i - 1, y_origin - i - 1, body2):
        break
      spaces += 1
    return spaces / 40

class ToMiddle(BasicHeuristic):
  """
  Bias to the middle of the board
  """
  def normalizedHeuristic(self, game_state):
    my_head = game_state.own_body[0]
    middle_x = 5
    middle_y = 5
    distance_to_middle = abs(my_head["x"] - middle_x) + abs(my_head["y"] - middle_y)
    return 1 - (distance_to_middle / 10)

class NumberOfMoves(BasicHeuristic):
  """
  Returns 1 if three moves are possible and 0 if only one is possible
  """
  def normalizedHeuristic(self, game_state):
    possible_moves = determineBestMove.getSafeMoves(game_state, True)
    if not possible_moves:
      possible_moves = determineBestMove.getLegalMoves(game_state, True)
      if not possible_moves:
        return 0
    return len(possible_moves) / 3
