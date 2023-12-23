from math import lcm

def parse_line(line):
	start, end = line.split("=")
	end = end[2:-1]
	end = end.split(',')
	if end[1][-1] == ')':
		end[1] = end[1][:-1]

	return start[:-1], (end[0], end[1][1:])

def open_map(filename):
	map = {}
	with open(filename, 'r') as file: 
		lines = file.readlines()
		steps = lines[0][:-1]

		for line in lines[2:]:
			start, end = parse_line(line)
			map[start] = end

	return steps, map

def calculate_steps(filename):
	steps, map = open_map(filename)
	count = 0
	position = "AAA" 
	while True:
		if position == "ZZZ":
			return count 

		left_or_right = 0 if steps[count%len(steps)] == 'L' else 1
		position = map[position][left_or_right]
		count += 1

def calculate_ghost_steps(filename):
	steps, map = open_map(filename)
	count = 0
	positions = [k for k in map.keys() if k[-1] == "A"]
	least_steps = [0] * len(positions)

	while 0 in least_steps:
		for i, node in enumerate(positions):
			if node.endswith("Z") and least_steps[i] == 0:
				least_steps[i] = count
		
		left_or_right = 0 if steps[count%len(steps)] == 'L' else 1
		for i, position in enumerate(positions):
			positions[i] = map[position][left_or_right]
		count += 1

	return lcm(*least_steps)
	


print(calculate_steps("Inputs/Day_8_Test.txt"))
print(calculate_steps("Inputs/Day_8_input.txt"))


print(calculate_ghost_steps("Inputs/Day_8_Test_2.txt"))
print(calculate_ghost_steps("Inputs/Day_8_input.txt"))