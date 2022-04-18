from Agent import Agent


class Game:
    def __init__(self, agents_data_array, p, min_val, max_val):
        self.agents = [Agent(i, self, agents_data_array[i][0], agents_data_array[i][1]) for i in
                       range(len(agents_data_array))]
        self.p = p
        self.min_val = min_val
        self.max_val = max_val

