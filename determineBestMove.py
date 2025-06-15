import random
import evaluatePosition
import threading
import time

def determine(game_state):
    safe_moves = getSafeMoves(game_state)
    best_move = ""
    
    my_snake = game_state["you"]
    op_snake = game_state["board"]["snakes"][0]
    if my_snake == op_snake:
        op_snake = game_state["board"]["snakes"][1]
        
    # create tree with calculated moves
    tree = []
    tree.append((game_state, 0))
    queue = tree[0]
    while True:
        pass
    # do breadth first search with safe moves
    # return best move

def getSafeMoves(game_state):
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # Rule out backwards movement
    my_head = game_state["you"]["head"]
    my_neck = game_state["you"]["body"][1]

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    # Prevention from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # Prevention from colliding with itself
    my_body = game_state['you']['body']
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
    opponents = game_state['board']['snakes']
    for opponent in opponents:
        opponent_body = opponent['body']
        for bodypart in opponent_body:
            if my_head["x"] + 1 == bodypart["x"] and my_head["y"] == bodypart[
                    "y"]:
                is_move_safe["right"] = False
            if my_head["x"] - 1 == bodypart["x"] and my_head["y"] == bodypart[
                    "y"]:
                is_move_safe["left"] = False
            if my_head["y"] + 1 == bodypart["y"] and my_head["x"] == bodypart[
                    "x"]:
                is_move_safe["up"] = False
            if my_head["y"] - 1 == bodypart["y"] and my_head["x"] == bodypart[
                    "x"]:
                is_move_safe["down"] = False

    # be safe from head to head collisions
    dangerdirection = checkHeadCollision(game_state)
    if dangerdirection != "none":
        is_move_safe[f"{dangerdirection}"] = False

    # Return safe moves
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    return safe_moves


def checkHeadCollision(game_state):
    # checks if head to head collision is imminent and returns the direction where the danger is coming from
    my_head = game_state["you"]["head"]
    for opponent in game_state['board']['snakes']:
        if opponent == game_state['you']:
            continue
        if my_head["x"] == opponent["head"]["x"]:
            if my_head["y"] == opponent["head"]["y"] + 2:
                if len(opponent["body"]) + 1 < len(game_state["you"]["body"]):
                    print("Stay on course for elimination!")
                    break
                print("Warning, head to head collision downwards!")
                return "down"
            if my_head["y"] == opponent["head"]["y"] - 2:
                if len(opponent["body"]) + 1 < len(game_state["you"]["body"]):
                    print("Stay on course for elimination!")
                    break
                print("Warning, head to head collision upwards!")
                return "up"
        if my_head["y"] == opponent["head"]["y"]:
            if my_head["x"] == opponent["head"]["x"] + 2:
                if len(opponent["body"]) + 1 < len(game_state["you"]["body"]):
                    print("Stay on course for elimination!")
                    break
                print("Warning, head to head collision to the left!")
                return "left"
            if my_head["x"] == opponent["head"]["x"] - 2:
                if len(opponent["body"]) + 1 < len(game_state["you"]["body"]):
                    print("Stay on course for elimination!")
                    break
                print("Warning, head to head collision to the right!")
                return "right"
        return "none"
