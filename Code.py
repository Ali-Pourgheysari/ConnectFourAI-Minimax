#import Library 
from pettingzoo.classic import connect_four_v3
import numpy as np


# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()

def heuristic():
    pass

def possible_moves(observation):
    moves = []
    for i in range(7):
        if observation['action_mask'] == 0:
            moves.append(i)
    return moves

def max_value(observation, alpha, beta, depth):
    if depth == 0 or termination or truncation:
        return heuristic(observation)
    value = float('-inf')
    for move in possible_moves(observation):
        new_observation = make_move(observation, move)
        value = max(value, min_value(new_observation, alpha, beta, depth-1))
        alpha = max(alpha, value)
        if beta <= alpha:
            break
    return value

def min_value(observation, alpha, beta, depth):
    if depth == 0 or termination or truncation:
        return heuristic(observation)
    value = float('inf')
    for move in possible_moves(observation):
        new_observation = make_move(observation, move)
        value = min(value, max_value(new_observation, alpha, beta, depth-1))
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value

def minimax(observation, depth, temp_env):
    best_score = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for move in possible_moves(observation):
        new_observation = make_move(observation, move)
        score = min_value(new_observation, alpha, beta, depth-1)
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
    return best_move

counter = 0
for agent in env.agent_iter():
    counter += 1

    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:

        action = None

    else:
        
        minimax(observation, 3, )

        # Retrun action
        action = env.action_space(agent).sample()  # this is where you would insert your policy

    if agent == 'player_1':
        action = int(input("Enter your action(0-6): "))

    env.step(action)

env.close()
