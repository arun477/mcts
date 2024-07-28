import random




def select_action(state):
    return random.choice(state.legal_actions())
