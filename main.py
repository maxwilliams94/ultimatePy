from ultimatepy import Tournament, Timings
from datetime import datetime, timedelta


# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]
# Tournament timings stored within namedTuple
# Game/Day Variables
timings = Timings(game_length=timedelta(hours=1),
                  game_break=timedelta(minutes=5),
                  day_start=datetime(year=1, month=1, day=1, hour=9),
                  day_length=timedelta(hours=8))
total_pitches = 1

tournament = Tournament(team_input)
tournament.create_groups(group_size= 4)
tournament.create_pitches(total_pitches=total_pitches)

for group in tournament.groups.values():
    group.refreshGroup()
    print(group)

tournament.create_group_stage()
print("Created Group Stage")
for i, ob in enumerate(tournament.schedule):
    print(i, ob)


# todos
# todo schedule needs timings adding following group stage creation
# todo allow data input for match results
# todo create storage for group results
