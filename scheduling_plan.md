# Proposed structure for adding group games (or games in general to the schedule
## Current Implimentation
- Create a cycled iterator of possible group seed match ups
- Cycle though these match ups and schedule them provided that a there is no double booking of teams

## Proposed Implimentation
- Create a non-cycled iterator for possible group seed match ups (or just a list)
- Store these match ups within a list for each group
- Iterate through this list (dictionary of lists))
- - As each fixture is added to the schedule (pop), assess priority of remaining fixtures
- - Add the highest priority of remaining fixtures each iteration

