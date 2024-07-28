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
        self.win_mark = 2

    
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
        avilable_next_actions = self.get_available_next_actions(state['state'])
        for action in avilable_next_actions:
            action_id, action_position = action
            action_state = deepcopy(state)
            action_state['parent'] = selected_action_id
            if current_player == 'x':
                action_state['player'] = 'o'
                action_state['state'][action_position] = -1
            else:
                action_state['player'] = 'x'
                action_state['state'][action_position] = 1

            self.state_tree[selected_action_id]['child'].append(action_id)
            child.append(selected_action_id + action_id)
            self.state_tree[selected_action_id + action_id] = action_state

        random_action_choice = np.random.randint(low=0, high=len(child), size=1)[0]
        child_action_id = child[random_action_choice]
        return child_action_id, len(child_action_id)
    

    def is_terminal_state(self, leaf_state):
        def __who_wins(sums, win_mark):
            if np.any(sums == win_mark):
                return "o"
            if np.any(sums == -win_mark):
                return "x"
            return None

        def __is_terminal_in_conv(leaf_state, win_mark):
            for axis in range(2):
                sums = np.sum(leaf_state, axis=axis)
                result = __who_wins(sums, win_mark)
                if result is not None:
                    return result

            for order in [-1, 1]:
                diags_sum = np.sum(np.diag(leaf_state[::order]))
                result = __who_wins(diags_sum, win_mark)
                if result is not None:
                    return result

            return None

        win_mark = self.win_mark
        n_rows_board = len(self.state_tree[(0,)]["state"])
        window_size = win_mark
        window_positions = range(n_rows_board - win_mark + 1)
        for row in window_positions:
            for col in window_positions:
                window = leaf_state[row : row + window_size, col : col + window_size]
                winner = __is_terminal_in_conv(window, win_mark)
                if winner is not None:
                    return winner

        if not np.any(leaf_state == 0):
            return "draw"

        return None

    def get_available_next_actions(self, leaf_state):
        actions = []
        count = 0
        state_size = len(leaf_state)
        for i in range(state_size):
            for j in range(state_size):
                if leaf_state[i][j] == 0:
                    actions.append([(i, j), count])
                count += 1
        return actions

    def simulate_play(self, child_action_id):
        state = deepcopy(self.state_tree[child_action_id])
        winner = self.is_terminal_state(self.state_tree[child_action_id]['state'])
        if winner:
            return winner
        
        is_game_end = False
        while not is_game_end:
            available_actions = self.get_available_next_actions(state['state'])
            random_action_choice = np.random.randint(low=0, high=len(available_actions), size=1)[0]
            action_id, action_position = available_actions[random_action_choice]
            if state['player'] == 'x':
                state['player'] = 'o'
                state['state'][action_position] = -1
            else:
                state['player'] = 'x'
                state['state'][action_position] = 1
            
            winner = self.is_terminal_state(state['state'])
            if winner:
                return winner
            
    
    def backprop_stats(self, child_action_id, winner):
        if winner == 'draw':
            reward = 0
        elif winner == 'x':
            reward = 1
        else:
            reward = -1
        while True:
            self.state_tree[child_action_id]['n'] += 1
            self.state_tree[child_action_id]['w'] += reward
            self.state_tree[child_action_id]['q'] = self.state_tree[child_action_id]['w'] / self.state_tree[child_action_id]['n']
            child_action_id = self.state_tree[child_action_id]['parent']
            if child_action_id is None:
                break
              

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
                
        
    