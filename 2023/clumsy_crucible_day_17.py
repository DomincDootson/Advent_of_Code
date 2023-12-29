from queue import PriorityQueue

def read_in_grid(filename):
	with open(filename) as file:
		lines = file.read()[:-1]

	return [[int(c) for c in line] for line in lines.split('\n')]


class Path():
	"""docstring for Path"""
	def __init__(self, hl, index, direction, n_dir):
		self.heat_loss = hl 
		self.index = index
		self.direction = direction
		self.n_direction = n_dir

	def __repr__(self):
		return f"{self.heat_loss} : {self.index} : {self.direction}"
	def __lt__(self, other):
		return self.heat_loss < other.heat_loss

	def hash(self):
		return (self.index, self.direction, self.n_direction)

	def is_on_grid(self, n, m):
		return 0<= self.index[0] < n and 0<=self.index[1] < m

	def step(self):
		self.index = (self.index[0]+self.direction[0], self.index[1] + self.direction[1])


class Grid():

	def __init__(self, filename, min_direction, max_direction):
		self.grid = read_in_grid(filename)
		self.n, self.m  = len(self.grid), len(self.grid[0])

		self.seen = set()
		self.paths = PriorityQueue()
		self.paths.put(Path(0, (0,0), (1,0), 1))
		self.paths.put(Path(0, (0,0), (0,1), 1))

		self.min_direction, self.max_direction = min_direction, max_direction


	def find_shorest_path(self):
		while self.paths:
			shortest_path = self.paths.get()
			shortest_path.step()
			if (not shortest_path.is_on_grid(self.n, self.m)) or (shortest_path.hash() in self.seen): # Checks if the path is okay
				continue
			else:
				self.seen.add(shortest_path.hash())
				
			i, j = shortest_path.index 
			shortest_path.heat_loss += self.grid[i][j]

			if (i == self.n-1) and (j == self.m-1) and (shortest_path.n_direction >= self.min_direction):	
				return shortest_path.heat_loss

			if shortest_path.n_direction >= self.min_direction:
				self.paths.put(Path(shortest_path.heat_loss, shortest_path.index, (shortest_path.direction[1],   shortest_path.direction[0]), 1))
				self.paths.put(Path(shortest_path.heat_loss, shortest_path.index, (-shortest_path.direction[1], -shortest_path.direction[0]), 1))

			if shortest_path.n_direction < (self.max_direction):
				self.paths.put(Path(shortest_path.heat_loss, shortest_path.index, (shortest_path.direction[0],   shortest_path.direction[1]), shortest_path.n_direction+1))



			


def find_shorest_path(filename, min_direction = 0, max_direction = 3):
	grid = Grid(filename, min_direction, max_direction)
	return grid.find_shorest_path()
	


print(find_shorest_path("Inputs/Day_17_Test.txt"))
print(find_shorest_path("Inputs/Day_17_input.txt"))

print(find_shorest_path("Inputs/Day_17_Test.txt", min_direction = 4, max_direction = 10))
print(find_shorest_path("Inputs/Day_17_input.txt", min_direction = 4, max_direction = 10))
