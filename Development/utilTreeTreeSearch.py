from operator import itemgetter

from constants import MAX_FORECAST
from othelloGameUtilState import OthelloGameState
from othelloGame import OthelloGame
from random import shuffle


class UtilTreeTreeSearch:

    def __init__(self, player: int, othello_game_state: OthelloGameState, parent=None, limit=MAX_FORECAST):
        self.parent = parent
        self.othello_game_state = othello_game_state
        self.child_nodes = []
        self.player = player

        self._build_tree(limit)

    def _build_tree(self, limit):
        if limit > 0:
            available_moves = self.othello_game_state.available_moves
            if len(available_moves) > 0:
                for possible_move in self.othello_game_state.available_moves:
                    new_board = OthelloGame.copy_board(self.othello_game_state.board)
                    OthelloGame.set_stone_static(new_board, self.othello_game_state.turn_number, possible_move)
                    new_game_state = OthelloGame._compute_moves_and_stones_to_turn(new_board,
                                                                                   self.othello_game_state.turn_number + 1,
                                                                                   0)
                    self.child_nodes.append((possible_move, UtilTreeTreeSearch(self.player, new_game_state, self, limit - 1)))
            elif self.othello_game_state.number_of_passes < 2:
                new_game_state = OthelloGame._compute_moves_and_stones_to_turn(self.othello_game_state.board,
                                                                               self.othello_game_state.turn_number + 1,
                                                                               self.othello_game_state.number_of_passes + 1)
                self.child_nodes.append(((-1, -1), UtilTreeTreeSearch(self.player, new_game_state, self, limit - 1)))
            # else:
            #     print("Game finished. End of branch")
        # else:
        #    print("End of branch reached!")

    def get_best_decision(self):
        information_dict = dict()
        information_dict["number_of_wins"] = 0
        information_dict["number_of_losses"] = 0
        if len(self.child_nodes) == 0:
            winner = OthelloGame.get_winner(self.othello_game_state.board)
            if winner == self.player:
                information_dict["number_of_wins"] = 1
            else:
                information_dict["number_of_losses"] = 1
            information_dict["min_points"] = information_dict["max_points"] = \
            OthelloGame.get_stats(self.othello_game_state.board)[self.player]
            # print(information_dict)
            return information_dict
        elif self.parent is not None:
            min_values = list()
            max_values = list()
            for (_, sub_tree) in self.child_nodes:
                best_decision_sub_tree = sub_tree.get_best_decision()
                information_dict["number_of_wins"] += best_decision_sub_tree["number_of_wins"]
                information_dict["number_of_losses"] += best_decision_sub_tree["number_of_losses"]
                min_values.append(best_decision_sub_tree["min_points"])
                max_values.append(best_decision_sub_tree["max_points"])
            information_dict["min_points"] = min(min_values)
            information_dict["max_points"] = max(max_values)
            # print(information_dict)
            return information_dict
        else:
            heuristic = list()
            for (decision, sub_tree) in self.child_nodes:
                best_decision_sub_tree = sub_tree.get_best_decision()
                heuristic.append((decision, best_decision_sub_tree["number_of_wins"] * 100 +  best_decision_sub_tree["max_points"]))
            shuffle(heuristic)
            best_heuristic = max(heuristic, key=itemgetter(1))[0]
            return best_heuristic

