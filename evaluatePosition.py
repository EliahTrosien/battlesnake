import heuristics


def getEvaluation(game_state):
    h1 = heuristics.OwnHealth().normalizedHeuristic(game_state)
    h2 = heuristics.SpaceSimple().normalizedHeuristic(game_state)
    h3 = heuristics.DistanceOfHeads().normalizedHeuristic(game_state)
    h4 = heuristics.AreaAroundHead().normalizedHeuristic(game_state)
    #print(f"Heuristics: health={h1}, space={h2}, distance={h3}, area={h4}")
    return 0.2 * h1 + 0.3 * h2 + 0.3 * h3 + 0.2 * h4
