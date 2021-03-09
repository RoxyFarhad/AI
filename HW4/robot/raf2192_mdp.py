"""
COMS W4701 Artificial Intelligence - Programming Homework 4

A MDP simulator for a robot vacuum cleaner in a house

@author: YOUR NAME AND UNI
"""

import random
import sys
from Qlearner import Qlearner

class FloorPlan(object):

    def __init__(self, dim, states, model, discount):
        self.width = dim["width"]
        self.height = dim["height"]
        self.goals = states["goals"]
        self.traps = states["traps"]
        self.blocked = states["blocked"]

        self.success_prob = model["success_prob"]
        self.trap_reward = model["trap_reward"]
        self.goal_reward = model["goal_reward"]
        self.living_reward = model["living_reward"]
        self.gamma = discount

        self.actions = ('n', 's', 'e', 'w')
        self.states = set()
        for x in range(self.width):
            for y in range(self.height):
                if (x,y) not in self.goals and (x,y) not in self.traps and (x,y) not in self.blocked:
                    self.states.add((x,y))

    #### Internal functions for running policies ###
    #### You should not need to use any of these functions ###

    def get_possible_actions(self, state):
        """
        Return the common list of actions available at any state
        """
        return self.actions

    def get_transitions(self, state, action):
        """
        Return a list of (successor, probability) pairs that
        can result from taking action from state.
        """
        result = []
        x,y = state
        remain_p = 0.0

        if action=="n":
            success = (x,y-1)
            fail = [(x+1,y), (x-1,y)]
        elif action=="s":
            success =  (x,y+1)
            fail = [(x+1,y), (x-1,y)]
        elif action=="e":
            success = (x+1,y)
            fail= [(x,y-1), (x,y+1)]
        elif action=="w":
            success = (x-1,y)
            fail= [(x,y-1), (x,y+1)]
          
        if success[0] < 0 or success[0] > self.width-1 or \
           success[1] < 0 or success[1] > self.height-1 or \
           success in self.blocked: 
                remain_p += self.success_prob
        else: 
            result.append((success, self.success_prob))
        
        for i,j in fail:
            if i < 0 or i > self.width-1 or \
               j < 0 or j > self.height-1 or \
               (i,j) in self.blocked: 
                    remain_p += (1-self.success_prob)/2
            else: 
                result.append(((i,j), (1-self.success_prob)/2))
           
        if remain_p > 0.0: 
            result.append(((x,y), remain_p))
        return result

    def move(self, state, action):
        """
        Return successor that results from taking action from state.
        """
        transitions = self.get_transitions(state, action)
        new_state = random.choices([i[0] for i in transitions], weights=[i[1] for i in transitions])
        return new_state[0]

    def simple_policy_rollout(self, initial_state, policy):
        """
        Return (Boolean indicating success of trial, total rewards) pair.
        """
        state = initial_state
        rewards = 0
        while True:
            state = self.move(state, policy[state])
            rewards += self.living_reward
            if state in self.goals:
                return True, rewards+self.goal_reward
            if state in self.traps:
                return False, rewards+self.trap_reward

    def transition(self, state, action):
        """
        Returns a successor state and reward for taking action from state.
        Used for testing Q-learning for this object class.
        """
        succ = self.move(state, action)
        reward = self.living_reward
        if succ in self.goals:
            return None, reward + self.goal_reward
        elif succ in self.traps:
            return None, reward + self.trap_reward
        return succ, reward


    #### Utility functions to visualize and test your MDP algorithms ###

    def test_policy(self, initial_state, policy, t=500):
        """
        Following the policy t times, return (success rate, average total rewards).
        """
        numSuccess = 0.0
        totalRewards = 0.0
        for i in range(t):
            result = self.simple_policy_rollout(initial_state, policy)
            if result[0]:
                numSuccess += 1
            totalRewards += result[1]
        return (numSuccess/t, totalRewards/t)

    def get_random_policy(self):
        """
        Generate a random policy.
        """
        policy = {}
        for i in range(self.width):
            for j in range(self.height):
                policy[(i,j)] = random.choice(self.actions)
        return policy

    def gen_rand_set(width, height, size):
        """
        Generate a random set of grid spaces for creating randomized maps.
        """
        mySet = set([])
        while len(mySet) < size:
            mySet.add((random.randint(0, width), random.randint(0, height)))
        return mySet


    def print_map(self, policy=None):
        """
        Print out the floorplan of the house, where * indicates start state,
        G indicates goal states, # indicates blocked states, and T indicates traps.
        If a policy is provided, it will be printed out on the map as well.
        """
        sys.stdout.write(" ")
        for i in range(2*self.width):
            sys.stdout.write("--")
        sys.stdout.write("\n")
        for j in range(self.height):
            sys.stdout.write("|")
            for i in range(self.width):
                if (i, j) in self.goals:
                    sys.stdout.write("G\t")
                elif (i, j) in self.traps:
                    sys.stdout.write("T\t")
                elif (i, j) in self.blocked:
                    sys.stdout.write("#\t")
                else:
                    if policy and (i, j) in policy:
                        a = policy[(i, j)]
                        if a == "n":
                            sys.stdout.write("^")
                        elif a == "s":
                            sys.stdout.write("v")
                        elif a == "e":
                            sys.stdout.write(">")
                        elif a == "w":
                            sys.stdout.write("<")
                        sys.stdout.write("\t")
                    else:
                        sys.stdout.write(".\t")
            sys.stdout.write("|")
            sys.stdout.write("\n")
        sys.stdout.write(" ")
        for i in range(2*self.width):
            sys.stdout.write("--")
        sys.stdout.write("\n")

    def print_values(self, values):
        """
        Given a dictionary {state: value} of values, print them on a grid.
        """
        for j in range(self.height):
            for i in range(self.width):
                if (i, j) in self.traps:
                    value = self.trap_reward
                elif (i, j) in self.goals:
                    value = self.goal_reward
                elif (i, j) in self.blocked:
                    value = 0.0
                else:
                    value = values[(i, j)]
                print("%10.2f" % value, end='')
            print()


    def test_random_policy(self, initial_state):
        rand_policy = self.get_random_policy()
        self.print_map()
        self.print_map(rand_policy)
        print("Success rate and average rewards for a random policy:", self.test_policy(initial_state, rand_policy))

    def test_value_iteration(self, threshold, asynch, initial_state):
        VStar, num_iterations = self.value_iteration(threshold, asynch)
        print("Values from value iteration")
        self.print_values(VStar)
        val_iter_policy = self.extract_policy(VStar)
        self.print_map(val_iter_policy)
        print("Iterations for convergence of value iteration:", num_iterations)
        print("Success rate and average rewards for computed policy:",
              self.test_policy(initial_state, val_iter_policy))

    def test_policy_iteration(self, num_iter_eval, asynch, initial_state):
        initial_policy = {state: 'n' for state in self.states}
        policy_iter_policy, num_iterations = self.policy_iteration(initial_policy, num_iter_eval, asynch)
        self.print_map(policy_iter_policy)
        print("Iterations for convergence of policy iteration:", num_iterations)
        print("Success rate and average rewards for computed policy:",
              self.test_policy(initial_state, policy_iter_policy))

    def test_qlearning(self, parameters, episodes, initial_state):
        Qlearner_obj = Qlearner(self.states, self.get_possible_actions, parameters)
        learned_Q = Qlearner_obj.run_Qlearning(self.get_possible_actions, self.transition, episodes)
        learned_V = self.QValue_to_value(learned_Q)
        learned_policy = self.extract_policy(learned_V)
        self.print_map(learned_policy)
        print("Success rate and average rewards for policy from Q-learning:",
              self.test_policy(initial_state, learned_policy))


    #### Utility computations for dynamic programming ###

    def QValue_to_value(self, Qvalues):
        """
        Given a dictionary {(state, action): q-value} of q-values,
        return a dictionary {state: value} of values.
        """
        values = {}
        for state in self.states:
            values[state] = -float("inf")
            for action in self.actions:
                values[state] = max(values[state], Qvalues[(state, action)])
        return values

    def Qvalue(self, state, action, values):
        """
        Given a dictionary {state: value} of values,
        return the Q-value for the state-action pair.
        """
        Q = 0
        for successor in self.get_transitions(state, action):
            if successor[0] in self.traps:
                VsPrime = self.trap_reward
            elif successor[0] in self.goals:
                VsPrime = self.goal_reward
            else:
                VsPrime = values[successor[0]]
            Q += successor[1] * (self.living_reward + self.gamma * VsPrime)
        return Q


    #### YOUR CODE STARTS HERE ###

    def value_iteration(self, epsilon, asynch=False):
        """
        Return a dictionary {state: value} of values as a result of running
        value iteration until max change is smaller than epsilon*(1-gamma)/gamma.
        Boolean asynch indicates asynchronous vs synchronous implementation.
        Also return number of iterations taken.
        """

        values = {}
        oldvalues = {}
        num_iterations = 0
        con_value = (epsilon*(1 - self.gamma))/(self.gamma)
        delta = float("inf")

        for state in self.states:
            values[state] = 0
            oldvalues[state] = 0

        while(delta > con_value): # loop to check convergence
            delta = float("-inf")
            for state in self.states:
                maxVk = float("-inf")

                curr_val = values[state]

                for action in self.actions:

                    if asynch == True:
                        Vk = self.Qvalue(state, action, values)
                       # print("state: ", state, " action: ", action, " qVal: ", Vk)
                        if Vk > maxVk: 
                            maxVk = Vk

                    else:
                        Vk = self.Qvalue(state, action, oldvalues)
                        if Vk > maxVk: 
                            maxVk = Vk
                values[state] = maxVk

                # now check the delta value (represents the change from old value)

                if abs((maxVk - curr_val)) > delta:
                    delta = abs((maxVk - curr_val))

            if asynch == False: # update the oldvalues for the new time once all value-itereation has been performed
                for state in self.states:
                    oldvalues[state] = values[state]
            max_change = delta

            num_iterations += 1

        return values, num_iterations

    def extract_policy(self, values):
        """
        "state: values"
        Return a dictionary {state: action} of the best policy for the given values.
        """
        policy = {}

        for state in self.states:
            maxVal = float("-inf")
            maxAction = 0
            for action in self.actions:
                qVal = self.Qvalue(state, action, values)
                if(qVal > maxVal):
                    maxVal = qVal
                    maxAction = action
            policy[state] = maxAction

        return policy


    def policy_eval_sweep(self, policy, values, asynch=False):
        """
        Return a dictionary {state: value} of values from one sweep of
        iterative policy evaluation for the current policy and values.
        Boolean asynch indicates asynchronous vs synchronous implementation.
    
        finds the values of the state according to that policy

        """
        oldValues = values

        if asynch == True:
            for state in self.states:
                values[state] = self.Qvalue(state, policy[state], values)
        else:
            for state in self.states:
                value = self.Qvalue(state, policy[state], oldValues)
                values[state] = value

        return values


    def policy_iteration(self, initial_policy, k, asynch=False):
        """
        Return an optimal policy (dictionary {state: action}) from
        running policy iteration starting from initial_policy.
        Implementation should alternate between k sweeps of iterative
        policy evaluation and one policy improvement.
        Boolean asynch indicates asynchronous vs synchronous implementation.
        Also return number of iterations taken.
        """
        policy = initial_policy
        num_iterations = 0
        counter = 0

        values = {}
        new_policy = {}

        for state in policy:
            values[state] = 0
    
        while (new_policy != policy):
            num_iterations += 1
            counter = 0
            new_policy = policy
            while counter < k:
                values = self.policy_eval_sweep(policy, values, asynch)   
                counter += 1
            
            policy = self.extract_policy(values)

        return policy, num_iterations


