import multiprocessing as mp
import numpy as np
import random

import os
import sys

import pandas as pd


cycles = 10

players = 2
casch = 2500
throws = 500


def throw_dice():
	dice1 = random.randint(1,6)
	dice2 = random.randint(1,6)

	if(dice1 ==dice2):
		return [1,dice1+dice2]
	else:
		return [0,dice1+dice2]




#board
game_owning = np.zeros((cycles,40)).astype(int)
game_landing = np.zeros((cycles,40)).astype(int)

# For each player 0 - number, 1 - position, 2 -  jail, 3 - passed Start
all_players = np.zeros((players,4)).astype(int)

for i in range(players):
	all_players[i][0] = i+1
print(all_players)

cycle = 0
while cycle < cycles:
	for i in range(players):
		print(all_players[i])
		move = throw_dice()
		print(move)
		
		#not in jail
		if all_players[i][2] ==  0:
			all_players[i][1] += move[1]
			

			#passing Start
			if all_players[i][1] > 39:
				all_players[i][1] = all_players[i][1] - 40
				all_players[i][3] += 1
				
			print(all_players[i][1])
			game_landing[cycle][all_players[i][1]] += 1
		
			if(game_owning[cycle][all_players[i][1]]) ==0:
				game_owning[cycle][all_players[i][1]] = i+1
			print(all_players[i])


		print('-----------------')
	print('--------------------------------------------------')
	cycle += 1
print(game_owning)
print('--------------------------------------------------')
print(game_landing)
