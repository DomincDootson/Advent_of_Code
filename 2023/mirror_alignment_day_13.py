import numpy as np 

def get_patterns(filename): # This can be tidied 
	with open(filename) as file:
		lines = file.read().split('\n\n')

	lines = [l.split('\n') for l in lines]

	del lines[-1][-1]
	for i, p in enumerate(lines):
		lines[i] = [[s for s in l] for l in p]

	return [np.array(p) for p in lines]


def count_differences(pattern, reflection_line, comparison_score) -> bool:  	
	comp_size = min(reflection_line+1, np.shape(pattern)[0]-1-reflection_line)
	upper, lower = pattern[reflection_line-comp_size+1:reflection_line+1, :], pattern[reflection_line+comp_size:reflection_line:-1,:,]

	total = 0
	for u_r, l_r in zip(upper, lower):
		for u, l in zip(u_r, l_r):
			total += 0 if u == l else 1

	return total == comparison_score


def check_reflections(pattern, comparison_score) -> int:
	for i in range(np.shape(pattern)[0]-1):
		if count_differences(pattern, i, comparison_score):
			return (i+1)
	return 0

def find_mirror(pattern, comparison_score) -> int:
	return check_reflections(pattern.transpose(), comparison_score) + 100 * check_reflections(pattern, comparison_score)

def find_mirrors(filename, comparison_score = 0) -> int:
	patterns = get_patterns(filename)
	return sum((find_mirror(p, comparison_score) for p in patterns))
	

print(find_mirrors("Inputs/Day_13_Test.txt"))
print(find_mirrors("Inputs/Day_13_input.txt"))

print(find_mirrors("Inputs/Day_13_Test.txt", 1))
print(find_mirrors("Inputs/Day_13_input.txt", 1))