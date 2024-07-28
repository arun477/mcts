import random

class VanilaMCTS:
    def __init__(self, initial_state, player, num_iterations=100, max_depth=5):
        self.num_itearions = num_iterations
        self.max_depth = max_depth
        self.root_id = (0,)
        self.state_tree[self.root_id] = {
            'child': [],
            'parent': None,
            'state': initial_state,
            'player': player,
            'n': 1e-4,
            'w': 0,
            'q': 0,
        }
        self.total_play = 0
    
    def choose_best_action(self):
        for _ in range(self.num_itearions):
            selected_action_id = self.select()
            child_action_id, play_depth = self.expand(selected_action_id)
            if play_depth >= self.max_depth:
                break
            winner = self.simulate_play(child_action_id)
            self.backprop_stats(child_action_id, winner)
        
        best_action_value, best_action = float('-inf'), None
        for action_id in self.state_tree[self.root_id]['child']:
            action_state = self.state_tree[self.root_id + action_id]
            if action_state['q'] > best_action_value:
                best_action_value = action_state['q']
                best_action = action_id

        return best_action, best_action_value
                
        
    