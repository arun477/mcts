import pyspiel
import numpy as np
import mcts as MCTS
from gui import GUI


gui = GUI()
gui.draw_lines()


def print_board(state):
    if not state.is_terminal():
        gui.update_board(str(state) + "\n")
        print(state.observation_string())
        print("-------------")


def get_human_action(state):
    while True:
        try:
            legal_actions = state.legal_actions()
            action = int(input(f"Enter you move {str(legal_actions)} : "))
            if action in legal_actions:
                return action
            else:
                print("Invalid move, Try again")
        except ValueError:
            print("Should be numeric value")


def play_game(game, human_player):
    state = game.new_initial_state()
    while not state.is_terminal():
        print_board(state)
        current_player = state.current_player()
        if current_player == human_player:
            action = get_human_action(state)
        else:
            action = MCTS.select_action(state)

        state.apply_action(action)

    print_board(state)
    if state.returns()[human_player] > 0:
        print("Human Wins!")
    elif state.returns()[human_player] < 0:
        print("AI Wins!")
    else:
        print("Draw")


def main():
    game = pyspiel.load_game("tic_tac_toe")
    human_player = 1
    play_game(game, human_player)


main()
