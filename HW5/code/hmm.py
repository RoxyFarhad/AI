"""
COMS W4701 Artificial Intelligence - Programming Homework 5

A HMM object with forward, Viterbi, and (optionally) smoothing algorithm implementations

@Roxanne Farhad: raf2192
"""

import numpy as np

class HMM(object):
    """
    states: List of state values (e.g., strings, integers, etc.)
    emissions: List of emission values (e.g., strings, integers, etc.)
    initial: Initial state probability distribution (row vector)
    tprob: Transition matrix. tprob[i,j] = Pr(X_t = j | X_{t-1} = i)
    eprob: Emissions matrix. eprob[i,j] = Pr(E_t = j | X_t = i)
    """
    def __init__(self, model):
        self.states = model["states"]
        self.emissions = model["emissions"]
        self.initial = np.array(model["initial"])
        self.tprob = np.array(model["tprob"])
        self.eprob = np.array(model["eprob"])


    """YOUR CODE STARTS HERE"""

    # Forward algorithm for state estimation
    """
    Input: List of observation indices
    Outputs: 2d array, each row is belief distribution P(X_t | e_{1:t})
    """
    def forward(self, observations):

        output = []

        first_obs = self.eprob[:,observations[0]]
        f0 = self.initial * first_obs 
        normalise = sum(f0)
        temp1 = []
        for i in f0:
            temp1.append(i/normalise)
        f1 = np.array(temp1)
        output.append(f1)

        for i in range(1, len(observations)):

            ft_dash = np.dot(output[i - 1], self.tprob)
            ft_dash_ = ft_dash * self.eprob[:,observations[i]]
            normalise = sum(ft_dash_)

            temp = []
            for i in ft_dash_:
                temp.append(i/normalise)
            ft1 = np.array(temp)

            output.append(ft1)


        return np.array(output)

        #return np.empty([len(observations), len(self.states)])


    # Elapse time for most likely sequence (Viterbi)
    """
    Input: Message distribution m_t = max P(x_{1:t-1}, X_t, e_{1:t})
    Outputs: max P(x_{1:t}, X_{t+1}, e_{1:t}), 
             list of most likely prior state indices
    """
    def propagate_joint(self, m):

        output = []
        max_val_in = 0
        max_val_out = 0
        max_point_int = []
        max_point_out = []

        max_point = 0
        max_col = 0
        for i in range(len(m)): 
            if(m[i] > max_point):
                max_point = m[i]
                max_col = i
        max_point_out = [max_col, max_col]

        for i in range(np.size(self.eprob, 0)):

            col = self.tprob[:, i] # column values 

            max_val = max(m * col)    
            output.append(max_val)

        # at the end the list would have all the correct numbers 
        #print(output)
        return np.array(output), max_point_out


    # Viterbi algorithm for state sequence estimation
    """
    Input: List of observation indices
    Outputs: List of most likely sequence of state indices
    """
    def viterbi(self, observations):

        output = []
        pointers = []

        first_obs = self.eprob[:,observations[0]]
        m0 = first_obs * self.initial
        normalise = sum(m0)
        temp1 = []
        for i in m0:
            temp1.append(i/normalise)
        m1 = np.array(temp1)

        output.append(m1)

        for i in range(1, len(observations)):
            m2_dash, pointer = self.propagate_joint(output[i-1])
            pointers.append(pointer)

            m2 = m2_dash * self.eprob[:,observations[i]]
            normalise = sum(m2)
            temp = []
            for i in m2:
                temp.append(i/normalise)
            m2_ = np.array(temp)
            output.append(m2_)

        # for the last m2 there is no values associated with it
        last_val = output[-1]
        max_point = 0
        max_col = 0
        for i in range(len(last_val)): 
            if(last_val[i] > max_point):
                max_point = last_val[i]
                max_col = i
        pointers.append([max_col, max_col])

        send_pointers = []
        for i in pointers:
            send_pointers.append(i[0])

        return send_pointers


    # Backward pass for computing likelihood of future evidence given current state
    """
    Input: List of observations indices
    Output: 2d array, each row is likelihood P(e_{k+1:T} | X_k)
    """
    def backward(self, observations):
        
        output = np.empty([len(observations), len(self.states)])
        base_case = np.ones([len(self.states)])
        output[-1] = base_case

        for i in reversed(range(0, len(observations) - 1)):
            b_k_dash = base_case * self.eprob[:, observations[i+1]]
            b_k = np.dot(b_k_dash, self.tprob.transpose())
            output[i] = b_k
            base_case = b_k

        return np.array(output)


    """YOUR CODE STOPS HERE"""

    def smooth(self, observations):
        forward = self.forward(observations)
        backward = self.backward(observations)
        smoothed = np.multiply(forward, backward)
        return smoothed / np.linalg.norm(smoothed, ord=1, axis=1).reshape(len(observations),1)
