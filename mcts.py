import numpy as np
from copy import deepcopy


class VanilaMCTS:
    def __init__(self, n_iterations, depth=15, exploration_const=5.0, tree=None, game_board=None, player=None):
        self.n_iterations = n_iterations
        self.depth = depth
        self.total_n = 0
        self.exploration_const = exploration_const
        if tree is None:
            self.tree = self._set_tictactoe(
                game_board,
                player,
            )
        else:
            self.tree = tree

    def _set_tictactoe(self, game_board, player):
        root_id = (0,)
        tree = {
            root_id: {
                "state": game_board,
                "player": player,
                "child": [],
                "parent": None,
                "n": 0,
                "w": 0,
                "q": None,
            }
        }
        return tree

    def selection(self):
        leaf_node_found = False
        leaf_node_id = (0,)
        while not leaf_node_found:
            node_id = leaf_node_id
            n_child = len(self.tree[node_id]["child"])
            if n_child == 0:
                leaf_node_id = node_id
                leaf_node_found = True
            else:
                maximum_uct_value = -100.0
                for i in range(n_child):
                    action = self.tree[node_id]["child"][i]
                    child_id = node_id + (action,)
                    w = self.tree[child_id]["w"]
                    n = self.tree[child_id]["n"]
                    total_n = self.total_n
                    if n == 0:
                        n = 1e-4
                    exploitation_value = w / n
                    exploration_value = np.sqrt(np.log(total_n) / n)
                    utc_value = exploitation_value + self.exploration_const * exploration_value
                    if utc_value > maximum_uct_value:
                        maximum_uct_value = utc_value
                        leaf_node_id = child_id
        depth = len(leaf_node_id)
        return leaf_node_id, depth
    

    def expansion(self, leaf_node_id):
        leaf_state = self.tree[leaf_node_id]['state']
        winner = self._is_terminal(leaf_state)
        possible_actions = self._get_valid_actions(leaf_state)
        child_node_id = leaf_node_id
        if winner is None:
            childs = []
            for action_set in possible_actions:
                action, action_idx = action_set
                state = deepcopy(self.tree[leaf_node_id]['state'])
                current_player = self.tree[leaf_node_id]['player']
                if current_player == 'o':
                    next_turn = 'x'
                    state[action] = 1
                else:
                    next_turn = 'o'
                    state[action] = -1
                
                child_id = leaf_node_id + (action_idx,)
                childs.append(child_id)
                self.tree[child_id] = {'state': state,
                                        'player': next_turn,
                                        'child': [],
                                        'parent': leaf_node_id,
                                        'n': 0, 'w': 0, 'q': 0}
                self.tree[leaf_node_id]['child'].append(action_idx)
            rand_idx = np.random.randint(low=0, high=len(childs), size=1)[0]
            child_node_id = childs[rand_idx[0]]
        return child_node_id
            
                
        

    def solve(self):
        for _ in range(self.n_iterations):
            leaf_node_id, depth_searched = self.selection()
            child_node_id = self.expansion(leaf_node_id)
            winner = self.simulation(child_node_id)
            self.backprop(child_node_id, winner)
            if depth_searched > self.depth:
                break

        current_state_node_id = (0,)
        action_candidates = self.tree[current_state_node_id]["child"]
        best_q = -100
        for a in action_candidates:
            q = self.tree[current_state_node_id + (a,)]["q"]
            if q > best_q:
                best_q = q
                best_action = a

        return best_action, best_q, depth_searched
