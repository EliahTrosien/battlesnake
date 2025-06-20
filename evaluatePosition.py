import heuristics


def getEvaluation(game_state):
    healthHeuristic = heuristics.OwnHealth()
    spaceHeuristic = heuristics.SpaceSimple()
    distanceHeuristic = heuristics.DistanceOfHeads()
    middleHeuristic = heuristics.ToMiddle()
    movesHeuristic = heuristics.NumberOfMoves()
    return (0.2 * healthHeuristic.normalizedHeuristic(game_state) +
            0.2 * spaceHeuristic.normalizedHeuristic(game_state) +
            0.2 * distanceHeuristic.normalizedHeuristic(game_state) + 
            0.2 * headAreaHeuristic.normalizedHeuristic(game_state) +
            0.2 * headAreaHeuristic.normalizedHeuristic(game_state))
