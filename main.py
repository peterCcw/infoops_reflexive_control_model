from file_reader import FileReader

# Scenario files must be in the same directory as main.py

reader = FileReader("example_scenarios/scenario1")
reader.read_file_and_execute()
#
# from game import Game
# from intel_actions import GetInfo, Disinform
# # # Scenario 1 - same reflexion, same initial values, reflexion = 3, no intel
# #
# agents_array = [[3, 3, 100], [3, 3, 100], [3, 4, 100]]
# g = Game(agents_array, (2/3), 0, 100)
# g.intel_actions.append(GetInfo(attacker=g.agents[0], target=g.agents[1], reflexion_level=3, id_getinfo_agent=0))
# g.intel_actions.append(GetInfo(attacker=g.agents[2], target=g.agents[0], reflexion_level=3, id_getinfo_agent=1))
# g.run_round()
# g.run_round()
# #g.run_round()
# #g.run_round()
# g.print_results()
#
#
# # scenario 2
# # # agents_array = [[3, 3, 3, 100], [3, 3, 2, 100], [3, 1, 4, 100]]
# # # g = Game(agents_array, (2/3), 0, 100)
# # # g.run_round()
# # # g.run_round()
# # # g.run_round()
# # # g.run_round()
# # # g.print_results()
#
# # # Scenario 3 - different reflexion, different initial values, no intel
# #
# # # agents_array = [[3, 1, 10, 90], [3, 3, 3, 80], [3, 3, 3, 75]]
# # # g = Game(agents_array, (2/3), 0, 100)
# # # g.run_round()
# # # g.run_round()
# # # g.run_round()
# # # g.run_round()
# # # g.print_results()