from ultimatepy import Tournament, Timings
from datetime import datetime, timedelta


# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H", "Uni A 3", "Uni B 2",
              "Uni C 2", "Uni D 2"]
# Tournament timings stored within namedTuple
# Game/Day Variables
timings = Timings(group_game_length=timedelta(minutes=50),
                  game_length=timedelta(hours=1),
                  game_break=timedelta(minutes=5),
                  day1_start=datetime(year=1, month=1, day=1, hour=9),
                  day2_start=datetime(year=1, month=1, day=2, hour=9),
                  day1_end=datetime(year=1, month=1, day=1, hour = 17),
                  day2_end=datetime(year=1, month=1, day=2, hour = 17))

tournament = Tournament(team_input)
tournament.create_groups(group_size=4)
tournament.create_pitches(total_pitches=3)
tournament.set_timings(timings)

for group in tournament.groups.values():
    group.refreshGroup()
    print(group)

tournament.create_group_stage()

# tournament.assign_timings_to_schedule()
# print("Assign Timings to Schedule")


tournament.create_bracket()

tournament.print_schedule()

# todos
# todo bracket stage completion
# todo create a method which creates fixtures (returns the fixture object but allows Team.number_of_games
#  to be incremented etc
# todo create storage for group results
# todo ability to read in results from a csv file
