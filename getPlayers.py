import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, date
import pandas as pd
import numpy as np
import html5lib

# Note: this code was strongly borrowed from http://www.danielforsyth.me/exploring_nba_data_in_python/

gamesFile = './games.csv'
BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'

games =  pd.read_csv(gamesFile)

request = requests.get(BASE_URL.format(games['id'][0]))
print request.url
table = BeautifulSoup(request.text).find('table', class_='mod-data')
print table.prettify()
heads = table.find_all('thead')
headers = heads[0].find_all('tr')[1].find_all('th')[1:]
headers = [th.text for th in headers]
print headers

columns = ['id', 'team', 'player'] + headers

players = pd.DataFrame(columns=columns)

def get_players(players, team_name):
	array = np.zeros((len(players), len(headers)+1), dtype=object)
	array[:] = np.nan
	for i, player in enumerate(players):
		cols = player.find_all('td')
		print "#########################################################"
		# print cols[0].text
		# break
		array[i, 0] = cols[0].text.split(',')[0]
		print array[i, 0]
		for j in range(1, len(headers) + 1):
			if not cols[1].text.startswith('DNP'):
				array[i, j] = cols[j].text
				print cols[j].text
	print array
	print "9999999999999999999999999999999999999999999999999999"
	frame = pd.DataFrame(columns=columns)
	for x in array:
		print x
		line = np.concatenate(([index, team_name], x)).reshape(1,len(columns))
		new = pd.DataFrame(line, columns=frame.columns)
		frame = frame.append(new)
	return frame

for index, row in games[:10].iterrows():
# for index, row in games.iterrows():
    print(index)
    print row
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    request = requests.get(BASE_URL.format(row['id']))
    print request.url
    table = BeautifulSoup(request.text, 'html5lib').find('table', class_='mod-data')
    # print table.prettify()
    heads = table.find_all('thead')
    bodies = table.find_all('tbody')

    team_1 = heads[0].th.text
    print team_1
    team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
    team_1_players = get_players(team_1_players, team_1)
    print team_1_players
    players = players.append(team_1_players)
    
    team_2 = heads[3].th.text
    team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
    team_2_players = get_players(team_2_players, team_2)
    players = players.append(team_2_players)

players = players.set_index('id')
print(players)


