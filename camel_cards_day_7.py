from collections import Counter
MAP       = {**{f"{i}" : i for i in range(1,10)}, "T" : 10, "J" : 11, "Q" : 12, "K" : 13, "A" : 14}
MAP_JOKER = {**{f"{i}" : i for i in range(1,10)}, "T" : 10, "J" : 1, "Q" : 12, "K" : 13, "A" : 14}


## Testing Functions 
def hand_score(hand):
	count = Counter(hand)
	l = len(count)
	
	if  l ==1:
		return 7
	elif l==2:
		return 6 if max(count.values()) == 4 else 5
	elif l==3:
		return 4 if max(count.values()) == 3 else 3
	elif l==4:
		return 2
	else:
		return 1

def hand_score_joker(hand):
	count = Counter(hand)
	n_jokers = count.get(1, 0) 
	if n_jokers == 5: # This is for the case when we have 5J 
		return 7
	
	if n_jokers != 0: del count[1]
	

	key_max = max(count.items(), key=lambda x: x[1])[0]
	count[key_max] += n_jokers
	

	new_hand = []

	for d in count.items():
		new_hand.extend(d[1]*[d[0]])

	return hand_score(new_hand)


class Hand():
	
	def __init__(self, hand, rank, joker = False):
		if joker:
			self.hand = [MAP_JOKER[h] for h in hand]
			self.score = hand_score_joker(self.hand)

		else:
			self.hand = [MAP[h] for h in hand]
			self.score = hand_score(self.hand)
		

		self.rank = int(rank)

		

	def __repr__(self):
		return f"{self.hand} : {self.rank}"

	def __lt__(self, other):
		if self.score == other.score:
			for s, o in zip(self.hand, other.hand):
				if s != o:
					return s < o

		
		return self.score < other.score


def read_in_hands(filename, joker):
	hands = []
	with open(filename) as file:
		for line in file.readlines():
			hand, rank = line.split()
			hands.append(Hand(hand, rank, joker))

	
	return hands


def calculate_winnings(filename):
	hands = read_in_hands(filename, False)
	hands.sort()
	
	return sum(((i+1)*hand.rank for i, hand in enumerate(hands)))


def calculate_winnings_joker(filename):
	hands = read_in_hands(filename, True)

	hands.sort()
	return sum(((i+1)*hand.rank for i, hand in enumerate(hands)))



print(calculate_winnings("Inputs/Day_7_Test.txt"))
print(calculate_winnings("Inputs/Day_7_input.txt"))

print(calculate_winnings_joker("Inputs/Day_7_Test.txt"))
print(calculate_winnings_joker("Inputs/Day_7_input.txt"))



