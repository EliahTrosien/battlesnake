import typing
import determineBestMove

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

  # start timer

  # create thread

  next_move = determineBestMove.calcMove(game_state) # calculate in thread

  # timer over? get result from thread

  print(f"MOVE {game_state['turn']}: {next_move}")
  return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
