#import Library 
from pettingzoo.classic import connect_four_v3
import numpy as np

# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()

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

def get_material_score(observation, player):
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

    for i, counts in enumerate(diagonal_counts):
        output += counts

    for i, counts in enumerate(anti_diagonal_counts):
        output += counts

    # count the number of 2s, 3s, and 4s
    two_count = output.count(2)
    three_count = output.count(3)
    four_count = output.count(4)
    
    # calculate the total material score for the player
    material_score = 0.3*two_count + 0.9*three_count + 10000*four_count
    return material_score

def heuristic(observation, player):
    my_material = get_material_score(observation['observation'], 1-player) + 0.1
    opponent_material = get_material_score(observation['observation'], player)
    value = my_material - opponent_material
    return value
    
def possible_moves(observation):
    moves = []
    for i in range(7):
        if observation['action_mask'][i] == 1:
            moves.append(i)
    return moves

def minimax(observation, depth, termination, truncation, maximize_player, alpha, beta):
    if depth == 0 or termination or truncation:
        return None, heuristic(observation, int(not maximize_player))

    if maximize_player:
        best_move = None
        best_value = float('-inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(not maximize_player))
            _, value = minimax(new_observation, depth - 1, termination, truncation, False, alpha, beta)
            observation = undo_move(observation, move, int(not maximize_player))
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_move, best_value

    else:
        best_move = None
        best_value = float('inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(not maximize_player))
            _, value = minimax(new_observation, depth - 1, termination, truncation, True, alpha, beta)
            observation = undo_move(observation, move, int(not maximize_player))
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_move, best_value

    
def make_move(observation, move, player):
    new_observation = observation.copy()

    for i in range(5, -1, -1):
        if all(elem == 0 for elem in new_observation['observation'][i, move]):
            new_observation['observation'][i][move][player] = 1
            break

    if any(elem == 1 for elem in new_observation['observation'][0][move]):
        new_observation['action_mask'][move] = 0
        
    return new_observation


def undo_move(observation, move, player):
    old_observation = observation.copy()

    for i in range(6):
        if old_observation['observation'][i][move][player] == 1:
            old_observation['observation'][i][move][player] = 0
            break

    if all(elem == 0 for elem in old_observation['observation'][0][move]):
        old_observation['action_mask'][move] = 1
        
    return old_observation

for agent in env.agent_iter():

    observation, _, termination, truncation, info = env.last()

    if termination or truncation:
        action = None

        if agent == 'player_1':
            print("Player 2 wins!")
        else:
            print("Player 1 wins!")
        break

    else:
        if agent == 'player_0':
            action, _ = minimax(observation, 2, termination, truncation, True, float('-inf'), float('inf'))
        else:
            action = int(input("Enter your action(0-6): "))

    env.step(int(action))

env.close()
