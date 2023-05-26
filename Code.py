#import Library 
from pettingzoo.classic import connect_four_v3
import numpy as np


# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()

def heuristic(observation):
    

def possible_moves(observation):
    moves = []
    for i in range(7):
        if observation['action_mask'] == 1:
            moves.append(i)
    return moves

def minimax(observation, depth, termination, truncation, maximize_player, alpha, betha):
    if depth == 0 or termination or truncation:
        return heuristic(observation)
    
    if maximize_player:
        value = float('-inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, 0)
            value = max(value, minimax(new_observation, depth-1, termination, truncation, False, alpha, betha))
            alpha = max(alpha, value)
            if betha <= alpha:
                break
        return value
    
    else:
        value = float('inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, 1)
            value = min(value, minimax(new_observation, depth-1, termination, truncation, True, alpha, betha))
            betha = min(betha, value)
            if betha <= alpha:
                break
        return value
    
def make_move(observation, move, player):
    new_observation = observation
    if new_observation['observation'][6, move, :] == 1:
        new_observation['action_mask'][move] = 0

    for i in range(6):
        if all(elem == 0 for elem in new_observation[i, move]):
            new_observation[i, move, player] = 1
            break
        
    return new_observation

for agent in env.agent_iter():

    observation, _, termination, truncation, info = env.last()

    if termination or truncation:
        action = None

    else:
        if agent == 'player_0':
            action = minimax(observation, 3, termination, truncation, True, float('-inf'), float('inf'))
        else:
            action = int(input("Enter your action(0-6): "))

    env.step(action)

env.close()

# def max_value(observation, alpha, beta, depth, termination, truncation):
#     if depth == 0 or termination or truncation:
#         return heuristic(observation)
#     value = float('-inf')
#     for move in possible_moves(observation):
#         new_observation = make_move(observation, move)
#         value = max(value, min_value(new_observation, alpha, beta, depth-1))
#         alpha = max(alpha, value)
#         if beta <= alpha:
#             break
#     return value

# def min_value(observation, alpha, beta, depth, termination, truncation):
#     if depth == 0 or termination or truncation:
#         return heuristic(observation)
#     value = float('inf')
#     for move in possible_moves(observation):
#         new_observation = make_move(observation, move)
#         value = min(value, max_value(new_observation, alpha, beta, depth-1))
#         beta = min(beta, value)
#         if beta <= alpha:
#             break
#     return value