#import Library 
from pettingzoo.classic import connect_four_v3
import numpy as np
import time
import copy

maxdepth = 5  # (maxdepth % depth == 2)
# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()

# count sublists of 1 in the given list
def count_sublists(lst):
    counts = []
    count = 0

    for num in lst:
        if num == 1:
            count += 1
        else:
            if count > 0:
                counts.append(count)
            count = 0

    if count > 0:
        counts.append(count)

    return counts

# calculate the value of each observation
def get_material_score(observation, player, terminate=False):
    # initialize counts for each line length
    observation = observation[:, :, player]

    output = []
    # Count sublists of 1s in rows
    row_counts = [count_sublists(row) for row in observation]

    for i, counts in enumerate(row_counts):
        output += counts

    # Count sublists of 1s in columns
    col_counts = [count_sublists(observation[:, i]) for i in range(observation.shape[1])]

    for i, counts in enumerate(col_counts):
        output += counts

    # Count sublists of 1s in diagonals
    diagonal_counts = []
    anti_diagonal_counts = []
    for i in range(observation.shape[0]):
        diagonal_counts.append(count_sublists(np.diagonal(observation, offset=i)))
        diagonal_counts.append(count_sublists(np.diagonal(observation, offset=-i)))
        anti_diagonal_counts.append(count_sublists(np.diagonal(np.fliplr(observation), offset=i)))
        anti_diagonal_counts.append(count_sublists(np.diagonal(np.fliplr(observation), offset=-i)))

    diagonal_counts.pop(0)
    anti_diagonal_counts.pop(0)
    for i, counts in enumerate(diagonal_counts):
        output += counts

    for i, counts in enumerate(anti_diagonal_counts):
        output += counts

    # count the number of 2s, 3s, and 4s
    two_count = output.count(2)
    three_count = output.count(3)
    four_count = output.count(4)

    if terminate:
        return bool(four_count)
    # calculate the total material score for the player
    material_score = 0.3*two_count + 0.9*three_count
    return material_score

# heuristic function
def heuristic(observation, player):
    my_material = get_material_score(observation['observation'], 1-player)
    opponent_material = get_material_score(observation['observation'], player)
    value = my_material - opponent_material
    return value

# get all possible moves
def possible_moves(observation):
    moves = []
    for i in range(7):
        if observation['action_mask'][i] == 1:
            moves.append(i)
    return moves

# minimax algorithm
def minimax(observation, depth, termination, truncation, maximize_player, alpha, beta):
    if depth == 0 or termination or truncation:
        return None, heuristic(observation, int(not maximize_player))

    # maximize player
    if maximize_player:
        best_move = None
        best_value = float('-inf')
        # for each possible move
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(not maximize_player))
            # check if the move results in a win
            termination = get_material_score(new_observation['observation'], int(not maximize_player), True)
            # recursively call minimax
            _, value = minimax(new_observation, depth - 1, termination, truncation, False, alpha, beta)
            observation = undo_move(new_observation, move, int(not maximize_player))
            # if the move results in a win, return the move and a high value
            if termination:
                return move, 1000
            # if the value is greater than the best value, update the best value and best move
            if value > best_value:
                best_value = value
                best_move = move
            # update alpha
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move, best_value

    else:
        best_move = None
        best_value = float('inf')
        # for each possible move
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(not maximize_player))
            # check if the move results in a win
            termination = get_material_score(new_observation['observation'], int(not maximize_player), True)
            # recursively call minimax
            _, value = minimax(new_observation, depth - 1, termination, truncation, True, alpha, beta)
            observation = undo_move(new_observation, move, int(not maximize_player))
            # if the move results in a win, return the move and a high value
            if termination:
                return move, -1000
            # if the value is greater than the best value, update the best value and best move
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            # update beta
            if beta <= alpha:
                break
        return best_move, best_value

# make a move    
def make_move(observation, move, player):
    new_observation = copy.deepcopy(observation)

    # find the first empty space in the column
    for i in range(5, -1, -1):
        if all(elem == 0 for elem in new_observation['observation'][i, move]):
            new_observation['observation'][i][move][player] = 1
            break
    # if the column is full, set the action mask to 0
    if any(elem == 1 for elem in new_observation['observation'][0][move]):
        new_observation['action_mask'][move] = 0
        
    
    return new_observation

# undo a move
def undo_move(observation, move, player):
    old_observation = copy.deepcopy(observation)

    # find the first non-empty space in the column
    for i in range(6):
        if old_observation['observation'][i][move][player] == 1:
            old_observation['observation'][i][move][player] = 0
            break

    # if the column is empty, set the action mask to 1
    if all(elem == 0 for elem in old_observation['observation'][0][move]):
        old_observation['action_mask'][move] = 1
        
    return old_observation

firstmove = True
for agent in env.agent_iter():

    observation, _, termination, truncation, info = env.last()

    if termination or truncation:
        action = None

        if agent == 'player_1':
            print("Player 2 wins!")
        else:
            print("Player 1 wins!")
        time.sleep(5)
        break

    else:
        # if it is the first move, play in the middle column
        if firstmove:
            action = 3
            firstmove = False
        elif agent == 'player_0':
            action, _ = minimax(observation, maxdepth, termination, truncation, True, float('-inf'), float('inf'))
        else:
            action = int(input("Enter your action(0-6): "))

    # if the action equals None, the player resigns
    if action is None:
        print('player 1 resigns')
        break

    env.step(int(action))

env.close()
