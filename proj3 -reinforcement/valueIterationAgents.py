# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for x in range(0, self.iterations):
          #create a copy so we dont calculate in the same step incorrectly
          boardValues = self.values.copy()
          for states in self.mdp.getStates():

            if self.mdp.isTerminal(states):
              continue
            else:

              maxValue = -999999

              for possibleActions in self.mdp.getPossibleActions(states):

                value = 0

                for nextState, prob in self.mdp.getTransitionStatesAndProbs(states, possibleActions):

                  # Q* [Q VALUE]: (s,a) = T(s,a,s') * [(R(s,a,s') + (Discount * V*(s')]
                  # use original self.value to update calculations, then make self.value the copy
                  value += prob * (self.mdp.getReward(states, possibleActions, nextState) + (self.discount*self.values[nextState]))

                # V*(s) = max(Q*(s,a))
                maxValue = max(value, maxValue)

              # Then, assign V*(s) to board
              boardValues[states] = maxValue

          self.values = boardValues

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """ 
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        # Q* [Q VALUE]: (s,a) = T(s,a,s') * [(R(s,a,s') + (Discount * V*(s') ]

        QValue = 0

        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state,action):
          QValue += prob * (self.mdp.getReward(state,action,nextState) + (self.discount*self.values[nextState]))

        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        tempValue = -999999
        bestAction = None

        for possibleActions in self.mdp.getPossibleActions(state):
          if self.mdp.isTerminal(state):
            return None
          else:
            QValue = self.computeQValueFromValues(state, possibleActions)
            if QValue >= tempValue:
              tempValue = QValue
              bestAction = possibleActions

        return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        for x in range(0, self.iterations):
          #create a copy so we dont calculate in the same step incorrectly
          boardValues = self.values.copy()
          listStates = self.mdp.getStates()
          i = x % len(listStates)
          states = listStates[i]

          if self.mdp.isTerminal(states):
            continue
          else:

            maxValue = -999999

            for possibleActions in self.mdp.getPossibleActions(states):

              value = 0

              for nextState, prob in self.mdp.getTransitionStatesAndProbs(states, possibleActions):

                # Q* [Q VALUE]: (s,a) = T(s,a,s') * [(R(s,a,s') + (Discount * V*(s')]
                # use original self.value to update calculations, then make self.value the copy
                value += prob * (self.mdp.getReward(states, possibleActions, nextState) + (self.discount*self.values[nextState]))

              # V*(s) = max(Q*(s,a))
              maxValue = max(value, maxValue)

            # Then, assign V*(s) to board
            boardValues[states] = maxValue

          self.values = boardValues

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)


    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        #returns the highest Q Value across all possible actions from s
        def highestQAction(state):
          return max(self.getQValue(state, possibleActions) for possibleActions in self.mdp.getPossibleActions(state))

        #compute predecessors of a state s.
        predecessors = {}

        for state in self.mdp.getStates():
          for action in self.mdp.getPossibleActions(state):
            for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
              if nextState in predecessors:
                predecessors[nextState].add(state) #if key is already in our dictionary, add previous states to set
              else:
                predecessors[nextState] = set([state]) #else, create a new key 


        #initialize an empty priority queue
        priorityStatesQueue = util.PriorityQueue()


        #STEP 1
        for states in self.mdp.getStates():
          if not self.mdp.isTerminal(states): #ignore terminal states 
            diff = abs(self.values[states] - highestQAction(states))
            priorityStatesQueue.update(states, -diff)


        #STEP 2
        for x in range(0, self.iterations):
          if priorityStatesQueue.isEmpty():
            return

          poppedState = priorityStatesQueue.pop()

          if not self.mdp.isTerminal(poppedState):#Update s's value (if it is not a terminal state) in self.values.
            self.values[poppedState] = highestQAction(poppedState) #get the highest Q action of the poppedState

          for pred in predecessors[poppedState]:
            diff = abs(self.values[pred] - highestQAction(pred))

            if diff > self.theta:
              priorityStatesQueue.update(pred, -diff)


            