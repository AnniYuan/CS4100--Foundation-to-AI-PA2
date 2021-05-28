# multiAgents.py
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = currentGameState.getFood()#successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        foods = newFood.asList()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "*** YOUR CODE HERE ***"
        without_fd = int(successorGameState.getScore())
        fdis = 0
        gdis = 0
        if len(foods) >0:
            fdis = min([int(manhattanDistance(f,newPos)) for f in foods])
        if len(newGhostStates) >0:
            gdis = min([int(manhattanDistance(ghostState.getPosition(),newPos))for ghostState in newGhostStates])
        if gdis > 10:
            gdis = 10
        return without_fd - fdis + gdis


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    # return the max-value of the index if depth ==0, otherwise return state value
    def max_value(self, gameState,d):
        maxScore = -999999
        chosen_pacmanIndex=0
        if gameState.isWin() or gameState.isLose() or d == self.depth:
            return self.evaluationFunction(gameState)

        pacman_legal_actions = gameState.getLegalActions(0)
        p_successor = [gameState.generateSuccessor(0, action) for action in pacman_legal_actions]
        pacman_evaluations = [self.min_value(s,d,1) for s in p_successor]
        if len(pacman_legal_actions) > 0:
            maxScore = max(pacman_evaluations)
            best_pacman_Indices = [index for index in range(len(pacman_evaluations)) if
                                   pacman_evaluations[index] == maxScore]
            chosen_pacmanIndex = random.choice(best_pacman_Indices)

        if d ==0:
            return chosen_pacmanIndex
        return maxScore

    #call min_value on each ghost
    def min_value(self, gameState,d,index):
        minScore = 999999
        if gameState.isWin() or gameState.isLose() or d == self.depth:
            return self.evaluationFunction(gameState)

        legal_actions = gameState.getLegalActions(index)
        for action in legal_actions:
            s = gameState.generateSuccessor(index, action)
            if index == gameState.getNumAgents() -1:
                minScore = min(self.max_value(s, d + 1),minScore)
            else: minScore = min(self.min_value(s,d,index+1),minScore)

        return minScore

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        pacman_legal_actions = gameState.getLegalActions(0)
        max = self.max_value(gameState,0)
        return pacman_legal_actions[max]


        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def max_value(self, gameState, d):
        maxScore = -99999
        pacman_legal_actions = gameState.getLegalActions(0)
        p_successor = [gameState.generateSuccessor(0, action) for action in pacman_legal_actions]
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        pacman_evaluations = [self.uniform_value(s, d, 1) for s in p_successor]

        if len(pacman_legal_actions) > 0:
            maxScore = max(pacman_evaluations)
            best_pacman_Indices = [index for index in range(len(pacman_evaluations)) if
                                   pacman_evaluations[index] == maxScore]
            chosen_pacmanIndex = random.choice(best_pacman_Indices)

        if d == 0:
            return chosen_pacmanIndex
        return maxScore


    def uniform_value(self, gameState,d,agentindex):
        legal_actions = gameState.getLegalActions(agentindex)
        sucessors = [gameState.generateSuccessor(agentindex, action) for action in legal_actions]
        number_of_sucessors = len(sucessors)
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if d == (self.depth-1) and agentindex == gameState.getNumAgents()-1:
            value = sum([self.evaluationFunction(s) for s in sucessors])/number_of_sucessors
            return value
        if agentindex == gameState.getNumAgents()-1:
            value = sum([self.max_value(s,d+1) for s in sucessors]) / number_of_sucessors
            return value
        else:
            value = sum([self.uniform_value(s,d,agentindex+1) for s in sucessors]) / number_of_sucessors
            return value


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman_legal_actions = gameState.getLegalActions(0)
        max = self.max_value(gameState, 0)
        return pacman_legal_actions[max]
        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = currentGameState.getFood()  # successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    foods = newFood.asList()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    without_fd = int(successorGameState.getScore())
    fdis = 0
    gdis = 0
    if len(foods) > 0:
        fdis = min([int(manhattanDistance(f, newPos)) for f in foods])
    if len(newGhostStates) > 0:
        gdis = min([int(manhattanDistance(ghostState.getPosition(), newPos)) for ghostState in newGhostStates])
    if gdis > 10:
        gdis = 5
    return without_fd - fdis + gdis

# Abbreviation
better = betterEvaluationFunction
