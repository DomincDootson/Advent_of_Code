from math import sqrt

def read_in_races(filename : str):	
	with open(filename) as file:
		times, distances = file.readlines()
	
	times, distances = times.split(":")[1], distances.split(":")[1]
	times, distances = times.split(), distances.split()
	return [int(t) for t in times], [int(d) for d in distances]


def n_solutions(time : int, distance : int) -> int:
	if time**2 < 4*distance:
		raise ValueError(f"Determinate of quadratic is negative, time: {time}, distance: {distance}")
	lower, upper = int(1+(time -sqrt(time**2 - 4*distance))/(2)), int((time +sqrt(time**2 - 4*distance))/(2))
	return upper-lower+1


def total_number_winning_way(filename : str) -> int:
	times, distances = read_in_races(filename)
	total = 1
	for t, d in zip(times, distances):
		total *= n_solutions(t,d)

	return total

def total_number_winning_way_pt2(filename : str) -> int:
	times, distances = read_in_races(filename)
	t, d = "".join([str(t) for t in times]), "".join([str(t) for t in distances])
	
	return n_solutions(int(t),int(d))



if __name__ == "__main__":
	print(total_number_winning_way("Inputs/Day_6_Test.txt"))
	print(total_number_winning_way("Inputs/Day_6_input.txt"))


	print(total_number_winning_way_pt2("Inputs/Day_6_Test.txt"))
	print(total_number_winning_way_pt2("Inputs/Day_6_input.txt"))





