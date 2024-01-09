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

def get_boundaries(filename):
	paths = get_dig_map(filename)
	current_position = [0,0]
	boundaries = []
	for step in paths:
		current_position = [c+step[1]*d for c, d in zip(current_position, direction(step[0]))]
		boundaries.append(Edge(current_position, step[1], step[2]))

	return boundaries

def get_boundaries_hex(filename):
	paths = get_dig_map(filename)
	current_position = [0,0]
	boundaries = []
	conversion = {0 : "R", 1 : "D", 2 : "L", 3 : "U"}
	for step in paths:
		size, d = int(step[2][1:-1], 16), conversion[int(step[2][-1])]
		
		current_position = [c+size*d for c, d in zip(current_position, direction(d))]
		boundaries.append(Edge(current_position, size, step[2]))

	return boundaries




def get_area(boundaries):
	area = abs(sum((boundaries[i].coords[0]*(-boundaries[(i+1)%len(boundaries)].coords[1]+ boundaries[(i-1)%len(boundaries)].coords[1]) for i in range(len(boundaries)))))//2
	boundary = sum((b.length for b in boundaries))
	
	i = area - boundary//2 +1
	return i+boundary


class Edge(object):
	"""docstring for Edge"""
	def __init__(self, coords, length, colour):
		self.coords = coords
		self.length = length
		self.colour = colour

	def __repr__(self):
		return f"{self.coords}"

	def __lt__(self, other):
		if self.coords[1] == other.coords[1]:
			return self.coords[0] < other.coords[0]
		return self.coords[1] < other.coords[1]

def find_area(filename):
	dig_map = get_boundaries(filename)
	return get_area(dig_map)

def find_area_hex(filename):
	dig_map = get_boundaries_hex(filename)
	return get_area(dig_map)

print(find_area("Inputs/Day_18_Test.txt"))
print(find_area("Inputs/Day_18_input.txt"))

print(find_area_hex("Inputs/Day_18_Test.txt"))
print(find_area_hex("Inputs/Day_18_Input.txt"))