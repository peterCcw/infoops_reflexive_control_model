class Agent:
    def __init__(self, id_number, game, number_of_agents, reflexion_level=3, intel_level=3):
        self.id_number = id_number
        self.game = game
        self.number_of_agents = number_of_agents
        self.reflexion_level = reflexion_level
        self.intel_level = intel_level
        self.last_result = None
        self.awareness_structure = []
        self.fill_awareness_structure(-1)

    def fill_awareness_structure(self, value):
        awareness_structure = [[] for x in range(self.number_of_agents)]
        # 1st level of reflexion
        awareness_structure[self.id_number] = [value for x in range(self.number_of_agents)]
        if self.reflexion_level >= 2:
            # 2nd level of reflexion
            for i in range(self.number_of_agents):
                if i != self.id_number:
                    awareness_structure[i] = [[value for x in range(self.number_of_agents)] if i == y else []
                                              for y in range(self.number_of_agents)]
            if self.reflexion_level >= 3:
                # 3rd level of reflexion
                for i in range(self.number_of_agents):
                    if i != self.id_number:
                        for j in range(self.number_of_agents):
                            if j != i:
                                awareness_structure[i][j] = [value for x in range(self.number_of_agents)]
        self.awareness_structure = awareness_structure

    def modify_awareness_structure(self, agent_id, value):
        for i in range(self.number_of_agents):
            # 1st level of reflexion modification
            if i == self.id_number:
                self.awareness_structure[i][agent_id] = value
            else:
                if len(self.awareness_structure[i]) > 0:
                    for j in range(self.number_of_agents):
                        # 2nd level of reflexion modification
                        if j == i:
                            self.awareness_structure[i][j][agent_id] = value
                        else:
                            if len(self.awareness_structure[i][j]) > 0:
                                # 3rd level of reflexion modification
                                self.awareness_structure[i][j][agent_id] = value

    def get_awareness_info(self, agent_id, reflexion_level):
        for i in range(self.number_of_agents):
            # 1st level of reflexion modification
            if i == self.id_number:
                if reflexion_level == 1:
                    return self.awareness_structure[i][agent_id]
            else:
                if len(self.awareness_structure[i]) > 0:
                    for j in range(self.number_of_agents):
                        # 2nd level of reflexion modification
                        if j == i:
                            if reflexion_level == 2:
                                return self.awareness_structure[i][j][agent_id]
                        else:
                            if len(self.awareness_structure[i][j]) > 0:
                                # 3rd level of reflexion modification
                                if reflexion_level == 3:
                                    return self.awareness_structure[i][j][agent_id]

    def calculate_value(self, n, p, values, min_val, max_val):
        differences = [abs(((p * sum(values)) / (n - p)) - x) for x in range(min_val, max_val + 1)]
        return differences.index(min(differences))

    def calculate_output_value(self):
        N = self.number_of_agents
        p = self.game.p
        min_val = self.game.min_val
        max_val = self.game.max_val

        for i in range(self.number_of_agents):
            # 1st level of reflexion modification
            if i != self.id_number and len(self.awareness_structure[i]) > 0:
                if len(self.awareness_structure[i]) > 0:
                    for j in range(self.number_of_agents):
                        if j != i and len(self.awareness_structure[i][j]) > 0:
                            # 3rd level calculation
                            values = self.awareness_structure[i][j].copy()
                            values.pop(j)
                            calculated_value = self.calculate_value(N, p, values, min_val, max_val)
                            self.awareness_structure[i][j][j] = calculated_value
                            self.awareness_structure[i][i][j] = calculated_value
                    # 2nd level calculation
                    values = self.awareness_structure[i][i].copy()
                    values.pop(i)
                    calculated_value = self.calculate_value(N, p, values, min_val, max_val)
                    self.awareness_structure[i][i][i] = calculated_value
                    self.awareness_structure[self.id_number][i] = calculated_value
        # 1st level calculation
        values = self.awareness_structure[self.id_number].copy()
        values.pop(self.id_number)
        calculated_value = self.calculate_value(N, p, values, min_val, max_val)
        self.awareness_structure[self.id_number][self.id_number] = calculated_value
        return calculated_value

    def next_round(self, result_value):
        if self.last_result is None:
            self.last_result = result_value
            self.fill_awareness_structure(int(result_value / self.game.p))
        else:
            percentage_difference = ((result_value / self.game.p) - (self.last_result / self.game.p)) / \
                                    (self.last_result / self.game.p)
            self.last_result = result_value
            self.fill_awareness_structure(int(result_value * (percentage_difference + 1)))
