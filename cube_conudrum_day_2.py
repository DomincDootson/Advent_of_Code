def get_round(lst):
	round_lst = []

	for i, value in enumerate(lst):

		if value.isnumeric():
			start = i
			while lst[i].isnumeric():
				i += 1 

			round_lst.append((int(lst[start:i]), lst[i+1])) 

	round_lst.sort(key = lambda x: x[1])
	return round_lst

def get_games(file_name): # Each element in the list is a game 
	games = []
	with open(file_name) as file:
		
		for line in file.readlines():
			line_S = line.split(":")
			line_r = line_S[1].split(';')
			rounds = [get_round(r) for r in line_r] 
			

			games.append(rounds)	
			


	return games

def check_games(file_name):
	total = 0
	games = get_games(file_name)
	test_map = {'b' : 14, 'g' : 13, 'r' : 12}

	for i, game in enumerate(games):
		if check_game(game, test_map):
			total += (i+1)

	return total

def check_game(game, test_map): 
	for rund in game:
		for cube in rund:
			if cube[0] > test_map[cube[1]]:
				return False

	return True


def min_games(file_name):
	total = 0
	games = get_games(file_name)
	

	for game in games:
			total += min_game(game)

	return total

def min_game(game): 
	count = {'b' : 0, 'g': 0, 'r' : 0}
	for rund in game:
		for cube in rund:
			count[cube[1]] = max(cube[0], count[cube[1]])
			
	
	return count['b']*count['g']*count['r']






print(check_games("Inputs/Day_2_Test.txt"))
print(check_games("Inputs/Day_2_Input.txt"))


print(min_games("Inputs/Day_2_Test.txt"))
print(min_games("Inputs/Day_2_Input.txt"))
		

