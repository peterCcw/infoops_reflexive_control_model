import copy
from Agent import Agent


class Game:
    def __init__(self, agents_data_array, p, min_val, max_val):
        self.agents = [Agent(i, self, agents_data_array[i][0], agents_data_array[i][1], agents_data_array[i][2],
                             agents_data_array[i][3]) for i in
                       range(len(agents_data_array))]
        self.agents_ordered = self.agents.copy()
        self.agents_ordered.sort(key=lambda x: x.intel_level)
        self.p = p
        self.min_val = min_val
        self.max_val = max_val
        self.results = []

    def run_round(self):
        pre_intel_awareness_structures = [agent.awareness_structure for agent in self.agents]
        pre_intel_awareness_structures = copy.deepcopy(pre_intel_awareness_structures)
        post_intel_awareness_structures = [agent.awareness_structure for agent in self.agents]
        post_intel_awareness_structures = copy.deepcopy(post_intel_awareness_structures)
        output_numbers = [agent.calculate_output_value() for agent in self.agents_ordered]
        post_calc_awareness_structures = [agent.awareness_structure for agent in self.agents]
        post_calc_awareness_structures = copy.deepcopy(post_calc_awareness_structures)
        result = int(sum(output_numbers) / len(output_numbers))

        self.results.append([pre_intel_awareness_structures, post_intel_awareness_structures,
                             post_calc_awareness_structures, output_numbers, result])
        for agent in self.agents:
            agent.next_round(result)

    def print_results(self):
        for i in range(len(self.results)):
            print(f"#Round {i + 1}")
            print(" Awareness structures before intelligence actions:")
            for structure in self.results[i][0]:
                for row in structure:
                    print(f"    {row}")
                print()

            print(" Awareness structures after intelligence action:")
            for structure in self.results[i][1]:
                for row in structure:
                    print(f"    {row}")
                print()

            print(" Awareness structures after calculation:")
            for structure in self.results[i][2]:
                for row in structure:
                    print(f"    {row}")
                print()

            print(" Outputs of each agent:")
            print(f" {self.results[i][3]}")

            print(" Overall round result:")
            print(f" {self.results[i][4]}")

            print()




