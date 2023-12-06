def read_schmatic(filename):
	engine_matrix = []
	with open(filename) as file:
		for line in file.readlines():

			engine_matrix.append(line[:-1])

	return engine_matrix

## Checking functions 
def check_number_left(i, j, schmatic):
	if j <0:
		return ""
	elif schmatic[i][j].isnumeric():
		return check_number_left(i, j-1, schmatic) + schmatic[i][j]
	else:
		return ""

def check_number_right(i, j, schmatic):
	if  j>=len(schmatic[0]):
		return ""
	elif schmatic[i][j].isnumeric():
		return schmatic[i][j] + check_number_right(i, j+1, schmatic)
	else:
		return ""

def to_int(string):
	if string == "":
		return 0
	else:
		return int(string)


def get_value(i,j, schmatic):
	if (not (0<= i < len(schmatic))) or not((0<= j < len(schmatic[0]))) or not(schmatic[i][j].isnumeric()):
		return 0
		
	return (check_number_left(i, j-1, schmatic) + schmatic[i][j] + check_number_right(i, j+1, schmatic))

	
	
def sum_dict(dictionary):
	return sum(sum(dictionary[key]) for key in dictionary) # Basically we just pass a generator to the sum funcion

def sum_ratio(dictionary):
	return sum(lst[0]*lst[1] for lst in dictionary.values() if len(lst) == 2)


def get_values_horizontal(i,j, schmatic):
	return [to_int(check_number_right(i, j+1, schmatic)), to_int(check_number_left(i, j-1, schmatic))]

def get_value_verticle(i,j,schmatic):
	value_above, value_below = to_int(get_value(i-1, j, schmatic)), to_int(get_value(i+1, j, schmatic))
	lst = [value_above, value_below]

	if not value_above:
		value_left, value_right = to_int(check_number_left(i-1,j-1, schmatic)), to_int(get_value(i-1, j+1, schmatic))
		lst.extend([value_left, value_right])	

	if not value_below:
		value_left, value_right = to_int(check_number_left(i+1,j-1, schmatic)), to_int(get_value(i+1, j+1, schmatic))
		lst.extend([value_left, value_right])

	return lst


def get_values(i, j, schmatic):
	if (schmatic[i][j].isnumeric() or schmatic[i][j] == '.'):
		return [] 

	lst = get_values_horizontal(i,j, schmatic)
	lst.extend(get_value_verticle(i,j,schmatic))

	return [v for v in lst if v != 0] # Gets ride of the zeros


def schmatic_mapping(filename):
	schmatic = read_schmatic(filename)
	char_dict = {}

	for i in range(len(schmatic)):
		for j in range(len(schmatic[i])):
			lst = get_values(i, j, schmatic)
			
			if lst:	
				char_dict[(i,j)] = lst
			
	return char_dict

def calculate_sum(filename):
	char_dict = schmatic_mapping(filename)
	return sum_dict(char_dict)

def calculate_ratios(filename):
	char_dict = schmatic_mapping(filename)
	schmatic = read_schmatic(filename)

	gear_dict = {key : char_dict[key] for key in char_dict if schmatic[key[0]][key[1]] == "*"}
	
	return sum_ratio(gear_dict)


print(calculate_sum("Inputs/Day_3_Test.txt"))
print(calculate_sum("Inputs/Day_3_Input.txt"))

print(calculate_ratios("Inputs/Day_3_Test.txt"))
print(calculate_ratios("Inputs/Day_3_Input.txt"))