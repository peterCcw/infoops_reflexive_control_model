from typing import List


class Agent:
    """
    Represents agent - player of p-beauty game contest.
    """

    def __init__(self, id_number: int, game, number_of_agents: int,
                 reflexion_level: int = 3, intel_level: int = 3, initial_value: int = -1):
        """
        :param id_number: int
        :param game: Game
        :param number_of_agents: int
        :param reflexion_level: int
        :param intel_level: int
        :param initial_value: int
        """
        self.id_number = id_number
        self.game = game
        self.number_of_agents = number_of_agents
        self.reflexion_level = reflexion_level
        self.intel_level = intel_level
        self.last_result = None
        self.awareness_structure = []
        self.fill_awareness_structure(initial_value)

    def fill_awareness_structure(self, value: int) -> None:
        """
        Sets every cell of awareness structure to given value.
        :param value: int
        """
        awareness_structure = [[] for _ in range(self.number_of_agents)]
        # 1st level of reflexion
        awareness_structure[self.id_number] = [value for _ in range(self.number_of_agents)]
        if self.reflexion_level >= 2:
            # 2nd level of reflexion
            for i in range(self.number_of_agents):
                if i != self.id_number:
                    awareness_structure[i] = [[value for _ in range(self.number_of_agents)] if i == y else []
                                              for y in range(self.number_of_agents)]
            if self.reflexion_level >= 3:
                # 3rd level of reflexion
                for i in range(self.number_of_agents):
                    if i != self.id_number:
                        for j in range(self.number_of_agents):
                            if j != i:
                                awareness_structure[i][j] = [value for _ in range(self.number_of_agents)]

        self.awareness_structure = awareness_structure

    def modify_awareness_structure(self, reflexion_level: int = 1, ids: List[int] = None, values: List[int] = None) -> \
            None:
        """
        Modifies awareness structure on given reflexion level with given value. Ids are used for reflexion levels 2 and
        3, they specify witch part of awareness structure should be changed. Values must be given as a List of int of
        length equal to number of agents in the game. If reflexion level of agent is lower than given parameter, nothing
        happens.
        :param reflexion_level: int
        :param ids: List[int]
        :param values: List[int]
        """
        if ids is None:
            ids = []
        if values is None:
            values = []

        values = [self.check_max_value(val) for val in values]

        if reflexion_level == 1:
            self.awareness_structure[self.id_number][ids[0]] = values
        elif reflexion_level == 2 and len(self.awareness_structure[ids[0]][ids[0]]) > 0:
            self.awareness_structure[ids[0]][ids[0]] = values
        elif reflexion_level == 3 and len(self.awareness_structure[ids[0]][ids[1]]) > 0:
            self.awareness_structure[ids[0]][ids[1]] = values

    def get_awareness_info(self, reflexion_level: int = 1, ids: List[int] = None) -> List[int]:
        """
        Returns awareness structure specified by given reflexion level and ids. If reflexion level of agent is lower
        than given parameter, None is returned.
        :param reflexion_level: int
        :param ids: List[int]
        :return: List[int] or None
        """
        if ids is None:
            ids = []

        if reflexion_level == 1:
            output = self.awareness_structure[self.id_number]
        elif reflexion_level == 2 and reflexion_level <= self.reflexion_level:
            output = self.awareness_structure[ids[0]][ids[0]]
        elif reflexion_level == 3 and reflexion_level == self.reflexion_level:
            output = self.awareness_structure[ids[0]][ids[1]]
        else:
            output = None

        return output

    def modify_after_disinform(self, reflexion_level: int, values: List[int], target_id: int, ids: List[int]) -> None:
        """
        Modifies single value in self awareness structure after disinforming other agent.
        :param reflexion_level: int
        :param values: List[int]
        :param target_id: int
        :param ids: List[int]
        """
        N = self.number_of_agents
        p = self.game.p
        min_val = self.game.min_val
        max_val = self.game.max_val

        values = values.copy()
        if reflexion_level == 1:
            for i in range(len(values)):
                if i != ids[0]:
                    # Calculating value with same assumptions as in calculate_value method
                    value = int(values[i] * (N - p) / (p * (N - 1)))
                    value = self.check_max_value(value)
                    self.awareness_structure[ids[0]][i] = [value for i in range(self.number_of_agents)]

        # For reflexion level == 2
        else:
            values.pop(ids[1])
            value = self.calculate_value(N, p, values, min_val, max_val)
            value = self.check_max_value(value)
            self.awareness_structure[target_id][ids[0]][ids[1]] = value

    def check_max_value(self, value: int) -> int:
        """
        Checks if given value is not greater than max value allowed in the game.
        :param value: int
        :return: int
        """
        if value > self.game.max_val:
            return self.game.max_val
        else:
            return value

    def calculate_value(self, N: int, p: int, values: List[int], min_val: int, max_val: int) -> int:
        """
        Calculates value of guess basing on given game parameters and values of other agent's guesses.
        :param N: int
        :param p: int
        :param values: List[int]
        :param min_val: int
        :param max_val: int
        :return: int
        """
        differences = [abs(((p * sum(values)) / (N - p)) - x) for x in range(min_val, max_val + 1)]
        return differences.index(min(differences))

    def calculate_guess_value(self):
        """
        Calculate final guess starting with the highest reflexion levels and going up to top.
        :return: int
        """
        N = self.number_of_agents
        p = self.game.p
        min_val = self.game.min_val
        max_val = self.game.max_val

        for i in range(self.number_of_agents):
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
        """
        Prepares agent for next round. Refills awareness structure basing on given result and previous results. After
        first round fills awareness structure with mean guess (assumes that every agent gave same guess), then
        calculates percentage difference.
        :param result_value: int
        """
        if self.last_result is None:  # Case after 1st round
            self.last_result = result_value
            self.fill_awareness_structure(int(result_value / self.game.p))
        else:  # Case after 2nd round and the following
            if self.last_result == 0:
                self.fill_awareness_structure(0)
            else:
                percentage_difference = ((result_value / self.game.p) - (self.last_result / self.game.p)) / \
                                        (self.last_result / self.game.p)
                self.last_result = result_value
                self.fill_awareness_structure(int(result_value * (percentage_difference + 1)))
