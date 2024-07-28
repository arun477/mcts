import random
import numpy as np
from copy import deepcopy

class VanilaMCTS:
    def __init__(self, initial_state, player, num_iterations=100, max_depth=5, exploit_const=5):
        self.num_itearions = num_iterations
        self.max_depth = max_depth
        self.exploit_const = exploit_const
        self.root_id = (0,)
        self.state_tree = { self.root_id: {
                'child': [],
                'parent': None,
                'state': initial_state,
                'player': player,
                'n': 1e-4,
                'w': 0,
                'q': 0,
            }
        }
        self.total_play = 0

    
    def get_ucb_score(self, state):
        exploitation_val = state['w'] / state['n']
        exploration_val = np.sqrt(np.log(self.total_play)/ state['n'])
        return exploitation_val + self.exploit_const * exploration_val

    
    def select_potential_leaf_action(self):
        selected_action_id = self.root_id
        selected_action_state = self.state_tree[selected_action_id]
        while len(selected_action_state['child']) > 0:
            parent_id = selected_action_id
            best_score, best_action_id = float('-inf'), None
            for action_id in selected_action_state['child']:
                action_state = self.state_tree[parent_id + action_id]
                ucb_score = self.get_ucb_score(action_state)
                if ucb_score > best_score:
                    best_score = ucb_score
                    best_action_id = action_id
            selected_action_id =parent_id + best_action_id
            selected_action_state = self.state_tree[selected_action_id]
        return selected_action_id

    
    def expand(self, selected_action_id):
        if self.is_terminal_state(self.state_tree[selected_action_id]):
            return selected_action_id
        
        state = deepcopy(self.state_tree[selected_action_id])
        current_player = str(state['player'])
        child = []
        avilable_next_actions = self.get_available_next_actions(state)
        for action in avilable_next_actions:
            action_id, action_position = action
            action_state = deepcopy(state)
            if current_player == 'x':
                state['player'] = 'o'
                state['state'][action_position] = -1
            else:
                state['player'] = 'x'
                state['state'][action_position] = 1
            self.state_tree[selected_action_id]['child'].append(action_id)
            child.append(selected_action_id + action_id)
            self.state_tree[selected_action_id + action_id] = action_state

        random_action_choice = np.random.randint(low=0, high=len(child), size=1)[0]
        child_action_id = child[random_action_choice]
        return child_action_id, len(child_action_id)
    
    
    def simulate_play(self, child_action_id):
        state = deepcopy(self.state_tree[child_action_id])
        winner = self.is_terminal_state(self.state_tree[child_action_id])
        if winner:
            return winner
        
        is_game_end = False
        while not is_game_end:
            available_actions = self.get_available_next_actions(state)
            
            
            


    def choose_best_action(self):
        for _ in range(self.num_itearions):
            selected_action_id = self.select_potential_leaf_action()
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
                
        
    