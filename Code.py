#import Library 
from pettingzoo.classic import connect_four_v3

# Create Environment
env = connect_four_v3.env(render_mode="human")

env.reset()
for agent in env.agent_iter():

    observation, reward, termination, truncation, info = env.last()

    break

    if termination or truncation:

        action = None

    else:

        # Retrun action
        action = env.action_space(agent).sample()  # this is where you would insert your policy

    env.step(action)

env.close()
