from typing import Type

class ScratchCard():
	def __init__(self, wn : list[str], n : list[str]) -> None:
		self.winning_numbers : set = {int(val) for val in wn} 
		self.numbers         : set = {int(val) for val in n} 

	def matching_numbers(self) -> int:
		return sum(1 for wn in self.winning_numbers if wn in self.numbers)

	def winnings(self) -> int:
		matching_numbers = self.matching_numbers()
		return 2**(matching_numbers-1) if matching_numbers > 0 else 0
		

def read_scratchcards(filename : str) -> list[Type[ScratchCard]]:
	scratchcards = []
	with open(filename, 'r') as file:
		for line in file.readlines():
			_, values = line.split(":")
			winning_numbers, numbers = values.split("|")
			winning_numbers, numbers = winning_numbers.split(), numbers.split()

			scratchcards.append(ScratchCard(winning_numbers, numbers))

	return scratchcards
		


def calculate_score(filename : str) -> int:
	scratchcards = read_scratchcards(filename)
	return sum(sc.winnings() for sc in scratchcards)


## Part 2 ##
## ------ ## 

def count_cards(filename : str) -> int:
	scratchcards = read_scratchcards(filename)
	scratchcards_count = [[sc, 1] for sc in scratchcards]

	for i, (sc, c) in enumerate(scratchcards_count):
		matching_numbers = sc.matching_numbers()
		for j in range(i+1, (i+1)+matching_numbers):	
			scratchcards_count[j][1] += c 

	return sum(sc_c[1] for sc_c in scratchcards_count)



print(calculate_score("Inputs/Day_4_Test.txt"))
print(calculate_score("Inputs/Day_4_input.txt"))

print(count_cards("Inputs/Day_4_Test.txt"))
print(count_cards("Inputs/Day_4_input.txt"))