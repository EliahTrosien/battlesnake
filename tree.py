from __future__ import annotations
from typing import Optional

class gamestate:
    own_body: list[tuple[int, int]]     # saves the body of own snake, with head being own_body[0] 
    own_health: int                     # saves the own current health: 0 < own_health <= 100
    opp_body: list[tuple[int, int]]     # saves the body of opponents snake, with head being opp_body[0]
    opp_health: int                     # saves the opponents current health: 0 < opp_health <= 100
    food: list[tuple[int, int]]         # saves all the places where food is (might be sorted in some way, don't know, does not matter)
    
    def __init__(self, server_response):
        self.own_body = server_response.snakes[0].body
        self.own_health = server_response.snakes[0].health
        self.opp_body = server_response.snakes[1].body
        self.opp_health = server_response.snakes[1].health
        self.food = server_response.food

class gametree:
    def __init__(self, value: int, own_move: bool, gamestate: gamestate, up: Optional[gametree] = None, down: Optional[gametree] = None, 
                left: Optional[gametree] = None, right: Optional[gametree] = None):
        self.value = value          # saves how desireable the position is
        self.own_move = own_move    # if uesd Min/Max-Search 
                                    # True means Max search -> Own Move
                                    # False means Min search -> Opp Move (or switched)
        # self.height = height      # saves the min depth of tree, might be useful to find where we need to continue calculating
        self.gamestate = gamestate  # holds the game state so we do not need to recalc it
        self.up = up                # link to the tree if snake goes up
        self.down = down            # link to the tree if snake goes down
        self.left = left            # link to the tree if snake goes left
        self.right = right          # link to the tree if snake goes right

# dann legt man einen Baum an
# sagt: Wenn neuer gamestate da ist, schaue welcher Pfad gegangen wurde -> setz das als neue wurzel des Baums
# rechne einfach weiter
# !!! sehr speicher aufwändig -> muss schauen, ob das geht
