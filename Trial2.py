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
owned_simple = np.zeros(40)
game_landing = np.zeros((cycles,40)).astype(int)

# change all unbuyable positions to -1, so that they are not buyed
special_ones = [0,2,4,7,10,17,20,22,30,33,36,38]
for i in special_ones:
	# https://stackoverflow.com/a/28952971/5531122
	#game_owning[::,i] = -1
	owned_simple[i] = -1



# For each player: 0 - player number, 1 - position on board, 2 - turns in jail,
# 3 - free out of jail cards, 4 - passed Start count
all_players = np.zeros((players,5)).astype(int)

for i in range(players):
	all_players[i][0] = i+1
print(all_players)



cycle = 0
thrown_double = 0
while cycle < cycles:
	for i in range(players):
		print(all_players[i])
		thrown_double = 0

		while thrown_double < 4:
			move = throw_dice()
			print(move)
			#not in jail
			if all_players[i][2] == 0:
				all_players[i][1] += move[1]	

			# in jail
			elif all_players[i][2] > 0:
				# in jail and thrown double
				if move[0] == 1:
					all_players[i][1] += move[1]
					all_players[i][2] = 0
					#when going out of jail you don't throw twicealthough you had double
					move[0] = 0
					print('double - out of jail')
				else:
					# in jail, not thrown double, has a card
					if all_players[i][3] > 0:
						all_players[i][1] += move[1]
						all_players[i][3] -= 1
						all_players[i][2] = 0
					# in jail, not thrown double, has no card, less then 3 turns
					elif all_players[i][3] == 0 and all_players[i][2] < 3:
						all_players[i][2] += 1
						print('stuck in jail')
					# it's three turns, going out anyway
					else:
						all_players[i][1] += move[1]
						all_players[i][2] = 0
						print('out of jail')

			# if thrown double trice you end up in jail
			if move[0] == 0:
				thrown_double = 4
			else:
				thrown_double += 1
				move = throw_dice()
				if thrown_double == 3:
					all_players[i][1] = 30
					all_players[i][2] = 1
					game_landing[cycle][30] += 1
					thrown_double = 4
					print('three doubles - go to jail')

			if all_players[i][2] == 0:

				#passing Start
				if all_players[i][1] > 39:
					all_players[i][1] = all_players[i][1] - 40
					all_players[i][4] += 1

				print(all_players[i][1])
				game_landing[cycle][all_players[i][1]] += 1

				# landing on go to jail
				if all_players[i][1] == 10:
					all_players[i][1] = 30
					all_players[i][2] = 1
					game_landing[cycle][30] += 1
					thrown_double = 4
					print('go to jail')

				# take if free to buy - first 
				if owned_simple[all_players[i][1]] == 0:
					owned_simple[all_players[i][1]] = i+1
					game_owning[cycle][all_players[i][1]] = i+1
			print(all_players[i])
		print(all_players[i])

		print('-----------------')
	print('--------------------------------------------------')
	cycle += 1

print(owned_simple)
print('--------------------------------------------------')
print(game_owning)
print('--------------------------------------------------')
print(game_landing)
