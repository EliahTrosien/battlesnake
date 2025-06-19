import threading
import evaluatePosition
import queue
import time
from typing import Optional
from copy import deepcopy

from main import gameState


class Node:
    gamestate: gameState

    def __init__(self, game_state):
        self.depth: int = 0
        self.utility: float = 0.0
        self.gamestate = game_state
        self.up: Optional['Node'] = None
        self.down: Optional['Node'] = None
        self.left: Optional['Node'] = None
        self.right: Optional['Node'] = None


root = None
best_move = None
lock = threading.Lock()
start_time = 0
time_limit = 0.3


def calcBestMove(gs):
    global root, best_move, start_time
    print("In calcBestMove")
    start_time = time.time()

    root = Node(gs)
    #print("Root length:", countNodes(root))
    nextNode = queue.Queue()
    nextNode.put(root)
    own_move = True

    while not nextNode.empty():
        if time.time() - start_time > time_limit:
            break

        current_node = nextNode.get()

        if current_node.depth % 2 == 0:
            own_move = True
        else:
            own_move = False

        possible_moves = getSafeMoves(current_node.gamestate, own_move)
        #???
        if not possible_moves:
            current_node.utility = 0

        for move in possible_moves:
            if time.time() - start_time > time_limit:
                break
            state = deepcopy(current_node.gamestate)
            new_state = doMove(state, move, own_move)
            child = Node(new_state)
            child.depth = current_node.depth + 1
            print("Child depth:", child.depth)
            child.utility = evaluatePosition.getEvaluation(new_state)
            setattr(current_node, move, child)
            nextNode.put(child)

    with lock:
        best_move = chooseBestMove()


def getBestMove():
    print("In getBestMove")
    global best_move
    with lock:
        return best_move if best_move else "up"


def chooseBestMove():
    print("In chooseBestMove")
    #print("Number of nodes:", countNodes(root))
    if not root:
        print("No root found")
        return "up"

    best = None
    best_val = float('-inf')
    for move in ["up", "down", "left", "right"]:
        child = getattr(root, move)
        if child:
            value = minmax(child, 1, False)
            print("Value:", value)
            if value > best_val:
                best_val = value
                print("Best value:", best_val)
                best = move
    print("Best move is:", best)
    return best


def countNodes(node):
    if node is None:
        return 0
    return (1  # aktueller Knoten
            + countNodes(node.up) + countNodes(node.down) +
            countNodes(node.left) + countNodes(node.right))


def minmax(node, depth, isMaximizing):
    if not any([node.up, node.down, node.left, node.right]):
        return node.utility

    if isMaximizing:
        best_value = float('-inf')
        for child in [node.up, node.down, node.left, node.right]:
            if child:
                value = minmax(child, depth + 1, False)
                best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for child in [node.up, node.down, node.left, node.right]:
            if child:
                value = minmax(child, depth + 1, True)
                best_value = min(best_value, value)
        return best_value


def doMove(game_state, move, is_own_move):
    new_game_state = deepcopy(game_state)
    if is_own_move:
        head = new_game_state.own_body[0]
    else:
        head = new_game_state.opp_body[0]
    new_head = {}

    if move == "up":
        new_head["x"] = head["x"]
        new_head["y"] = head["y"] + 1
    elif move == "down":
        new_head["x"] = head["x"]
        new_head["y"] = head["y"] - 1
    elif move == "left":
        new_head["x"] = head["x"] - 1
        new_head["y"] = head["y"]
    else:
        new_head["x"] = head["x"] + 1
        new_head["y"] = head["y"]

    if is_own_move:
        new_game_state.own_body.insert(0, new_head)
    else:
        new_game_state.opp_body.insert(0, new_head)
    if new_head in new_game_state.food:
        new_game_state.food.remove(new_head)
        if is_own_move:
            new_game_state.own_health = 100
        else:
            new_game_state.opp_health = 100
    else:
        if is_own_move:
            new_game_state.own_body.pop()
            new_game_state.own_health -= 1
        else:
            new_game_state.opp_body.pop()
            new_game_state.opp_health -= 1

    return new_game_state


def getSafeMoves(game_state, is_own_move):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    if is_own_move:
        snake = game_state.own_body
        opponent_body = game_state.opp_body
    else:
        snake = game_state.opp_body
        opponent_body = game_state.own_body

    # Rule out backwards movement
    my_head = snake[0]
    my_neck = snake[1]

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    # Prevention from moving out of bounds
    board_width = 11
    board_height = 11
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # Prevention from colliding with itself
    my_body = snake
    for bodypart in my_body:
        if my_head["x"] + 1 == bodypart["x"] and my_head["y"] == bodypart["y"]:
            is_move_safe["right"] = False
        if my_head["x"] - 1 == bodypart["x"] and my_head["y"] == bodypart["y"]:
            is_move_safe["left"] = False
        if my_head["y"] + 1 == bodypart["y"] and my_head["x"] == bodypart["x"]:
            is_move_safe["up"] = False
        if my_head["y"] - 1 == bodypart["y"] and my_head["x"] == bodypart["x"]:
            is_move_safe["down"] = False

    # Prevention from colliding with other Battlesnakes
    if game_state.opp_body != my_body:
        opponent_body = game_state.opp_body
    else:
        opponent_body = game_state.own_body
    for bodypart in opponent_body:
        if my_head["x"] + 1 == bodypart["x"] and my_head["y"] == bodypart["y"]:
            is_move_safe["right"] = False
        if my_head["x"] - 1 == bodypart["x"] and my_head["y"] == bodypart["y"]:
            is_move_safe["left"] = False
        if my_head["y"] + 1 == bodypart["y"] and my_head["x"] == bodypart["x"]:
            is_move_safe["up"] = False
        if my_head["y"] - 1 == bodypart["y"] and my_head["x"] == bodypart["x"]:
            is_move_safe["down"] = False

    # Return safe moves
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    return safe_moves
