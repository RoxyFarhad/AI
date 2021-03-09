#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 3

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: Roxanne Farhad @raf2192
"""

import random
import sys
import time
import heapq

# You can use the functions in othello_shared to write your AI 
from othello_shared import get_possible_moves, play_move, compute_utility


############ MINIMAX ###############################

"""
Computes the minimax value of a MAX node
"""
def minimax_max_node(board):

    """

    If the value being tested is a terminal node -> return it 
    then for every possible action i.e, child nodes:
        assign the value v = max(v, min_node(state, action))

    for every child node - play the move and check the score.
    Play move returns the new board - the score becomes the value, 
    and then put the new board into the min function

    1. test  state

        // the max node is always dark - 1 
    
    """
    v = float("-inf")
    moves = get_possible_moves(board, 1)

    if(len(moves) == 0):
        # this means that the dark player can play no moves i.e. no child nodes
        return compute_utility(board)
    else: 
        for move in moves:
            movei = move[0]
            movej = move[1]
            newBoard = play_move(board, 1, movei, movej)
            newV = minimax_min_node(newBoard)
            if(v < newV):
                v = newV
    
    # at the end of this then best move becomes the best option to take 
    # then the move has to be played

    return v


"""
Computes the minimax value of a MIN node
"""
def minimax_min_node(board):

    v = float("inf")
    moves = get_possible_moves(board, 2)

    if(len(moves) == 0):
        return compute_utility(board)
    else:
        for move in moves:
            movei = move[0]
            movej = move[1]
            newBoard = play_move(board, 2, movei, movej)
            newV = minimax_max_node(newBoard)
            if(v > newV):
                v = newV

    return v

"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""
def select_move_minimax(board, color):

    if(color == 1):
        v = float("-inf")
        moves = get_possible_moves(board, 1)
        for move in moves:
            new_board = play_move(board, 1, move[0], move[1])
            newV = minimax_min_node(new_board)
            if(newV > v):
                v = newV
                bestMove = move
    else:
        v = float("inf")
        moves = get_possible_moves(board, 2)
        for move in moves:
            newBoard = play_move(board, 2, move[0], move[1])
            newV = minimax_max_node(newBoard)
            if(v > newV):
                v = newV
                bestMove = move
 
    return bestMove
############ ALPHA-BETA PRUNING #####################

"""
Computes the minimax value of a MAX node with alpha-beta pruning
"""
def alphabeta_max_node(board, alpha, beta, level=1, limit=float("inf")):
    
    v = float("-inf")
    a = alpha
    b = beta

    heap = []
    moveDict = {}

    moves = get_possible_moves(board, 1)

    if(len(moves) == 0 or level == limit):
        return compute_utility(board)

    for move in moves:
        newBoard = play_move(board, 1, move[0], move[1])
        mVal = compute_utility(newBoard)
        moveVal = (mVal, move)
        heapq.heappush(heap, moveVal)

    heap.reverse()

    level += 1
    for move in heap: 
        newBoard = play_move(board, 1, move[1][0], move[1][1])
        newV = alphabeta_min_node(newBoard, a, b, level, limit)
        v = max(v, newV)
        if(v >= b):
            return v
        else:
            a = max(a, v)

    return v

"""
Computes the minimax value of a MIN node with alpha-beta pruning
"""
def alphabeta_min_node(board, alpha, beta, level=1, limit=float("inf")):

    v = float("inf")
    a = alpha
    b = beta

    heap = []
    moveDict = {}

    moves = get_possible_moves(board, 2)

    if(len(moves) == 0 or level == limit):
        return compute_utility(board)

    for move in moves:
        newBoard = play_move(board, 2, move[0], move[1])
        mVal = compute_utility(newBoard)
        moveVal = (mVal, move)
        heapq.heappush(heap, moveVal)

    level += 1
    for move in heap:
        newBoard = play_move(board, 2, move[1][0], move[1][1])
        newV = alphabeta_max_node(newBoard, a, b, level, limit)
        v = min(v, newV)
        if(v <= a):
            return v
        else: 
            b = min(b, v)

    return v

"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""
def select_move_alphabeta(board, color, limit=float("inf")):

    a = float("-inf")
    b = float("inf")

    realLim = limit

    if(color == 1):

        heap = [] 

        v = float("-inf")  
        moves = get_possible_moves(board, 1)
        for move in moves:
            new_board = play_move(board, 1, move[0], move[1])
            mVal = compute_utility(new_board)
            moveVal = (mVal, move)
            heapq.heappush(heap, moveVal) 

        for move in heap:
            new_board = play_move(board, 1, move[1][0], move[1][1])
            newV = alphabeta_min_node(new_board, a, b, 2, realLim)
            if(newV > v):
                v = newV
                bestMove = move[1]

    else:

        heap = []

        v = float("inf")
        moves = get_possible_moves(board, 2)
        for move in moves:
            newBoard = play_move(board, 2, move[0], move[1])
            mVal = compute_utility(newBoard)
            moveVal = (mVal, move)
            heapq.heappush(heap, moveVal) 

        heap.reverse()

        for move in heap:
            newBoard = play_move(board, 2, move[1][0], move[1][1])
            newV = alphabeta_max_node(newBoard, a, b, 2, realLim)
            if(v > newV):
                v = newV
                bestMove = move[1]

    return bestMove


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
