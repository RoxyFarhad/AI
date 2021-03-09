"""
COMS W4701 Artificial Intelligence - Programming Homework 6

A Bayes net implementation with sampling algorithms

@author: raf2192
"""

import numpy as np
import random

class Node(object):
    def __init__(self, name, parents, probs):
        self.name = name
        self.parents = parents
        self.probs = probs

    def __str__(self):
        return self.name

    # Returns probability distribution of node conditioned on parents.
    # If assignment does not contain all of node.parents, return [0, 0].
    def prob_given_parents(self, assignment):
        parent_values = []
        for parent in self.parents:
            parent_values.append(assignment[parent.name])
        if tuple(parent_values) in self.probs:
            prob = self.probs[tuple(parent_values)]
            return [prob, 1-prob]
        return [0, 0]


class BayesNet(object):
    def __init__(self, nodes):
        self.nodes = nodes

    """YOUR CODE STARTS HERE"""


    # Returns a sample {node.name: value} computed using rejection sampling.
    # If sampled variables are not consistent with evidence, return None instead.
    def rejection_sample(self, evidence):

        sample = {}

        for node in self.nodes:
            prob = node.prob_given_parents(sample)
            x = np.random.choice([True, False], 1, p=prob)
            sample[node.name] = x[0]

        if(len(evidence) == 0):
            return sample
        
        for key in evidence.keys():
            if key in sample:
                if sample[key] != evidence[key]:
                    return None

        return sample

    # Returns a sample {node.name: value} and weight computed using likelihood weighting.
    def weighted_sample(self, evidence):
        sample = {}
        weight = 1.0

        for node in self.nodes:
            if node.name not in evidence:
                prob = node.prob_given_parents(sample)
                x = np.random.choice([True, False], 1, p=prob)
                sample[node.name] = x[0]
            else:
                sample[node.name] = evidence[node.name]
                node_probs = node.prob_given_parents(sample)
                if(sample[node.name] == True):
                    weight = weight * node_probs[0]
                else:
                    weight = weight * node_probs[1]

        return sample, weight


    # Returns a sample {node.name: value} computed using Gibbs sampling.
    # Returned sample should be identical to given sample, except value of node is resampled.
    def Gibbs_sample(self, node, sample):
        child_nodes = []
        parents_true = {}
        parents_false = {}
        node_probs = node.prob_given_parents(sample)
        true_value = node_probs[0]
        false_value = node_probs[1]

        for n in self.nodes:
            if node in n.parents:
                child_nodes.insert(0, n) # means that the order is kept

        for child in child_nodes:
            other_parents = {} #then have to find all other parents 
            for parent in child.parents:
                if parent != node: # want to exclude the value of parent from the node because we need to call it twice // once for true and once for false
                    parents_true[parent.name] = sample[parent.name]
                    parents_false[parent.name] = sample[parent.name]
                else:
                    parents_true[parent.name] = True
                    parents_false[parent.name] = False

            child_prob_parent_true = child.prob_given_parents(parents_true)  ## child_prob_parent_true[0] means prob of seeing Child = true when parent is true
            child_prob_parent_false = child.prob_given_parents(parents_false) ## this is if parent is equal to False
            
            if child.name in sample.keys() and sample[child.name] == True:
                #need to keep two trackers pos, neg to multiply the value of sample by the two values of node being sampled on
                true_value = true_value * child_prob_parent_true[0] 
                false_value = false_value * child_prob_parent_false[0]
            elif child.name in sample.keys() and sample[child.name] == False:
                # if child is false then the second value from either val has to be multiplied by the value so far
                true_value = true_value * child_prob_parent_true[1]
                false_value = false_value * child_prob_parent_false[1]
            
            # now need to normalise values 
        true_value = true_value/(true_value + false_value)
        false_value = 1 - true_value

        x = np.random.choice([True, False], 1, p=(true_value, false_value))
        sample[node.name] = x[0]
        
        return sample


    """YOUR CODE STOPS HERE"""

    def infer(self, query, evidence, N, method):
        count = 0.0
        effective = 0.0
        weight = 1
        index = 0

        # initialize a random sample for Gibbs sampling
        if method == 'Gibbs':
            sample = {}
            nonevidence = []
            for node in self.nodes:
                if node.name in evidence:
                    sample[node.name] = evidence[node.name]
                else:
                    sample[node.name] = np.random.choice([True, False])
                    nonevidence.append(node)

        for i in range(N):
            if method == 'rejection':
                sample = self.rejection_sample(evidence)
                if sample is None:
                    continue
            elif method == 'likelihood':
                sample, weight = self.weighted_sample(evidence)
            elif method == 'Gibbs':
                node = nonevidence[index]
                sample = self.Gibbs_sample(node, sample)
                index = (index + 1) % len(nonevidence)
            effective += weight
            if sample[query]: count += weight

        return count/effective, effective