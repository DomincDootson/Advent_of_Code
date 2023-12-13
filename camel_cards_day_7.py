from collections import Counter
from abc import ABC, abstractmethod

class Hand(ABC):
	def __init__(self, hand : list[int], rank : list[int]) -> None:
		self.hand : list[int] = hand
		self.rank : list[int] = rank
		self.score : int = self.get_score(self.get_counter())
	
	def get_score(self, hand_counter : dict[int, int]) -> int:
		l = len(hand_counter)
		if  l ==1:
			return 7
		elif l==2:
			return 6 if max(hand_counter.values()) == 4 else 5
		elif l==3:
			return 4 if max(hand_counter.values()) == 3 else 3
		elif l==4:
			return 2
		else:
			return 1

	@abstractmethod
	def get_counter(self) -> dict[int, int]:
		pass

	def __repr__(self) -> str:
		return f"{self.hand} : {self.rank}"

	def __lt__(self, other) -> bool:
		if self.score == other.score:
			for s, o in zip(self.hand, other.hand):
				if s != o:
					return s < o

		return self.score < other.score

class NormalHand(Hand):
	"""docstring for NormalHand"""
	MAP = {**{f"{i}" : i for i in range(1,10)}, "T" : 10, "J" : 11, "Q" : 12, "K" : 13, "A" : 14}
	def __init__(self, hand, rank) -> None:
		Hand.__init__(self, [NormalHand.MAP[h] for h in hand], int(rank))

	def get_counter(self):
		return Counter(self.hand)
	
class JokerHand(Hand):
	"""docstring for JokerHand"""
	MAP = {**{f"{i}" : i for i in range(1,10)}, "T" : 10, "J" : 1, "Q" : 12, "K" : 13, "A" : 14}
	def __init__(self, hand, rank):
		Hand.__init__(self, [JokerHand.MAP[h] for h in hand], int(rank))

	def get_counter(self): 
		count = Counter(self.hand)
		n_jokers = count.get(1, 0) 
		
		if n_jokers == 5: return {1 : 5}
		if n_jokers != 0: del count[1]

		key_max = max(count.items(), key=lambda x: x[1])[0]
		count[key_max] += n_jokers
		return count		

## Functions ## 
def read_in_hands(filename : str) -> list[(list[int], int)]:
	hands = []
	with open(filename) as file:
		for line in file.readlines():
			hand, rank = line.split()
			hands.append((hand, rank))

	return hands

def standard_camel_cards(filename : str) -> int:
	hands = read_in_hands(filename)
	normal_hands = [NormalHand(h, r) for h, r in hands]
	normal_hands.sort()
	
	return sum(((i+1)*hand.rank for i, hand in enumerate(normal_hands)))

def joker_camel_cards(filename : str) -> int:
	hands = read_in_hands(filename)
	normal_hands = [JokerHand(h, r) for h, r in hands]
	normal_hands.sort()
	
	return sum(((i+1)*hand.rank for i, hand in enumerate(normal_hands)))

print(standard_camel_cards("Inputs/Day_7_Test.txt"))
print(standard_camel_cards("Inputs/Day_7_input.txt"))

print(joker_camel_cards("Inputs/Day_7_Test.txt"))
print(joker_camel_cards("Inputs/Day_7_input.txt"))