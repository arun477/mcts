import numpy as np
from copy import deepcopy
import json


class Policy:
    def __init__(self):
        self.tree = {}


class VanilaMCTS(object):
    def __init__(self, n_iterations, depth=15, exploration_const=5.0, win_mark=3, tree=None, game_board=None, player=None):
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
        n_rows = len(game_board)
        self.n_rows = n_rows
        self.win_mark = win_mark

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
        leaf_state = self.tree[leaf_node_id]["state"]
        winner = self._is_terminal(leaf_state)
        possible_actions = self._get_valid_actions(leaf_state)
        child_node_id = leaf_node_id
        if winner is None:
            childs = []
            for action_set in possible_actions:
                action, action_idx = action_set
                state = deepcopy(self.tree[leaf_node_id]["state"])
                current_player = self.tree[leaf_node_id]["player"]
                if current_player == "o":
                    next_turn = "x"
                    state[action] = 1
                else:
                    next_turn = "o"
                    state[action] = -1

                child_id = leaf_node_id + (action_idx,)
                childs.append(child_id)
                self.tree[child_id] = {"state": state, "player": next_turn, "child": [], "parent": leaf_node_id, "n": 0, "w": 0, "q": 0}
                self.tree[leaf_node_id]["child"].append(action_idx)
            rand_idx = np.random.randint(low=0, high=len(childs), size=1)
            child_node_id = childs[rand_idx[0]]
        return child_node_id

    def _is_terminal(self, leaf_state):
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
        n_rows_board = len(self.tree[(0,)]["state"])
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

    def _get_valid_actions(self, leaf_state):
        actions = []
        count = 0
        state_size = len(leaf_state)
        for i in range(state_size):
            for j in range(state_size):
                if leaf_state[i][j] == 0:
                    actions.append([(i, j), count])
                count += 1
        return actions

    def simulation(self, child_node_id):
        self.total_n += 1
        state = deepcopy(self.tree[child_node_id]["state"])
        previous_player = deepcopy(self.tree[child_node_id]["player"])
        anybody_win = False

        while not anybody_win:
            winner = self._is_terminal(state)
            if winner is not None:
                anybody_win = True
            else:
                possible_actions = self._get_valid_actions(state)
                rand_idx = np.random.randint(low=0, high=len(possible_actions), size=1)[0]
                action, _ = possible_actions[rand_idx]

                if previous_player == "o":
                    current_player = "x"
                    state[action] = -1
                else:
                    current_player = "o"
                    state[action] = 1

                previous_player = current_player

        return winner

    def backprop(self, child_node_id, winner):
        player = deepcopy(self.tree[(0,)]["player"])
        if winner == "draw":
            reward = 0
        elif winner == player:
            reward = 1
        else:
            reward = -1

        finished_backprop = False
        node_id = child_node_id
        while not finished_backprop:
            self.tree[node_id]["n"] += 1
            self.tree[node_id]["w"] += reward
            self.tree[node_id]["q"] = self.tree[node_id]["w"] / self.tree[node_id]["n"]
            parent_id = self.tree[node_id]["parent"]
            if parent_id == (0,):
                self.tree[parent_id]["n"] += 1
                self.tree[parent_id]["w"] += reward
                self.tree[parent_id]["q"] = self.tree[parent_id]["w"] / self.tree[parent_id]["n"]
                finished_backprop = True
            else:
                node_id = parent_id

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
