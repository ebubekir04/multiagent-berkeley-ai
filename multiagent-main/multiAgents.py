# multdepth=None
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
from os import close

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        # Print every variable to see what we are working with:
        # Useful information you can extract from a GameState (pacman.py)
        # successorGameStates print:
        #  %%%%%%%%%%%%%%%%%%%%%%%%%
        # %.               ....   %
        # %          ..  ... G... %
        # %          ..  ...  ... %
        # %       ..       ....   %
        # %    ..   ^..  ...  ... %
        # %         ...  ...  ... %
        # %      ....      ....  o%
        # %%%%%%%%%%%%%%%%%%%%%%%%%

        # newPos print:
        # (x, y)

        # newFood print:
        # FFFFFFFFFFFFFFFFFFFFFFFFF
        # FTFFFFFFFFFFFFFFFTTTTFFFF
        # FFFFFFFFFFFTTFFTTTFFTTTFF
        # FFFFFFFFFFFTTFFTTTFFTTTFF
        # FFFFFFFFTTFFFFFFFTTTTFFFF
        # FFFFFTTFFFFTTFFTTTFFTTTFF
        # FFFFFFFFFFTTTFFTTTFFTTTFF
        # FFFFFFFTTTTFFFFFFTTTTFFFF
        # FFFFFFFFFFFFFFFFFFFFFFFFF

        # newGhostStates print:
        # [<game.AgentState object at 0x10afaddf0>]

        # newScaredTimes print:
        # [<game.AgentState object at 0x10afaddf0>]

        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()  # asList toegevogd
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currFood = currentGameState.getFood().asList()  # extra toegevoegd
        pacmanPositie = currentGameState.getPacmanPosition()  # extra toegevoegd

        score = 0

        # if pacman is in the same position as a ghost, get severely punished
        ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates]
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            if newPos == ghostPos:
                score = float('-inf')
                return score

        # if pacman eats food, it gets rewarded
        if len(newFood) < len(currFood):
            score += 100

        # added this if-statement to avoid a ValueError if the newFood list is empty
        # newPos, currFood ipv currPos en newFood
        if len(currFood) != 0:
            closestFood = min(map(lambda pos: manhattanDistance(pos, newPos), currFood))[1]
        else:
            closestFood = (0, 0)  # dit toevoegen aan verslag, zonder if-else statement krijg je een error

        # if pacman moves closer to the closest food, it gets rewarded
        if manhattanDistance(newPos, closestFood) < manhattanDistance(pacmanPositie, closestFood):
            score += 10
            return score

        # find the closest food position based on pacman's current position
        closestGhost = min(map(lambda pos: manhattanDistance(pos, newPos), ghostPositions))[1]

        # if pacman moves closer to the nearest ghost, it gets slightly punished
        if manhattanDistance(newPos, closestGhost) > manhattanDistance(pacmanPositie, closestGhost):
            score += 5
            return score
        else:
            score -= 5  # ook punishen als die dichter bij een geest komt
            return score

        # in case none of the if-statements get triggered
        # return score

        # ---TRASH CODE---
        # ver van spoken blijven, dicht bij eten blijven
        # weighted sum
        # maak gebruk van pacmanPositie en foodPosities variabelen
        # foodState ligt verder van newPos dan ghostState -> 0 teruggeven en for loop om verder te gaan
        # ghoststate ligt verder van newPos dan foodState -> 1 en verder in for loop gaan
        # for ghostState in newGhostStates:
        #     for food in newFood:
        #         afstandTotFood = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
        #         l = []
        #         afstandTotGhost = abs(ghostState[0] - newPos[0]) + abs(ghostState[1] - newPos[1])
        #         l.append(afstandTotGhost)
        #         if afstandTotFood < min(l):
        #             score += 1
        #         else:
        #             return score
        #
        #     if newFood[x][y]:

        # positionlist = []
        #
        # for ghostPos in ghostPositions:
        #     for food in newFood:
        #         distance = abs(ghostPos[0] - food[0]) + abs(ghostPos[1] - food[1])
        #         positionlist.append(distance)

        # print("Lijst: ", positionlist)
        # print("Score: ", max(positionlist))

        # return min(foodpositions)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        def minimax(gameState, depth, agentIndex):                              # deze functie zal nagaan in welk staat het spel zich bevindt
            if gameState.isWin() or gameState.isLose() or depth == self.depth:  # ga na of de staat van het game een terminal is
                return self.evaluationFunction(gameState), None
            if agentIndex == 0:
                return max_value(gameState, depth)
            else:
                return min_value(gameState, agentIndex, depth)

        def max_value(gameState, depth):
            value = float('-inf')
            best_move = None
            for move in gameState.getLegalActions(0):                                             # deze for loop zal elke mogelijke actie van Pacman doorlopen
                next_value, _ = minimax(gameState.generateSuccessor(0, move), depth,1)  # genereer voor elke actie de volgende staat van het spel in functie van de opvolgende speler
                if next_value > value:
                    value = next_value
                    best_move = move
            return value, best_move

        def min_value(gameState, agentIndex, depth):
            value = float('inf')
            best_move = None
            num_agents = gameState.getNumAgents()
            next_agent = 0 if agentIndex + 1 == num_agents else agentIndex + 1         # doel van de functie is nagaan of volgende speler ghost of pacman is

            for move in gameState.getLegalActions(agentIndex):
                if next_agent == 0:
                    next_value, _ = minimax(gameState.generateSuccessor(agentIndex, move), depth + 1, next_agent)
                else:
                    next_value, _ = minimax(gameState.generateSuccessor(agentIndex, move), depth, next_agent)

                if next_value < value:
                    value = next_value
                    best_move = move
            return value, best_move

        _, start_state = minimax(gameState, 0, 0)   # het spel wordt in het begin op diepte 0 met pacman begonnen
        return start_state


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def minimax(gameState, depth, agentIndex, alfa, beta):  # parameters alfa en beta worden meegegeven
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            if agentIndex == 0:
                return max_value(gameState, depth, alfa, beta)
            else:
                return min_value(gameState, agentIndex, depth, alfa, beta)

        def max_value(gameState, depth, alfa, beta):
            value = float('-inf')
            best_move = None
            for move in gameState.getLegalActions(0):
                next_value, _ = minimax(gameState.generateSuccessor(0, move), depth,1, alfa, beta)
                if next_value > value:
                    value = next_value
                    best_move = move

                alfa = max(alfa, value)                    # doel van alfa is om zijn waarde te verhogen
                if alfa > beta:                            # als alfa groter is dan beta, dan mogen we prunen
                    break
            return value, best_move

        def min_value(gameState, agentIndex, depth, alfa, beta):
            value = float('inf')
            best_move = None
            num_agents = gameState.getNumAgents()
            next_agent = 0 if agentIndex + 1 == num_agents else agentIndex + 1

            for move in gameState.getLegalActions(agentIndex):
                if next_agent == 0:
                    next_value, _ = minimax(gameState.generateSuccessor(agentIndex, move), depth + 1, next_agent, alfa, beta)
                else:
                    next_value, _ = minimax(gameState.generateSuccessor(agentIndex, move), depth, next_agent, alfa, beta)

                if next_value < value:
                    value = next_value
                    best_move = move

                beta = min(beta, value)             #doel van beta is om zijn waarde te verlagen
                if beta < alfa:                     #als beta kleiner is dan alfa, dan mogen we prunen
                    break
            return value, best_move

        _, start_state = minimax(gameState, 0, 0, float('-inf'), float('inf'))
        return start_state


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluationfunction (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # weighted sum nemen, zoals verteld werd in de WPO

    # ghost states
    ghostStates = currentGameState.getGhostStates()

    # scared times
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # positions
    foodPositions = currentGameState.getFood().asList()  # list of all food positions
    pacmanPosition = currentGameState.getPacmanPosition()
    capsulePositions = currentGameState.getCapsules()
    ghostPositions = [ghostState.getPosition() for ghostState in ghostStates]

    # counts
    capsuleCount = len(capsulePositions)
    foodCount = currentGameState.getNumFood()  # amount of food left
    ghostCount = len(ghostPositions)

    # distances
    foodDistances = [manhattanDistance(foodPosition, pacmanPosition) for foodPosition in foodPositions]
    ghostDistances = [manhattanDistance(ghostPosition, pacmanPosition) for ghostPosition in ghostPositions]
    capsuleDistances = [manhattanDistance(pacmanPosition, Capsule) for Capsule in capsulePositions]

    # closest x
    closestFood = min(foodDistances) if len(foodDistances) > 0 else 0
    closestCapsule = min(capsuleDistances) if len(capsuleDistances) > 0 else 0
    closestGhost = min(ghostDistances) if len(ghostDistances) > 0 else 0

    # avoid divisonByZero
    closestGhost += 1
    closestCapsule += 1
    closestFood += 1
    foodCount += 1

    if 0 in scaredTimes:
        return (3 / closestFood) + (-150 / closestGhost) + (2 / closestCapsule) + (-30 * foodCount) + (
                -30 * capsuleCount)
    else:
        return (2 / closestFood) + (30 / closestGhost) + (-30 * foodCount) + (-50 * ghostCount)

    ### TRASH CODE ####
    # extra: als er 1 food pellet over is en de lijst van capsules is niet leeg, dan geef een lage score voor de food en hoge voor de capsule
    # als pacman een capsule heeft gegeten (maw ghost zijn scared) dan moet hij niet meteen voor de andere gaan en enkel focusen om de geest te eten
    # als er geen capsules meer zijn, enkel focusen op geesten vermijden en food pellets pakken
    # (ghostWeight / closestGhost) + (foodWeight / closestFood) + (foodCountWeight * foodCount)
    # game goal: alle food pellets op eten
    # ideale goal: als die dicht is bij capsules, eerst capsules eten, dan geesten, dan terug food pellets

    # hier score initialiseren zodat we die kunnen aanpassen afhankelijk van de situatie
    # maakt geen verschil
    # if pacmanPosition in foodPositions:
    #     score += 100

    # -foodCount -1/closestGhost ==> eet meer food

    # 3 factoren waarmee ik rekening moet houden
    # 1: food
    # 2: power pellets
    # 3: ghosts, al dan niet Scared

    # Trial 1: -closestFood + (-15 * closestGhost) + -closestCapsule + (-10 * foodCount) + currentScore
    # Trial 2: (1 / closestFood) + (-15 * closestGhost) + (1 / closestCapsule) + (-10 * foodCount) + currentScore

    # ik kreeg een error omdat de XDistances leeg kan zijn, dus ik heb een extra if test toegevoegd

    # 1 / ... want hoe dichter bij de food, hoe kleiner de noemer, hoe groter de waarde

    # gebruik van currentScore is niet toegelaten

    # # motiveer pacman om food pellets te eten
    #     if pacmanPosition in foodPositions:
    #         score += 1
    #     else:
    #         score += (-10 / closestFood) + (-2 * foodCount)
    #
    #     # motiveer pacman om capsules te eten, nog meer als een geest dichtbij is
    #     if pacmanPosition in capsulePositions:
    #         score += 1
    #     else:
    #         if closestCapsule < 2 and closestGhost < 4:
    #             score += 2 / closestCapsule
    #         else:
    #             score += 1 / closestCapsule
    #
    #     # motiveer pacman om weg te blijven van geesten, tenzij ze scared zijn
    #     if 0 not in scaredTimes:
    #         score += 1 / closestGhost
    #     else:
    #         score -= 1 / closestGhost
    #
    #     if len(capsulePositions) == 0 and 0 in scaredTimes:
    #         score = -foodCount - 1 / closestGhost
    #         return score


# Abbreviation
better = betterEvaluationFunction
