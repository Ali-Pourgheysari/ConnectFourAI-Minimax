#import Library 
from pettingzoo.classic import connect_four_v3

# Create Environment
env = connect_four_v3.env(render_mode="human")
env.reset()



def get_material_score(observation, player):
    # initialize counts for each line length
    one_count = 0
    two_count = 0
    three_count = 0
    four_count = 0
    observation = observation[:, :, player]

    for row in observation:
        # check horizontal lines
        for i in range(len(row) - 3):
            sub_list = list(row[i:i+4])
            if sub_list.count(1) == 1 and sub_list.count(0) == 3:
                one_count += 1
            elif sub_list.count(1) == 2 and sub_list.count(0) == 2:
                two_count += 1
            elif sub_list.count(1) == 3 and sub_list.count(0) == 1:
                three_count += 1
            elif sub_list.count(1) == 4 and sub_list.count(0) == 0:
                four_count += 1

    for col in range(len(observation[0])):
        # check vertical lines
        for i in range(len(observation) - 3):
            sub_list = [observation[j][col] for j in range(i, i+4)]
            if sub_list.count(1) == 1 and sub_list.count(0) == 3:
                one_count += 1
            elif sub_list.count(1) == 2 and sub_list.count(0) == 2:
                two_count += 1
            elif sub_list.count(1) == 3 and sub_list.count(0) == 1:
                three_count += 1
            elif sub_list.count(1) == 4 and sub_list.count(0) == 0:
                four_count += 1

    for i in range(len(observation) - 3):
        # check diagonal lines (top-left to bottom-right)
        for j in range(len(observation[0]) - 3):
            sub_list = [observation[i+k][j+k] for k in range(4)]
            if sub_list.count(1) == 1 and sub_list.count(0) == 3:
                one_count += 1
            elif sub_list.count(1) == 2 and sub_list.count(0) == 2:
                two_count += 1
            elif sub_list.count(1) == 3 and sub_list.count(0) == 1:
                three_count += 1
            elif sub_list.count(1) == 4 and sub_list.count(0) == 0:
                four_count += 1

        # check diagonal lines (bottom-left to top-right)
        for j in range(len(observation[0]) - 3):
            sub_list = [observation[i+3-k][j+k] for k in range(4)]
            if sub_list.count(1) == 1 and sub_list.count(0) == 3:
                one_count += 1
            elif sub_list.count(1) == 2 and sub_list.count(0) == 2:
                two_count += 1
            elif sub_list.count(1) == 3 and sub_list.count(0) == 1:
                three_count += 1
            elif sub_list.count(1) == 4 and sub_list.count(0) == 0:
                four_count += 1
    
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
    old_observaion = observation.copy()

    for i in range(6):
        if old_observaion['observation'][i][move][player] == 1:
            old_observaion['observation'][i][move][player] = 0
            break

    if all(elem == 0 for elem in old_observaion['observation'][0][move]):
        old_observaion['action_mask'][move] = 1
        
    return old_observaion

for agent in env.agent_iter():

    observation, _, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
        break

    else:
        if agent == 'player_0':
            action = minimax(observation, 6, termination, truncation, True, float('-inf'), float('inf'))
        else:
            action = int(input("Enter your action(0-6): "))

    env.step(int(action))

env.close()