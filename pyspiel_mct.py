import random

def get_state_tree(state, root_id):
    return {root_id: { 'state': state, 'parent': None, 'w':0, 'n': 1e-4, 'q': 0, 'child': []}}

def select_leaf_node(state_tree, node_id):
    child = state_tree[node_id]['child']
    if len(child) == 0:
        return node_id

    best_leaf_node_id, best_score = None, float('-inf')
    for child_id in child:
        pass
        
     
def select_action(state):
    root_id = (0,)
    state_tree = get_state_tree(state, root_id)
    selected_leaf_node_id = select_leaf_node(state_tree, root_id)
    

    return random.choice(state.legal_actions())

