# Define the action space
action_space = [(dx, dy, dz, speed) for dx in [-1, 0, 1] for dy in [-1, 0, 1] for dz in [-1, 0, 1] for speed in
                [0, 1]]

print(action_space)

# Define a function that maps an action to an integer
def action_to_index(action):
    return action_space.index(action)


# Define a function that maps an integer to an action
def index_to_action(index):
    return action_space[index]

