import time
import matplotlib.pyplot as plt
def read_distribution(filename):
	with open(filename) as file:
		dist = file.read().split('\n')
		del dist[-1]
	return [[s for s in l ] for l in dist]

class Distribution():
	def __init__(self, filename):
		self.dist = read_distribution(filename)

	def __str__(self):
		return '\n'.join(["".join(r) for r in self.dist])

	def tilt_north(self):
		for i in range(len(self.dist)):
			for j in range(len(self.dist[0])):
				self.tilt_element((i,j), (i-1, j))
	def tilt_south(self):
		for i in reversed(range(len(self.dist))):
			for j in range(len(self.dist[0])):
				self.tilt_element((i,j), (i+1, j))
	def tilt_west(self):
		for i in range(len(self.dist)):
			for j in range(len(self.dist[0])):
				self.tilt_element((i,j), (i, j-1))
	def tilt_east(self):
		for i in range(len(self.dist)):
			for j in reversed(range(len(self.dist[0]))):
				self.tilt_element((i,j), (i, j+1))

	def tilt_element(self, old, new):
		if not (0 <= new[0] < len(self.dist) and 0 <= new[1] < len(self.dist[0])):
			return  
		if self.dist[old[0]][old[1]] != "O":
			return  
		if self.dist[new[0]][new[1]] == "#" or self.dist[new[0]][new[1]] == "O":
			return 

		self.dist[new[0]][new[1]], self.dist[old[0]][old[1]] = self.dist[old[0]][old[1]], self.dist[new[0]][new[1]]
		
		new_coords = (new[0] + new[0]-old[0], new[1] + new[1]-old[1])
		self.tilt_element(new, new_coords)

	def cycle(self):
		self.tilt_north()
		self.tilt_west()
		self.tilt_south()
		self.tilt_east()


	def calculate_load(self):
		total = 0
		for i in range(len(self.dist)):
			for j in range(len(self.dist[0])):
				if self.dist[i][j] == "O":
					total += (len(self.dist)-i)

		return total


def title_north(filename):
	d = Distribution(filename)
	d.tilt_north()
	return d.calculate_load()

def cycle(filename):
	d = Distribution(filename)
	seen, score = [str(d)], [d.calculate_load()]
	while True:
		d.cycle()
		if str(d) in seen:
			cycle_len = len(seen) - seen.index(str(d))
			start = seen.index(str(d))
			break 
		
		seen.append(str(d))
		score.append(d.calculate_load())

	return score[(1000000000-start)%(cycle_len)+start] 


print(title_north("Inputs/Day_14_Test.txt"))	
print(title_north("Inputs/Day_14_input.txt"))	

print(cycle("Inputs/Day_14_Test.txt"))
print(cycle("Inputs/Day_14_input.txt"))

