"""
COMS W4701 Artificial Intelligence - Programming Homework 4

A Q-learning agent for a stochastic task environment

@author: YOUR NAME AND UNI
"""

import random
import math
import sys


class Qlearner(object):

    def __init__(self, states, valid_actions, parameters):
        self.alpha = parameters["alpha"]
        self.epsilon = parameters["epsilon"]
        self.gamma = parameters["gamma"]
        self.Q0 = parameters["Q0"]

        self.states = states
        self.Qvalues = {}
        for state in states:
            for action in valid_actions(state):
                self.Qvalues[(state, action)] = parameters["Q0"]

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setDiscount(self, gamma):
        self.gamma = gamma

    def setLearningRate(self, alpha):
        self.alpha = alpha


    def update(self, state, valid_actions, transition):
        """
        Perform one transition from state and update the corresponding Q-value.
        Choose an action using epsilon-greedy and valid_actions(state).
        transition(state, action) returns a (successor, reward) pairing.
        self.Qvalues is updated in place and the successor state is returned.
        """
        #### REPLACE THE FOLLOWING WITH YOUR CODE ###

        # finding the optimal policy:

        new_state = ""
        reward = 0
        optimalAction = ""
        max_q = float('-inf')

        number = random.uniform(0, 1)
        if(number < 0.2):
            for action in valid_actions(state):
                val = self.Qvalues[(state, action)]
                if(val > max_q):
                    max_q = val
                    optimalAction = action

            new_state, reward = transition(state, optimalAction)

        else:
            optimalAction = random.choice(valid_actions(state)) # the optimal action for the current state
            new_state, reward = transition(state, optimalAction) # makes the transition to the new state

        if new_state is None:
            for action in valid_actions(new_state):
                self.Qvalues[(new_state, action)] = 0
            self.Qvalues[(state, optimalAction)] = reward
            return new_state; 

        max_q_2 = float("-inf")
        max_action = ""
        for action in valid_actions(new_state):
            value = self.Qvalues[(new_state, action)]
            if(value > max_q_2):
                max_q_2 = value
                max_action = action

        curr_q = self.Qvalues[(state, optimalAction)]

        sample = reward + self.gamma*(max_q_2)
        new_q = curr_q + self.alpha*(sample-curr_q)

        self.Qvalues[(state, optimalAction)] = new_q
        return new_state


    def run_Qlearning(self, valid_actions, transition, num_episodes):
        """
        Run Q-learning for num_episodes and then returns the set of all Qvalues.
        valid_actions(state) and transition(state, action) are functions passed into update().
        """
        for i in range(num_episodes):
            state = random.choice(tuple(self.states))
            while state is not None:
                state = self.update(state, valid_actions, transition)
        return self.Qvalues
