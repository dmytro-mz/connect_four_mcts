import configparser

import numpy as np

from connect_four.game import GameState, Game

mcts_config = configparser.ConfigParser()
mcts_config.read('config.ini')


class StateNode:
    def __init__(self, state: GameState):
        self.state = state
        self.w = 0
        self.n = 0
        self.parents = []
        self.children = []

    def _get_z(self):
        return self.w / self.n

    def get_ucb(self):
        return self._get_z() + mcts_config['C'] * np.sqrt(np.ln(self.parents[0].n / self.n))


class StateGraph:
    def __init__(self, root_node: StateNode):
        self.root = root_node


class MCTS:
    def __init__(self, root_state: GameState, game: Game):
        self.graph = StateGraph(StateNode(root_state))
        self.game = game
        self.all_state_nodes = {root_state}

    def select(self) -> StateNode:
        return None

    def expand(self, state_node):
        pass

    def simulate(self, state_node) -> int:
        return 1

    def propagate(self, state_node, value):
        pass

    def get_next_action(self) -> int:
        for _ in range(mcts_config['N_SIMULATIONS']):
            selected_leaf = self.select()
            if not selected_leaf.state.is_internal():
                self.expand(selected_leaf)
                simulation_node = np.random.choice(selected_leaf.children)
                simulation_value = self.simulate(simulation_node)
            else:
                simulation_node = selected_leaf
                simulation_value = selected_leaf.state.value
            self.propagate(simulation_node, simulation_value)

        optimal_next_state = max(self.graph.root.children, key=lambda child: child.n)
        return self.game.get_action_to_transit_state(self.graph.root.state, optimal_next_state)
