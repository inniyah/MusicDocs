#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See: https://github.com/adeveloperdiary/HiddenMarkovModel
# See: http://www.adeveloperdiary.com/data-science/machine-learning/introduction-to-hidden-markov-model/

import numpy as np

# Hidden Markov Model (θ) has with following parameters :
# 
# S = Set of M Hidden States
# A = Transaction Probability Matrix (aij)
# V = Sequence of T observations (vt)
# B = Emission Probability Matrix (Also known as Observation Likelihood) (bjk)
# π = Initial Probability Distribution

# Evaluation Problem: Given the model (θ), we want to determine the probability that
# a particular sequence of visible states/symbol (V) that was generated from the model (θ).

def forward(V, a, b, initial_distribution):
    # αj(0) = πj·bjk
    alpha = np.zeros((V.shape[0], a.shape[0]))
    alpha[0, :] = initial_distribution * b[:, V[0]]

    # αj(t+1) = bjkv(t+1)·∑i=1..M, aij·αi(t)
    for t in range(1, V.shape[0]):
        for j in range(a.shape[0]):
            # Matrix Computation Steps
            #                  ((1x2) . (1x2))      *     (1)
            #                        (1)            *     (1)
            alpha[t, j] = alpha[t - 1].dot(a[:, j]) * b[j, V[t]]

    return alpha

# Backward Algorithm is the time-reversed version of the Forward Algorithm. In Backward Algorithm
# we need to find the probability that the machine will be in hidden state si at time step t
# and will generate the remaining part of the sequence of the visible symbol V.

def backward(V, a, b):
    beta = np.zeros((V.shape[0], a.shape[0]))

    # setting beta(T) = 1
    beta[V.shape[0] - 1] = np.ones((a.shape[0]))

    # βi(t) = ∑j=0..M, βj(t+1)·bjkv(t+1)·aij

    # Loop in backward way from T-1 to
    # Due to python indexing the actual loop will be T-2 to 0
    for t in range(V.shape[0] - 2, -1, -1):
        for j in range(a.shape[0]):
            beta[t, j] = (beta[t + 1] * b[:, V[t + 1]]).dot(a[j, :])

    return beta


# Learning Problem: Once the high-level structure (Number of Hidden & Visible States) of
# the model is defined, we want to estimate the Transition (a) & Emission (b) Probabilities
# using the training sequences. 

def baum_welch(V, a, b, initial_distribution, n_iter=100):
    M = a.shape[0]
    T = len(V)

    for n in range(n_iter):
        alpha = forward(V, a, b, initial_distribution)
        beta = backward(V, a, b)

        xi = np.zeros((M, M, T - 1))
        for t in range(T - 1):
            denominator = np.dot(np.dot(alpha[t, :].T, a) * b[:, V[t + 1]].T, beta[t + 1, :])
            for i in range(M):
                numerator = alpha[t, i] * a[i, :] * b[:, V[t + 1]].T * beta[t + 1, :].T
                xi[i, :, t] = numerator / denominator

        gamma = np.sum(xi, axis=1)
        a = np.sum(xi, 2) / np.sum(gamma, axis=1).reshape((-1, 1))

        # Add additional T'th element in gamma
        gamma = np.hstack((gamma, np.sum(xi[:, :, T - 2], axis=0).reshape((-1, 1))))

        K = b.shape[1]
        denominator = np.sum(gamma, axis=1)
        for l in range(K):
            b[:, l] = np.sum(gamma[:, V == l], axis=1)

        b = np.divide(b, denominator.reshape((-1, 1)))

    return (a, b)


# Decoding Problem: Once we have the estimates for Transition (a) & Emission (b) Probabilities,
# we can then use the model (θ) to predict the Hidden States W which generated the Visible Sequence V

def viterbi(V, a, b, initial_distribution):
    T = V.shape[0]
    M = a.shape[0]

    omega = np.zeros((T, M))
    omega[0, :] = np.log(initial_distribution * b[:, V[0]])

    prev = np.zeros((T - 1, M))

    # ωi(t+1) = max(i, ωi(t)·aij·bjkv(t+1))

    # One implementation trick is to use the log scale so that we dont get the underflow error.

    for t in range(1, T):
        for j in range(M):
            # Same as Forward Probability
            probability = omega[t - 1] + np.log(a[:, j]) + np.log(b[j, V[t]])

            # This is our most probable state given previous state at time t (1)
            prev[t - 1, j] = np.argmax(probability)

            # This is the probability of the most probable state (2)
            omega[t, j] = np.max(probability)

    # Path Array
    S = np.zeros(T)

    # Find the most probable last hidden state
    last_state = np.argmax(omega[T - 1, :])

    S[0] = last_state

    backtrack_index = 1
    for i in range(T - 2, -1, -1):
        S[backtrack_index] = prev[i, int(last_state)]
        last_state = prev[i, int(last_state)]
        backtrack_index += 1

    # Flip the path array since we were backtracking
    S = np.flip(S, axis=0)

    return S


