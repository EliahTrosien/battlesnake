import heuristics


def getEvaluation(game_state):
    healthHeuristic = heuristics.OwnHealth()
    spaceHeuristic = heuristics.SpaceSimple()
    distanceHeuristic = heuristics.DistanceOfHeads()
    headAreaHeuristic = heuristics.AreaAroundHead()
    return (0.2 * healthHeuristic.normalizedHeuristic(game_state) +
            0.3 * spaceHeuristic.normalizedHeuristic(game_state) +
            0.3 * distanceHeuristic.normalizedHeuristic(game_state) + 
            0.2 * headAreaHeuristic.normalizedHeuristic(game_state))
