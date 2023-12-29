from collections import defaultdict

def read_in_grid(filename):
	with open(filename) as file:
		lines = file.read()[:-1]

	return [[c for c in line] for line in lines.split('\n')]


class Ray():
	def __init__(self, coords, direction):
		self.coords = coords
		self.direction = direction

	def __repr__(self):
		return f"{self.coords} : {self.direction}"

	def move(self):
		self.coords = (self.coords[0] +self.direction[0], self.coords[1] +self.direction[1])
	
	def is_on_grid(self, n, m):
		return 0<= self.coords[0] < n and 0<=self.coords[1] < m

	def coords_index(self):
		return self.coords[1], self.coords[0]
		

class Grid():
	def __init__(self, filename, ray = Ray((0,0), (1,0))):
		self.grid = read_in_grid(filename)
		self.n, self.m = len(self.grid), len(self.grid[0])
		self.visited = defaultdict(list)

		self.rays = [ray]

	def evolve_rays(self):
		while len(self.rays) > 0:  
			self.update_directions() 
			self.move_rays()
			self.remove_off_grid() # Checks if they are on the grid
			self.update_visted()

	def visited_squares(self):
		self.evolve_rays()
		return len(self.visited)

	def remove_off_grid(self):
		self.rays = [r for r in self.rays if r.is_on_grid(self.n, self.m)]

	def update_visted(self):
		self.rays = [r for r in self.rays if r.direction not in self.visited[r.coords]]

		for r in self.rays:
			self.visited[r.coords].append(r.direction)

	def update_directions(self):
		new_rays = []
		for r in self.rays:
			i, j = r.coords_index()
			symbol = self.grid[i][j]

			if symbol == '\\':
				
				r.direction = (r.direction[1], r.direction[0]) 
			elif symbol == '/':
				r.direction = (-r.direction[1], -r.direction[0]) 
			elif symbol == '-' and r.direction[0] == 0:
				r.direction = (1,0)
				new_rays.append(Ray(r.coords, (-1,0)))
			elif symbol == '|' and r.direction[1] == 0:
				r.direction = (0,1)
				new_rays.append(Ray(r.coords, (0,-1)))

		self.rays.extend(new_rays)
			

	def move_rays(self):
		for r in self.rays:
			r.move()

	def print_visited(self):
		for i in range(self.n):
			string = ""
			for j in range(self.m):
				if (j,i) in self.visited:
					string += "#"
				else:
					string += "."
			print(string)


			
def n_energised_squares(filename):
	grid = Grid(filename)	
	return grid.visited_squares()

def find_optimal_start(filename):
	grid = Grid(filename)
	n,m = grid.n, grid.m

	max_value = 0
	
	for i in range(n):
		gl = Grid(filename, Ray((0, i), (1,0)))
		gr = Grid(filename, Ray((m-1, i), (-1,0)))
		max_value = max([max_value, gr.visited_squares(), gl.visited_squares()])

	for j in range(m):
		gl = Grid(filename, Ray((j, 0), (0, 1)))
		gr = Grid(filename, Ray((j, n-1,), (0,-1)))
		max_value = max([max_value, gr.visited_squares(), gl.visited_squares()])

	return max_value

print(n_energised_squares("Inputs/Day_16_Test.txt"))
print(n_energised_squares("Inputs/Day_16_input.txt"))

print(find_optimal_start("Inputs/Day_16_Test.txt"))
print(find_optimal_start("Inputs/Day_16_input.txt"))

