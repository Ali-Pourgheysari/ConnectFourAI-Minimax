#import Library 
from pettingzoo.classic import connect_four_v3
import numpy as np

# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()

def count_sublists_1s(lst):
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
    row_counts = [count_sublists_1s(row) for row in observation]

    for i, counts in enumerate(row_counts):
        output += counts

    # Count sublists of 1s in columns
    col_counts = [count_sublists_1s(observation[:, i]) for i in range(observation.shape[1])]

    for i, counts in enumerate(col_counts):
        output += counts

    # Count sublists of 1s in diagonals
    diagonal_counts = []
    anti_diagonal_counts = []
    for i in range(observation.shape[0]):
        diagonal_counts.append(count_sublists_1s(np.diagonal(observation, offset=i)))
        diagonal_counts.append(count_sublists_1s(np.diagonal(observation, offset=-i)))
        anti_diagonal_counts.append(count_sublists_1s(np.diagonal(np.fliplr(observation), offset=i)))
        anti_diagonal_counts.append(count_sublists_1s(np.diagonal(np.fliplr(observation), offset=-i)))

    for i, counts in enumerate(diagonal_counts):
        output += counts

    for i, counts in enumerate(anti_diagonal_counts):
        output += counts

    one_count = output.count(1)
    two_count = output.count(2)
    three_count = output.count(3)
    four_count = output.count(4)
    
    # calculate the total material score for the player
    material_score = 0.1*one_count + 0.3*two_count + 0.9*three_count + 1000*four_count
    return material_score

def heuristic(observation, player):
    my_material = get_material_score(observation['observation'], player)
    opponent_material = get_material_score(observation['observation'], 1-player)
    value = my_material - opponent_material
    return value
    
def possible_moves(observation):
    moves = []
    for i in range(7):
        if observation['action_mask'][i] == 1:
            moves.append(i)
    return moves

def minimax(observation, depth, termination, truncation, maximize_player, alpha, betha):
    if depth == 0 or termination or truncation:
        return heuristic(observation, int(not maximize_player))
    
    if maximize_player:
        value = float('-inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(maximize_player))
            value = max(value, minimax(new_observation, depth-1, termination, truncation, False, alpha, betha))
            alpha = max(alpha, value)
            observation = undo_move(observation, move, int(maximize_player))
            if betha <= alpha:
                break
        return value
    
    else:
        value = float('inf')
        for move in possible_moves(observation):
            new_observation = make_move(observation, move, int(maximize_player))
            value = min(value, minimax(new_observation, depth-1, termination, truncation, True, alpha, betha))
            betha = min(betha, value)
            observation = undo_move(observation, move, int(maximize_player))
            if betha <= alpha:
                break
        return value
    
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

    else:
        if agent == 'player_1':
            action = minimax(observation, 6, termination, truncation, True, float('-inf'), float('inf'))
        else:
            action = int(input("Enter your action(0-6): "))

    env.step(int(action))

env.close()