def test_forward(V):
    # Transition Probabilities
    a = np.array(((0.54, 0.46), (0.49, 0.51)))

    # Emission Probabilities
    b = np.array(((0.16, 0.26, 0.58), (0.25, 0.28, 0.47)))

    # Equal Probabilities for the initial distribution
    initial_distribution = np.array((0.5, 0.5))

    alpha = forward(V, a, b, initial_distribution)
    print(alpha)


def test_backward(V):
    # Transition Probabilities
    a = np.array(((0.54, 0.46), (0.49, 0.51)))

    # Emission Probabilities
    b = np.array(((0.16, 0.26, 0.58), (0.25, 0.28, 0.47)))

    beta = backward(V, a, b)
    print(beta)


def test_baum_welch(V):
    # Transition Probabilities
    a = np.ones((2, 2))
    a = a / np.sum(a, axis=1)

    # Emission Probabilities
    b = np.array(((1, 3, 5), (2, 4, 6)))
    b = b / np.sum(b, axis=1).reshape((-1, 1))

    # Equal Probabilities for the initial distribution
    initial_distribution = np.array((0.5, 0.5))

    print(baum_welch(V, a, b, initial_distribution, n_iter=100))


def test_viterbi(V):
    # Transition Probabilities
    a = np.ones((2, 2))
    a = a / np.sum(a, axis=1)

    # Emission Probabilities
    b = np.array(((1, 3, 5), (2, 4, 6)))
    b = b / np.sum(b, axis=1).reshape((-1, 1))

    # Equal Probabilities for the initial distribution
    initial_distribution = np.array((0.5, 0.5))

    a, b = baum_welch(V, a, b, initial_distribution, n_iter=100)

    print([['A', 'B'][int(s)] for s in viterbi(V, a, b, initial_distribution)])


def main():
    W = np.array(['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B',
                  'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A',
                  'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
                  'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'B', 'B', 'B', 'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'B',
                  'B', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',
                  'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'A'])

    V = np.array([0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 0, 2, 1, 2, 0, 2, 0, 1, 2, 1, 2, 0, 2,
                  0, 2, 2, 0, 2, 2, 2, 0, 0, 1, 0, 1, 2, 2, 2, 2, 0, 2, 2, 2, 1, 2, 0, 1, 0, 0, 2, 1, 2, 1, 1, 1, 0, 2, 0, 0, 1,
                  1, 2, 0, 1, 2, 0, 1, 0, 2, 1, 0, 0, 2, 0, 1, 0, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2,
                  2, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1, 1, 1, 2, 1, 0, 1, 0, 1, 0, 1, 2, 0, 2, 2, 1, 0, 0, 1, 1, 2, 2, 0, 2, 0,
                  0, 0, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 1, 2, 1, 1, 1, 2, 2,
                  2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 0, 2, 0, 1, 2, 0, 1, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
                  0, 0, 1, 2, 1, 0, 2, 2, 1, 2, 2, 2, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 0, 2, 0, 1,
                  1, 2, 0, 0, 2, 2, 2, 1, 1, 0, 0, 1, 2, 1, 2, 1, 0, 2, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 1, 2, 2, 0, 1, 2, 2, 2, 0,
                  1, 1, 2, 2, 0, 1, 2, 2, 2, 2, 2, 2, 0, 1, 2, 2, 0, 2, 0, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 0, 0, 0, 2, 2, 1,
                  1, 2, 1, 0, 2, 1, 1, 1, 0, 1, 2, 1, 2, 1, 2, 2, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 1, 0, 1, 1, 1, 2, 1, 2, 2, 2,
                  2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 2, 1, 0, 2, 2, 0, 2, 2, 0, 2, 2, 2, 2, 0, 2, 2, 2, 1,
                  2, 0, 2, 1, 2, 2, 2, 1, 2, 2, 2, 0, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 0, 2, 2, 1, 2, 2, 2, 2, 1, 2, 0,
                  2, 1, 2, 2, 0, 1, 0, 1, 2, 1, 0, 2, 2, 2, 1, 0, 1, 0, 2, 1, 2, 2, 2, 0, 2, 1, 2, 2, 0, 1, 2, 0, 0, 1, 0, 1, 1,
                  1, 2, 1, 0, 1, 2, 1, 2, 2, 0, 0, 0, 2, 1, 1, 2, 2, 1, 2])

    print("\nTest: Forward:")
    test_forward(V)
    print("\nTest: Backward:")
    test_backward(V)
    print("\nTest: Baum Welch:")
    test_baum_welch(V)
    print("\nTest: Viterbi:")
    test_viterbi(V)

if __name__ == '__main__':
    main()
