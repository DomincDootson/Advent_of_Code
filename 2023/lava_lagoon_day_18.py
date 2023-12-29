import sys
sys.setrecursionlimit(7000)


def get_dig_map(filename):
	with open(filename) as file:
		lines = file.read().split('\n')[:-1]

	return [(l.split()[0], int(l.split()[1]), l.split()[2][1:-1]) for l in lines]


def direction(orenentation):
	if orenentation == "R":
		return (1,0)
	elif orenentation == "L":
		return (-1,0)
	elif orenentation == "U":
		return (0,-1)
	else:
		return (0, 1)


def get_boundaries(paths):
	current_position = [0,0]
	boundaries = []
	for step in paths:
		for _ in range(step[1]):
			current_position = [c+d for c, d in zip(current_position, direction(step[0]))]
			
			boundaries.append(Edge(current_position, step[2]))

	return boundaries







def enclosed_volume(lst, i, j): # CALCULATE THE VOLUME USING AN INTERNAL SEARCH
	
	if lst[i][j] == "#":
		
		return 0

	if 0<=i<len(lst) and 0<=j<len(lst[0]) and lst[i][j] != "s":
		lst[i][j] = "s" 
		return 1 + enclosed_volume(lst, i-1, j) + enclosed_volume(lst, i, j-1) + enclosed_volume(lst, i+1, j) + enclosed_volume(lst, i, j+1) 

	return 0 


	

class Edge(object):
	"""docstring for Edge"""
	def __init__(self, coords, colour):
		self.coords = coords
		self.colour = colour

	def __repr__(self):
		return f"{self.coords}"

	def __lt__(self, other):
		if self.coords[1] == other.coords[1]:
			return self.coords[0] < other.coords[0]
		return self.coords[1] < other.coords[1]

class Map():
	"""docstring for Map"""
	def __init__(self, filename):
		self.instructions = get_dig_map(filename)
		self.boundaries = get_boundaries(get_dig_map(filename))
		self.boundaries.sort()

		self.m_max, self.n_max = max((e.coords[0] for e in self.boundaries))+1, max((e.coords[1] for e in self.boundaries))+1
		self.m_min, self.n_min = min((e.coords[0] for e in self.boundaries)), min((e.coords[1] for e in self.boundaries))

	
	def __str__(self):
		index = 0
		string = ""
		for j in range(self.n_min, self.n_max):
			
			for i in range(self.m_min, self.m_max):
				if index == (len(self.boundaries)):
					return string[:-1]
				
				if self.boundaries[index].coords == [i,j]:
					string += "#"
					index += 1
				else:
					string +="."
			
				
				
			string += '\n'
		return string[:-1]


	def print(self):
		print(str(self))
			

	def to_lst(self):
		lst = [[c for c in r] for r in str(self).split('\n')]


		if len(lst[-1]) < len(lst[0]):
			lst[-1].extend(["."]*(len(lst[0])-len(lst[-1])))

		return lst


	def calculate_volume(self):
		lst = self.to_lst()
		for j in range(len(lst[1])):
			if lst[1][j] == "#":
				break

		v = enclosed_volume(lst, 1, j+1)
		
		return v + len(self.boundaries)	
		
		
					
			
			

		 
		



dig_map = Map("Inputs/Day_18_Input.txt")
print(dig_map.calculate_volume())
# dig_map.to_lst()
# print(dig_map.calculate_volume())
# print(dig_map.m_max, dig_map.n_max)
# 		