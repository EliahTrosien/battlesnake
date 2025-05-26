# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["head"]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
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

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
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

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
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

    # check for head to head collisions
    dangerdirection = checkCollision(game_state)
    if dangerdirection != "none":
        is_move_safe[f"{dangerdirection}"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(
            f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    min = board_width + 1
    for food_item in food:
        min_temp = abs(my_head['x'] - food_item['x']) + abs(my_head['y'] -
                                                            food_item['y'])
        if min_temp < min:
            min = min_temp
            food = food_item
    if min == board_width + 1:
        food = food[0]
    food_x = food['x']
    food_y = food['y']
    if my_head["x"] < food_x and is_move_safe["right"]:
        next_move = "right"
    elif my_head["x"] > food_x and is_move_safe["left"]:
        next_move = "left"
    elif my_head["y"] < food_y and is_move_safe["up"]:
        next_move = "up"
    elif my_head["y"] > food_y and is_move_safe["down"]:
        next_move = "down"

    # if enemy head gets too close, get away (or maybe not if it is shorter)

    opponents = game_state['board']['snakes']
    for opponent in opponents:
        if opponent == game_state['you']:
            continue
        opponent_head = opponent['head']
        if abs(my_head["x"] - opponent_head["x"]) < 2 and abs(
                my_head["y"] - opponent_head["y"]) < 2:
            print("Opponent near!")
            if len(opponent["body"]) + 1 < len(game_state["you"]["body"]):
                print("Stay on course for elimination!")
                break  # andere schlange umbringen wenn die pech hat und in uns rein läuft
            votes = {"right": 0, "left": 0, "up": 0, "down": 0}
            if opponent_head["x"] == my_head["x"] + 1:
                votes["left"] = votes["left"] + 1
            if opponent_head["x"] == my_head["x"] - 1:
                votes["right"] = votes["right"] + 1
            if opponent_head["y"] == my_head["y"] + 1:
                votes["down"] = votes["down"] + 1
            if opponent_head["y"] == my_head["y"] - 1:
                votes["up"] = votes["up"] + 1

            max_vote = max(votes.values())

            winners = [
                direction for direction, vote in votes.items()
                if vote == max_vote
            ]
            for winner in winners:
                if winner == "right":
                    if is_move_safe["right"]:
                        next_move = "right"
                elif winner == "left":
                    if is_move_safe["left"]:
                        next_move = "left"
                elif winner == "up":
                    if is_move_safe["up"]:
                        next_move = "up"
                else:
                    if is_move_safe["down"]:
                        next_move = "down"
            print(f"Dodging {next_move}!")

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


def checkCollision(game_state):
    # checks if head to head collision is imminent and returns the direction to dodge
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


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
