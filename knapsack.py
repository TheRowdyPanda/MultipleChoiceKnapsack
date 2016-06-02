from collections import namedtuple
import pandas as pd
import csv

class Player():
    def __init__(self, position, name, salary, points, value):
        self.self = self
        self.position = position
        self.name = name
        self.salary = salary
        self.points = points
        self.value = value
        
    def __iter__(self):
        return iter(self.list)
    
    def __str__(self):
        return "{} {} {} {}".format(self.name,self.position,self.salary, self.points)


peeps = pd.read_csv("Fantasy_NBA.csv")
peepsNew = pd.read_csv("Fantasy_Better.csv")


players = [];
newPlayers = {};

for index, row in peepsNew.iterrows():
	pName = peepsNew['Name'][index]
	pScore = peepsNew['Points'][index]
	newPlayers[pName] = pScore;
	#dict = {pName:pScore};
	#newPlayers.append(dict);

print(newPlayers)

for index, row in peeps.iterrows():
	pName = peeps['Name'][index]
	pScore = peeps['AvgPointsPerGame'][index]
	pCost = peeps['Salary'][index]
	pPos = peeps['Position'][index]
	value = pScore/pCost;
	findNewScore = pScore;
	if pName in newPlayers:		
		findNewScore = newPlayers[pName];
	#findNewScore = [player for player in newPlayers if player[1] == pName];
	#findNewScore = findNewScore[1];
	player = Player(pPos, pName, pCost, findNewScore, value)
	players.append(player)


def points_knapsack(players):
    budget = 50000
    current_team_salary = 0
    constraints = {
        'PG':1,
        'SG':1,
	'GFlex':1,
        'SF':1,
        'PF':1,
        'FFlex':1,
        'C':1,
        'RFlex':1,
        }
    
    counts = {
        'PG':0,
        'SG':0,
	'GFlex':0,
        'SF':0,
        'PF':0,
        'FFlex':0,
        'C':0,
        'RFlex':0,
        }
    
    players.sort(key=lambda x: x.value, reverse=True)
    team = []
    
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if counts[pos] < constraints[pos] and current_team_salary + sal <= budget:
            team.append(player)
            counts[pos] = counts[pos] + 1
            current_team_salary += sal
            continue
        if counts['GFlex'] < constraints['GFlex'] and current_team_salary + sal <= budget and pos in ['PG','SG']:
            team.append(player)
            counts['GFlex'] = counts['GFlex'] + 1
            current_team_salary += sal 
        if counts['FFlex'] < constraints['FFlex'] and current_team_salary + sal <= budget and pos in ['PF','SF']:
            team.append(player)
            counts['FFlex'] = counts['FFlex'] + 1
            current_team_salary += sal 
        if counts['RFlex'] < constraints['RFlex'] and current_team_salary + sal <= budget and pos in ['PG','SG','SF','PF', 'C']:
            team.append(player)
            counts['RFlex'] = counts['RFlex'] + 1
            current_team_salary += sal 

    players.sort(key=lambda x: x.points, reverse=True)
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if player not in team:
            pos_players = [ x for x in team if x.position == pos]
            pos_players.sort(key=lambda x: x.points)
            for pos_player in pos_players:
                if (current_team_salary + sal - pos_player.salary) <= budget and pts > pos_player.points:
                    team[team.index(pos_player)] = player
                    current_team_salary = current_team_salary + sal - pos_player.salary
                    break
    return team

    return team




team = points_knapsack(players)
points = 0
salary = 0
for player in team:
    points += player.points
    salary += player.salary
    print player
print "\nPoints: {}".format(points)
print "Salary: {}".format(salary)
