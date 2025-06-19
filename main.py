import threading
import typing
import determineBestMove
from typing import List, Tuple


class gameState:
    own_body: List[Tuple[
        int, int]]  # saves the body of own snake, with head being own_body[0]
    own_health: int  # saves the own current health: 0 < own_health <= 100
    opp_body: List[Tuple[
        int,
        int]]  # saves the body of opponents snake, with head being opp_body[0]
    opp_health: int  # saves the opponents current health: 0 < opp_health <= 100
    food: List[Tuple[
        int,
        int]]  # saves all the places where food is (might be sorted in some way, don't know, does not matter)

    def __init__(self, server_response):
        self.own_body = server_response['board']['snakes'][0]['body']
        self.own_health = server_response['board']['snakes'][0]['health']
        self.opp_body = server_response['board']['snakes'][1]['body']
        self.opp_health = server_response['board']['snakes'][1]['health']
        self.food = server_response['board']['food']


def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",
        "color": "#888888",
        "head": "default",
        "tail": "default",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
def move(game_state: typing.Dict) -> typing.Dict:

    best_move = None

    # convert server response to gamestate with less information
    state = gameState(game_state)

    # start calculation in thread
    calc_thread = threading.Thread(target=determineBestMove.calcBestMove,
                                   args=(state, ))
    calc_thread.start()
    # end calculation after 450ms
    calc_thread.join(timeout=0.45)

    # get best move after time is up
    best_move = determineBestMove.getBestMove()

    print(f"MOVE {game_state['turn']}: {best_move}")
    return {"move": best_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
