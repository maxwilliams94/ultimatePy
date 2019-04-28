from ultimatepy import Tournament, Timings
from datetime import datetime, timedelta


# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]
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
tournament.create_pitches(total_pitches=2)
tournament.set_timings(timings)

for group in tournament.groups.values():
    group.refreshGroup()
    print(group)

tournament.create_group_stage()

# tournament.assign_timings_to_schedule()
# print("Assign Timings to Schedule")

tournament.print_schedule()


# todos
# todo create a method which creates fixtures (returns the fixture object but allows Team.number_of_games
#  to be incremented etc
# todo recreate str overides for classes. when a class needs to be printed within
#  another class, print specific attributes of it instead of the entire class which will cause errors
# todo create storage for group results
