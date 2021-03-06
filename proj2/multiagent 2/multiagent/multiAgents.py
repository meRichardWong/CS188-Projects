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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        # print legalMoves
        # print scores
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
        The code below extracts some useful information from the state, like 
        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.

        1) the remaining food (newFood) and 

        2) Pacman position after moving (newPos).

        3 )newScaredTimes holds the number of moves that each ghost will remain
          scared because of Pacman having eaten a power pellet.


        """

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        distanceToClosestGhost = 0
        distanceToClosestFood = 0
        distanceToClosestCapsule = 0
        foodWeight = 0
        ghostWeight = 0

        # foodList is a grid, we must turn it into a List
        foodList = newFood.asList()
        foodDistances = [manhattanDistance(newPos, foodCoord) for foodCoord in foodList]

        capsuleList = successorGameState.getCapsules()
        capsuleDistances = [manhattanDistance(newPos, capsuleCoord) for capsuleCoord in capsuleList]

        if foodDistances:
          distanceToClosestFood = min(foodDistances)

        if capsuleDistances:
          distanceToClosestCapsule = min(capsuleDistances)

        #newGhostStates is already a list, so we don't need to run asList() on this
        ghostDistances = [manhattanDistance(newPos, ghostCoord.getPosition()) for ghostCoord in newGhostStates]
        
        if ghostDistances:
          distanceToClosestGhost = min(ghostDistances)

        if distanceToClosestGhost < 2:
          return -100

        capsuleWeight = 0
        if distanceToClosestCapsule > 0:
          capsuleWeight = 1.0/distanceToClosestCapsule

        foodWeight = 0
        if distanceToClosestFood > 0:
          foodWeight = 1.0/distanceToClosestFood

        ghostWeight = 0
        if distanceToClosestGhost > 0:
          ghostWeight = 1.0/distanceToClosestGhost

        newfoodList = newFood.asList()
        oldfoodList = currentGameState.getFood().asList()

        if len(newfoodList) < len(oldfoodList) or successorGameState.getScore() > currentGameState.getScore():
          return 75

        val = foodWeight - ghostWeight + capsuleWeight

        for times in newScaredTimes:
          if times > 0:
            val = foodWeight + ghostWeight

        return val

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

      best_Score = -9999999
      best_Action = Directions.STOP #initialize
      gameStateLegalActions = gameState.getLegalActions()

      for legalActions in gameStateLegalActions:
        gameStateSuccessorState = gameState.generateSuccessor(0, legalActions) # changed

        tempVal = best_Score
        best_Score = max(best_Score, self.min_Play(gameStateSuccessorState, self.depth, 1)) #AA

        if best_Score > tempVal:
          best_Action = legalActions #change actions to legalActions cleanup

      return best_Action

    def max_Play(self, gameState, depth):

      best_Score = -9999999
      pacmanLegalActions = gameState.getLegalActions(0)

      #if the game is over, return score 
      if gameState.isWin() or gameState.isLose() or depth == 0: #how do I know when maximum depth is reached?
        return self.evaluationFunction(gameState)

      for legalActions in pacmanLegalActions:
        pacmanSuccessorState = gameState.generateSuccessor(0, legalActions) #changed

        best_Score = max(best_Score, self.min_Play(pacmanSuccessorState, depth, 1))

      return best_Score

    def min_Play(self, gameState, depth, ghostIndex):

      best_Score = 9999999
      ghostLegalActions = gameState.getLegalActions(ghostIndex)
      bottomLevel = gameState.getNumAgents() - 1

      #if the game is over, return score 
      if gameState.isWin() or gameState.isLose() or depth == 0: #how do I know when maximum depth is reached?
        return self.evaluationFunction(gameState)

      for legalActions in ghostLegalActions:

        ghostSuccessorState = gameState.generateSuccessor(ghostIndex, legalActions)

        if ghostIndex == bottomLevel:
          best_Score = min(best_Score, self.max_Play(ghostSuccessorState, depth - 1))
        else:
          best_Score = min(best_Score, self.min_Play(ghostSuccessorState, depth, ghostIndex + 1))

      return best_Score



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
        Returns the minimax action using self.depth and self.evaluationFunction
      """
      
      best_Score = -9999999
      alpha = -9999999
      beta = 999999
      best_Action = Directions.STOP

      gameStateLegalActions = gameState.getLegalActions()

      for legalActions in gameStateLegalActions:

        gameStateSuccessorState = gameState.generateSuccessor(0, legalActions)

        tempVal = best_Score
        best_Score = max(best_Score, self.min_Play(gameStateSuccessorState, alpha, beta, self.depth, 1)) #changed

        if best_Score > tempVal:
          best_Action = legalActions
        else: 
          best_Score = tempVal
        # if best_Score > beta:
        #   return best_Action

        alpha = max(best_Score, alpha)

      return best_Action

    def max_Play(self, gameState, alpha, beta, depth):

      best_Score = -9999999

      gameStateLegalActions = gameState.getLegalActions()

      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      for legalActions in gameStateLegalActions:
        gameStateSuccessorState = gameState.generateSuccessor(0, legalActions)
        best_Score = max(best_Score, self.min_Play(gameStateSuccessorState, alpha, beta, depth, 1))

        if best_Score > beta:
          return best_Score

        alpha = max(best_Score, alpha)

      return best_Score

    def min_Play(self, gameState, alpha, beta, depth, ghostIndex):

      best_Score = 999999
      ghostLegalActions = gameState.getLegalActions(ghostIndex)
      bottomLevel = gameState.getNumAgents() - 1 


      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      for legalActions in ghostLegalActions:

        gameStateSuccessorState = gameState.generateSuccessor(ghostIndex, legalActions)

        if ghostIndex == bottomLevel:
          best_Score = min(best_Score, self.max_Play(gameStateSuccessorState, alpha, beta, depth - 1))

        else:
          best_Score = min(best_Score, self.min_Play(gameStateSuccessorState, alpha, beta, depth, ghostIndex + 1))

        if best_Score < alpha:
          return best_Score

        beta = min(best_Score, beta)

      return best_Score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):


      """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
      """
      #util.raiseNotDefined()

      return self.max_Play(gameState, 1)

    def max_Play(self, gameState, depth): 

      best_Score = 0
      best_Action = Directions.STOP
      pacmanLegalActions = gameState.getLegalActions(0)

      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      for legalActions in pacmanLegalActions:
        gameStateSuccessorState = gameState.generateSuccessor(0, legalActions)
        expectedMove = self.expAgent(gameStateSuccessorState, depth, self.depth, 1)

        if expectedMove > best_Score:
          best_Action = legalActions
          best_Score = expectedMove

      if depth > 1: # reached the last level
        return best_Score

      return best_Action

    def expAgent(self, gameState, depth, selfDepth, ghostIndex): #expected agent

      best_Score = 0
      ghostLegalActions = gameState.getLegalActions(ghostIndex)
      bottomLevel = gameState.getNumAgents() - 1 

      if gameState.isWin() or gameState.isLose() or depth == 0:
        return self.evaluationFunction(gameState)

      for legalActions in ghostLegalActions:
        ghostSuccessorState = gameState.generateSuccessor(ghostIndex, legalActions)

        if ghostIndex != bottomLevel:
          best_Score += self.expAgent(ghostSuccessorState, depth, selfDepth, ghostIndex + 1)

        else: 
          if depth == selfDepth: 
            best_Score += self.evaluationFunction(ghostSuccessorState)
          else:
            best_Score += self.max_Play(ghostSuccessorState, depth + 1)

      return best_Score/len(ghostLegalActions)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      Prioritize the pellet.

      Get food as long as food exists on the board

      Keep AWAY from the ghosts if they are not scared, otherwise, 
      go after the ghosts after eating the pellet. Pacman is highly rewarded
      for keeping away and going after ghost to incentivize a higher score.
    """

    #Pacman
    currPacManPosition = currentGameState.getPacmanPosition()

    #Ghosts
    currGhostStates = currentGameState.getGhostStates()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    #POWER CAPSULES
    gameStateCapsules = currentGameState.getCapsules()

    #Game information
    foodList = currentGameState.getFood().asList()

    # our better evaluation value 
    score = 0.0

    if len(gameStateCapsules) > 0:
      score += (1.0/len(gameStateCapsules)) * 50.0

    if len(foodList) > 0:
      score += 1.0/len(foodList) * 500.0
    for food in foodList:
      score += 250.0/util.manhattanDistance(currPacManPosition, food)

    
    for ghost in newGhostStates:
      distanceToClosestGhost = util.manhattanDistance(currPacManPosition, ghost.getPosition())

      if newScaredTimes > distanceToClosestGhost:
        score += 5000.0
      elif newScaredTimes < distanceToClosestGhost:
        score -= 2500.0
      else: 
        score += (1000.0/ (1.0/distanceToClosestGhost))

    score += 500.0*currentGameState.getScore()

    return score

# Abbreviation
better = betterEvaluationFunction

