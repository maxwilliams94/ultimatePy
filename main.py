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
total_pitches = 1

tournament = Tournament(team_input)
tournament.create_groups(group_size= 4)
tournament.create_pitches(total_pitches=total_pitches)
tournament.set_timings(timings)

for group in tournament.groups.values():
    group.refreshGroup()
    print(group)

tournament.create_group_stage()

tournament.assign_timings_to_schedule()
print("Assign Timings to Schedule")
for i, ob in enumerate(tournament.schedule):
    print("{:4} {}".format(i+1, ob))


# todos
# todo schedule needs timings adding following group stage creation
# todo allow data input for match results
# todo create storage for group results
# todo printed schedule should show team seeds and group position