if __name__ == "__main__":

    # A one-room floor plan
    dim = {"width": 8, "height": 8}
    goals = set([(1,4),(4,7),(7,6)])
    blocked = set([(2,1),(3,1),(3,7),(5,5),(5,6),(5,7),(6,0),(7,0),(7,1)])
    traps = set([(0,7),(1,7),(2,7),(3,3),(3,4),(4,3),(4,4),(5,3),(5,4)])
    special_states = {"goals":goals, "blocked":blocked, "traps":traps}

    #A two-room floor plan
    #dim = {"width": 12, "height": 8}
    #goals = set([(1,4),(4,7),(11,1)])
    #blocked = set([(2,1),(3,1),(3,7),(5,5),(5,6),(5,7),(6,0),(7,0),(7,1),(7,2),(7,3),(7,6),(7,7),(10,5),(10,6),(10,7),(11,5),(11,6),(11,7)])
    #traps = set([(0,7),(1,7),(2,7),(3,3),(3,4),(4,3),(4,4),(5,3),(5,4),(8,0),(9,0),(9,3),(9,4),(10,3),(10,4)])
    #special_states = {"goals":goals, "blocked":blocked, "traps":traps}

    model = {"success_prob":0.8, "living_reward":-0.1, "trap_reward":-10.0, "goal_reward":5.0}
    discount = 0.9
    map = FloorPlan(dim, special_states, model, discount)
    initial_state = (4,2)

    # Rollout a random policy. Run this first to get a feel for the problem.
    #map.test_random_policy(initial_state)
    #print()

    # Run and test value iteration.
    threshold = 0.001
    map.test_value_iteration(threshold, False, initial_state)
    print()

    # Run and test policy iteration.
    num_iter_eval = 1
    map.test_policy_iteration(num_iter_eval, False, initial_state)
    print()

    # Run and test Q-learning.
    parameters = {"alpha":0.1, "epsilon":0.2, "gamma":discount, "Q0":0}
    episodes = 1000
    map.test_qlearning(parameters, episodes, initial_state)