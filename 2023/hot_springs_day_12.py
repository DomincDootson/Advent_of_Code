from functools import cache
# The solution takes inspo from https://github.com/fuglede/adventofcode/blob/master/2023/day12/solutions.py 
class Springs():
	
	def __init__(self, springs : str, combinations):
		
		self.springs = springs #[c for c in springs]
		self.combinations = tuple([int(c) for c in combinations.split(',')])

	def __repr__(self):
		return f"{self.springs} : {self.combinations}"

	def multiply(self):
		self.springs = ("?".join([self.springs]*5))
		self.combinations = self.combinations * 5
		
		

def read_in_springs(file):
	springs = []
	with open(file) as file:
		for line in file.readlines():
			s, c = line.split(" ")
			springs.append(Springs(s, c[:-1]))
	return springs


@cache
def num_solutions(s, sizes, num_done_in_group=0):
    if not s:
        return not sizes and not num_done_in_group
  
    num_sols = 0
    possible = [".", "#"] if s[0] == "?" else s[0]
    for c in possible:
        if c == "#":
            num_sols += num_solutions(s[1:], sizes, num_done_in_group + 1)
        else:
            if num_done_in_group:
                if sizes and sizes[0] == num_done_in_group:
                    num_sols += num_solutions(s[1:], sizes[1:])
            else:
                num_sols += num_solutions(s[1:], sizes)
    
    return num_sols


def number_solutions(filename):
	springs = read_in_springs(filename)
	return sum((num_solutions(s.springs + ".", s.combinations) for s in springs))

def number_solutions_pt2(filename):
	springs = read_in_springs(filename)
	for s in springs: s.multiply()


	return sum((num_solutions(s.springs + ".", s.combinations) for s in springs))

# Part 1
print(number_solutions("Inputs/Day_12_Test.txt"))
print(number_solutions("Inputs/Day_12_input.txt"))

print(number_solutions_pt2("Inputs/Day_12_Test.txt"))
print(number_solutions_pt2("Inputs/Day_12_input.txt"))
