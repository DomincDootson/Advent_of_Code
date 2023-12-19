def read_image(filename):
	
	with open(filename) as file:
		image = [[s for s in line if s != '\n'] for line in file.readlines()]

	return image

def expand_galaxy(image):
	rows, columns = [0] * len(image), [0] * len(image[0])

	for i in range(len(rows)):
		for j in range(len(image[0])):
			if image[i][j] == '#':
				rows[i], columns[j] = 1, 1

	return {i for i, v in enumerate(rows) if v == 0}, {i for i, v in enumerate(columns) if v == 0} 


def find_galaxies(image):
	coordinates = []
	for i in range(len(image)):
		for j in range(len(image[0])):
			if image[i][j] == '#':
				coordinates.append((i,j))

	return coordinates


def calculate_distance(coord1, coord2, empty_rows, empty_cols, expansion_factor = 1):
	min_row, max_row = min(coord1[0], coord2[0]), max(coord1[0], coord2[0])
	min_col, max_col = min(coord1[1], coord2[1]), max(coord1[1], coord2[1])
	extra = 0
	for e_r in empty_rows:
		if min_row < e_r < max_row:
			extra += 1

	for e_c in empty_cols:
		if min_col < e_c < max_col:
			extra += 1
	return (max_row-min_row) + (max_col-min_col) + extra * (expansion_factor-1)			
	
def calculate_distances(file, expansion_factor):
	image = read_image(file)
	empty_rows, empty_cols = expand_galaxy(image)
	coords = find_galaxies(image)
	
	
	total = 0
	for i in range(len(coords)):
		for j in range(i+1, len(coords)):
			total += calculate_distance(coords[i], coords[j], empty_rows, empty_cols, expansion_factor)

	return total
	


print(calculate_distances("Inputs/Day_11_Test.txt",2))
print(calculate_distances("Inputs/Day_11_input.txt",2))

print(calculate_distances("Inputs/Day_11_Test.txt",100))
print(calculate_distances("Inputs/Day_11_input.txt",10**6))


