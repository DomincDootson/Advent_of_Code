from typing import Type
class Node():
	def __init__(self, values):
		if values[0]>values[1]:
			raise ValueError(f"In the range the first must be smaller than the second: {values}")
		self.range = values # Note that these values are inclusive
		

	def __getitem__(self, index):
		if index == 0 or index == 1:	
			return self.range[index]
		raise  ValueError("Node can only take index values 0 or 1")
	def __repr__(self):
		return str(self.range)

	def __lt__(self, other):
		return self.range[0] < other[0]




class Mapping():
	def __init__(self, values : list[str]):
		
		self.input_range = []
		self.output_range = []

		for line in values:
			output_start, input_start, length = [int(v) for v in line.split()]

			self.input_range.append((input_start, input_start+length-1))
			self.output_range.append((output_start, output_start+length-1))
		self.sort_by_input()

		self.fill_missing()

		

	def __str__(self):
		return f"Input  Range: {self.input_range}\nOutput Range: {self.output_range}"


	def sort_by_input(self):
		n = len(self.input_range) 
		for i in range(n):
			for j in range(n-(i+1)):
				if self.input_range[j][0] > self.input_range[j+1][0]:
					self.input_range[j], self.input_range[j+1] = self.input_range[j+1], self.input_range[j]
					self.output_range[j], self.output_range[j+1] = self.output_range[j+1], self.output_range[j]

	def fill_missing(self):
		self.sort_by_input()
		self.add_ends()
		for i in range(1,len(self.input_range)-1):
			if self.input_range[i+1][0]-self.input_range[i][1] > 1:
				missing = (self.input_range[i][1]+1,self.input_range[i+1][0]-1)
				self.input_range.append(missing)
				self.output_range.append(missing)
		self.sort_by_input()


	def add_ends(self):
		missing = (self.input_range[-1][1]+1, 10**20)		
		self.input_range.append(missing)
		self.output_range.append(missing)


		if self.input_range[0][0] > 0:
			missing = (0, self.input_range[0][0]-1)
			self.input_range.append(missing)
			self.output_range.append(missing)
		self.sort_by_input()
		
	# I need to sort the arries via the index of the input_range

	def map(self, in_numb : int) -> int:
		for i, in_range in enumerate(self.input_range):
			if in_range[0] <= in_numb <= in_range[1]:
				return self.output_range[i][0] + (in_numb - in_range[0])

		


	def map_range(self, node : Type[Node]) -> list[Type[Node]]:
		for i in range(len(self.input_range)):
			if self.input_range[i][0] <= node[0] <= self.input_range[i][1]:	
				break 
		output = []

		
		for j in range(i, len(self.input_range)):

			if self.input_range[j][0] <= node[1] <= self.input_range[j][1]:
				new_node = Node((self.map(max(self.input_range[j][0], node[0])), self.map(node[1])))
				output.append(new_node)
				return output
			else:
				new_node = Node((self.map(max(self.input_range[j][0], node[0])), self.output_range[j][1]))
				output.append(new_node)

		raise ValueError(f"Make the upper limit of the input_range larger. Current value: {self.input_range[j]}, Current Node: {node}")



## Read in functions ##
def read_maps(filename):
	maps, holding = [], []

	with open(filename) as file:
		lines  = file.readlines()
		_, seeds = (lines[0]).split(":")
		
		for line in lines[1:]:
			if line[0].isnumeric():
				holding.append(line[:-1])

			if line =='\n':
				maps.append(holding)
				holding = []

		maps.append(holding)

	return seeds.split(), maps[1:]

def read_maps_seeds(filename):
	seeds, maps = read_maps(filename)
	return [int(s) for s in seeds], [Mapping(m) for m in maps]

def list_mappings(seeds, maps):
	for m in maps:
		seeds = [m.map(s) for s in seeds]

	return min(seeds)
		

def single_seeds(filename):
	seeds, maps = read_maps_seeds(filename)
	return list_mappings(seeds, maps)




## Part II ##
## ------- ##

def read_maps_seeds_range(filename):
	seed_ranges, maps = read_maps(filename)
	seeds = []
	for start, length in zip(seed_ranges[::2], seed_ranges[1::2]):
		node = Node((int(start),int(start)+int(length)-1))
		seeds.append(node)

	return seeds, [Mapping(m) for m in maps]

## We need a function that will take the starting value and sucessively apply the range function 

def range_seeds(filename):
	seeds, maps = read_maps_seeds_range(filename)
	
	for m in maps:
		
		
		new_range = []
		for r in seeds:
			new_range.extend(m.map_range(r))

		seeds = new_range
		
		
	
	return min(seeds)
	
	

	

#93533455



print(single_seeds("Inputs/Day_5_input.txt"))
print(single_seeds("Inputs/Day_5_Test.txt"))

#print(range_seeds("Inputs/Day_5_input.txt"))
print(range_seeds("Inputs/Day_5_Test.txt"))