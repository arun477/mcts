import random
import numpy as np
import matplotlib.pyplot as plt


_explore_const = 5
_num_iterations = 100


def get_initial_values(game_state, parent):
    return {"game_state": game_state, "parent": parent, "w": 0, "n": 1e-4, "q": 0, "child": []}


def get_state_tree(game_state, root_id):
    return {root_id: get_initial_values(game_state, None)}


def get_ucb_score(child_id, state_tree, parent_visits):
    child_state = state_tree[child_id]
    n, w = child_state["n"], child_state["w"]
    exploit_val = w / n
    exploration_val = np.sqrt(np.log(parent_visits) / n)
    return exploit_val + _explore_const * exploration_val


def select_leaf_node(state_tree, node_id):
    while True:
        child = state_tree[node_id]["child"]
        if len(child) == 0:
            return node_id

        best_leaf_node_id, best_score = node_id, float("-inf")
        for action in child:
            child_id = node_id + (action,)
            ucb_score = get_ucb_score(child_id, state_tree, state_tree[node_id]["n"])
            if ucb_score > best_score:
                best_score = ucb_score
                best_leaf_node_id = child_id
        node_id = best_leaf_node_id


def expand_node(selected_leaf_node_id, state_tree):
    game_state = state_tree[selected_leaf_node_id]["game_state"].clone()
    if game_state.is_terminal():
        return selected_leaf_node_id

    child_ids = []
    legal_actions = game_state.legal_actions()
    for action in legal_actions:
        next_game_state = game_state.clone()
        next_game_state.apply_action(action)
        child_id = selected_leaf_node_id + (action,)
        state_tree[child_id] = get_initial_values(next_game_state, parent=selected_leaf_node_id)
        child_ids.append(child_id)
        state_tree[selected_leaf_node_id]["child"].append(action)

    return random.choice(child_ids)


def simulate_play(unexplored_child_node_id, state_tree):
    game_state = state_tree[unexplored_child_node_id]["game_state"]
    if game_state.is_terminal():
        return game_state.rewards()
    game_state = game_state.clone()
    while not game_state.is_terminal():
        game_state.apply_action(random.choice(game_state.legal_actions()))
    return game_state.rewards()


def backprop(unexplored_child_node_id, reward, state_tree):
    node_id = unexplored_child_node_id
    while True:
        parent = state_tree[node_id]["parent"]
        state_tree[node_id]["n"] += 1
        state_tree[node_id]["w"] += reward
        state_tree[node_id]["q"] = state_tree[node_id]["w"] / state_tree[node_id]["n"]
        if parent is None:
            break
        node_id = parent


def choose_best_action(root_id, state_tree):
    best_score, best_action = float("-inf"), None
    for action in state_tree[root_id]["child"]:
        child_id = root_id + (action,)
        q = state_tree[child_id]["q"]
        if q > best_score:
            best_score = q
            best_action = action
    return best_action


def plot_score_grid(scores):
    fig, ax = plt.subplots()

    cax = ax.matshow(scores, cmap="coolwarm")

    fig.colorbar(cax)

    for (i, j), val in np.ndenumerate(scores):
        ax.text(j, i, f"{val:.2f}", ha="center", va="center", color="black")

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(3))

    ax.set_xticklabels(["0", "1", "2"])
    ax.set_yticklabels(["0", "1", "2"])

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    plt.title("Tic-Tac-Toe Move Scores")
    plt.show()


def plot_board_scores(root_id, state_tree):
    q_values = np.zeros(9)
    for action in state_tree[root_id]["child"]:
        child_id = root_id + (action,)
        q = state_tree[child_id]["q"]
        q_values[action] = q
    q_values = q_values.reshape(3, 3)
    print(q_values.reshape(3, 3))
    plot_score_grid(q_values)


def select_action(game_state):
    root_id = (0,)
    state_tree = get_state_tree(game_state.clone(), root_id)

    for _ in range(_num_iterations):
        selected_leaf_node_id = select_leaf_node(state_tree, root_id)
        unexplored_child_node_id = expand_node(selected_leaf_node_id, state_tree)
        rewards = simulate_play(unexplored_child_node_id, state_tree)
        reward = rewards[game_state.current_player()]
        backprop(unexplored_child_node_id, reward, state_tree)

    plot_board_scores(root_id, state_tree)
    best_action = choose_best_action(root_id, state_tree)
    return best_action
