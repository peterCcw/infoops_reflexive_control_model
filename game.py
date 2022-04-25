import copy
from typing import List
from agent import Agent


class Game:
    """
    Main class simulating p-beauty game contest. It keeps results of each round in 'results' field according to the
    following order: 0. awareness structures at the beginning of the round, 1. awareness structures at the end of the
    round (after intelligence/counterintelligence actions and calculating) 2. guesses of each agent (player), 3. overall
    score (mean of guesses multiplied by p-value) 4. winner or winners (for multiple same optimal guess case)
    """
    def __init__(self, agents_data_array: List[List[int]], p: float, min_val: int, max_val: int):
        """
        :param agents_data_array: List[List[int]]
        :param p: float
        :param min_val: int
        :param max_val: int
        """
        self.number_of_agents = len(agents_data_array)
        self.agents = [Agent(i, self, self.number_of_agents, agents_data_array[i][0], agents_data_array[i][1],
                             agents_data_array[i][2]) for i in range(len(agents_data_array))]

        self.agents_ordered = self.agents.copy()
        self.agents_ordered.sort(key=lambda x: x.intel_level)

        self.p = p
        self.min_val = min_val
        self.max_val = max_val

        self.intel_actions = []
        self.results = []

    def run_round(self) -> None:
        """
        Simulation of single round. It executes intel actions and calculates guess for each agent according to order by
        intelligence level. Calculates overall score and marks winners. Saves data for results.
        """
        # Saving initial awareness structures
        start_of_round_awareness_structures = [agent.awareness_structure for agent in self.agents]
        start_of_round_awareness_structures = copy.deepcopy(start_of_round_awareness_structures)

        # Execution of intelligence/counterintelligence actions and calculating guess for each agent
        guesses_of_players = []
        for agent in self.agents_ordered:
            actions = filter(lambda x: (x.attacker.id_number == agent.id_number), self.intel_actions)
            for action in actions:
                action.run_action()
                self.intel_actions.remove(action)
            guesses_of_players.append((agent.id_number, agent.calculate_guess_value()))

        # Sorting guesses by id of agents
        guesses_of_players.sort(key=lambda x: x[0])
        guesses_of_players = [output[1] for output in guesses_of_players]

        # Saving final awareness structures
        end_of_round_awareness_structures = [agent.awareness_structure for agent in self.agents]
        end_of_round_awareness_structures = copy.deepcopy(end_of_round_awareness_structures)

        # Calculating overall score
        score_overall = sum(guesses_of_players) / len(guesses_of_players)

        # Calculating winners
        results_of_players = []
        for i in range(len(guesses_of_players)):
            results_of_players.append((abs(score_overall - guesses_of_players[i]), i))
        results_of_players.sort(key=lambda x: x[0])
        winners = [res[1] if res[0] == results_of_players[0][0] else None for res in results_of_players]
        while None in winners:
            winners.remove(None)

        # Saving all results for single round
        self.results.append([start_of_round_awareness_structures, end_of_round_awareness_structures, guesses_of_players,
                             score_overall, winners])

        # Sending feedback to agents and preparing them for next round
        for agent in self.agents:
            agent.next_round(score_overall)

    def print_results(self) -> None:
        """
        Prints info about the results.
        """
        for i in range(len(self.results)):
            print(f"=============== # Round {i + 1} =============== ")
            print(" Initial awareness structure:")
            for structure in self.results[i][0]:
                for row in structure:
                    print(f"    {row}")
                print()

            print(" Awareness structures after intelligence/counterintelligence actions and calculation:")
            for structure in self.results[i][1]:
                for row in structure:
                    print(f"    {row}")
                print()

            print(" Outputs of each agent:")
            print(f" {self.results[i][2]}")

            print(" Overall round result:")
            print(f" {self.results[i][3]:.4f}")

            print(" Winner(s):")
            print(f" {self.results[i][4]}")
            print()
