import sys

from game import Game
from intel_actions import GetInfo, Disinform


class FileReader:
    """
    Provides file I/O interface.
    """
    def __init__(self, path):
        """
        :param path: str
        """
        self.path = path
        self.agents_array = []
        self.game = None

    def read_file_and_execute(self) -> None:
        """
        Reads file and executes game scenario. Results are saved into file 'input_file_name'_output.
        """
        with open(self.path) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i]
                # 1st line - preparing agent data array
                if i == 0:
                    agents_data_line = line
                    agents_data_line = [split for split in agents_data_line.split(';')]
                    agents_data_line.remove('\n')
                    self.agents_array = [x.split(',') for x in agents_data_line]
                    self.agents_array = [[int(data) for data in agent] for agent in self.agents_array]
                # 2nd line - initializing the game
                elif i == 1:
                    game_data_line = line
                    game_data_line = [split for split in game_data_line.split(';')]
                    game_data_line.remove('\n')
                    self.game = Game(self.agents_array, float(game_data_line[0]), int(game_data_line[1]),
                                     int(game_data_line[2]), float(game_data_line[3]))
                # Executing intel actions, run round etc.
                else:
                    action_data_line = line
                    action_data_line = [split for split in action_data_line.split(';')]

                    # Removing \n and EOF chars
                    if '\n' in action_data_line:
                        action_data_line.remove('\n')
                    if i == len(lines) - 1:
                        action_data_line = action_data_line[:-1]

                    # Appending get info intel action
                    if action_data_line[0] == 'getinfo':
                        attacker = self.game.agents[int(action_data_line[1])]
                        target = self.game.agents[int(action_data_line[2])]
                        reflexion_level = int(action_data_line[3])

                        if len(action_data_line) == 5:
                            id_getinfo_agent = int(action_data_line[4])
                        else:
                            id_getinfo_agent = None
                        self.game.intel_actions.append(GetInfo(attacker=attacker, target=target,
                                                               reflexion_level=reflexion_level,
                                                               id_getinfo_agent=id_getinfo_agent))
                    # Appending disinform intel action
                    elif action_data_line[0] == 'disinform':
                        attacker = self.game.agents[int(action_data_line[1])]
                        target = self.game.agents[int(action_data_line[2])]
                        reflexion_level = int(action_data_line[3])

                        ids_line = action_data_line[4].split(',')
                        ids_disinform_agent = [int(id_data) for id_data in ids_line]
                        self.game.intel_actions.append(Disinform(attacker=attacker, target=target,
                                                                 reflexion_level=reflexion_level,
                                                                 ids_disinform_agent=ids_disinform_agent))
                    # Running single round
                    elif action_data_line[0] == 'run':
                        self.game.run_round()

                    # Saving results to file
                    elif action_data_line[0] == 'results':
                        output_filename = f"output_{self.path.split('/')[-1]}"
                        with open(output_filename, 'w') as f_output:
                            original_stdout = sys.stdout
                            sys.stdout = f_output
                            self.game.print_results()
                            sys.stdout = original_stdout
