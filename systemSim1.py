# SYSTEM SIMULATION 1
# DOCS:
#    https://axelrod.readthedocs.io/en/latest/index.html

import axelrod as axl
import random
import pprint
import matplotlib.pyplot as plt
# matplotlib inline

"""MAKE PLAYERS"""
# to transform player's strategies:
    # https://axelrod.readthedocs.io/en/latest/how-to/use_strategy_transformers.html

#PLAYERS
players = [s() for s in axl.basic_strategies] # create players
print(len(axl.players)) # count available players

# SET PLAYER ATTRIBUTES
attr = [i for i in range(len(players))] # attribute value for each player
# define method
def set_player_attr(players, attr):
    """Add attribute to player strategy classes to be accessable via self.attr"""
    for player, a in zip(players, attr):
        setattr(player, "attr", a)

set_player_attr(players, attr) # set attribute

# overwrite final_score_per_turn() to include attribute
class AttrBaseMatch(axl.Match):
"""Axelrod Match object with a modified final score function to enable attr to influence the final score as a multiplier"""
    def final_score_per_turn(self):
        base_scores = axl.Match.final_score_per_turn(self)
        return [player.attr * score for player, score in zip(self.players, base_scores)]

"""
The behavior of matches, and Moran processes can be more heavily influenced by
partially overwriting other match functions or birth and death functions within MoranProcess.
"""

"""RUN A MATCH"""
# CREATE MATCHES BETWEEN PLAYERS
players = (axl.Alternator(), axl.TitForTat())
match = axl.Match(players, turns=5, noise = 0.1) # set up match, result sroted in Match class
interactions = match.play() # overwrites the above Match class attribute

# visualize
print(match.sparklines()) # solid for cooperation, space for defection

#RESULTS
# interactions between players
print(interactions)
# individual scores for a Match
print(match.scores())
# final match scores
print(match.final_score())
# final score per Match
print(match.final_score_per_turn())
# winner of the Match
print(match.winner())
# count of cooperations per player
print(match.cooperation())
# count of cooperations per turn
print(match.normalised_cooperation())

"""RUN A TOURNAMENT"""
# same as Axelrod (1980)
# BUT THEIR CODE IS UNAVAILABLE AND WE GET DIFFERENT WINNERS
    # seed for reproducibility
    # 5 repetitions to smooth random effects

# create a tournament
tournament = axl.Tournament(players=players, turns=200, repetitions=5, seed=1) # pass filename = "tournamentInformation.csv" to save results to file

results = tournament.play() # play the tournament

# print ranked names
for name in results.ranked_names:
    print(name)

# SUMMARIZE RESULTS
summary = results.summarise() # summarize
pprint.pprint(summary) # print summary
results.write_summary('summary.csv') # write to csv

# TO ACCESS THESE RESULTS, VISIT:
    # https://axelrod.readthedocs.io/en/latest/how-to/access_tournament_results.html#tournament-results

# VISUALIZE
plot = axl.Plot(results) # set up plotting

#boxplot
p1 = plot.boxplot() # boxplot
p1.show # show plot

"""
# alter aspects of plot
>>> _, ax = plt.subplots()
>>> title = ax.set_title('Payoff')
>>> xlabel = ax.set_xlabel('Strategies')
>>> p = plot.boxplot(ax=ax)
>>> p.show()
"""

# distribution of wins
p2.plot.winplot()
p2.show

# payoff matrix
p3 = plot.payoff()
p3.show

# save all plots
save_all_plots

# EVOLUTIONARY SET UP
"""
MORAN PROCESS
Given an initial popu.ation of plahers, the population is itertedin rounds consisting of:
    - matches played between each pair of players, with the cumulative total scores recorded
    - a player is chosen to reproduce proportional to the player’s score in the round
    - a player is chosen at random to be replaced
The process proceeds in rounds until the population consists of a single player type. That type is declared the winner.
"""
# RUN MORAN PROCESS
# fitness function for determining parents to replicate
    #(Ohtsuki, 2006)
w = 0.95 # w denotes intensity of selection
fitness_transformation = lambda score: 1 - w + w * score
# nonzero mutation rate will cause Markov process to lack absorbing states
    # iterate with a loop to prevent this
mp = axl.MoranProcess(players, turns = 10, fitness_transformation=fitness_transformation, mutation_rate=0.1, seed=1) # make Moran process
# run in loop to prevent infinite number of trials
for _ in mp:
    if len(mp.population_distribution()) == 1:
        break
print(mp.population_distribution)

"""!! DO I NEED TO MOVE THE BELOW INTO THE ABOVE LOOP?"""
populations = mp.play() # run Moran process
print(mp.winning_strategy_name) # winning strategy

# ATTRIBUTES OF MORAN PROCESS
print(len(mp)) # number of rounds
print(pprint.pprint(populations)) # sequence of populations

# scores from each round
for row in mp.score_history:
    print([round(element, 1) for element in row])

# Plot
ax = mp.populations_plot() # make Moran process plot
plt.show # AX.SHOW? show plot

# HUMAN INTERACTION
