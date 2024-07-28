import random

class MCTS:
    def select_action(self, state):
        return random.choice(state.legal_actions())
