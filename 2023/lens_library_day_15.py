from collections import defaultdict
def HASH_string(string):
	total  = 0
	for l in string:
		total += ord(l)
		total *= 17
		total %= 256 
	return total

class LabelledLens(object):
	def __init__(self, label, focal_length):
		self.label, self.focal_length = label, int(focal_length)

	def __eq__(self, other):
		return self.label == other.label

	def __repr__(self):
		return f"[{self.label} : {self.focal_length}]"
		
	def box(self):
		return HASH_string(self.label)

def read_instuctions(filename):
	with open(filename) as file:
		instructions = file.read()[:-1].split(',')
	return instructions

def sum_instuctions(filename):
	instructions = read_instuctions(filename)
	return sum((HASH_string(s) for s in instructions))

def add_to_box(instruction, boxes):	
	is_in = False
	labelled_lens = LabelledLens(*instruction.split("="))
	box = labelled_lens.box()

	for i, lens in enumerate(boxes[box]):
		if lens == labelled_lens:
			boxes[box][i] = labelled_lens
			is_in=True
	
	if not is_in:
		boxes[box].append(labelled_lens)

def remove_from_box(instruction, boxes):
	label = instruction[:-1]
	box = HASH_string(label)
	boxes[box] = [l for l in boxes[box] if label != l.label]


def generate_boxes(instructions):
	boxes = defaultdict(list)

	for instruction in instructions:
		if "=" in instruction:
			add_to_box(instruction, boxes)
		else:
			remove_from_box(instruction, boxes)		
	
	return boxes


def focal_length_box(lst):
	return sum(((i+1)*lens.focal_length for i, lens in enumerate(lst)))

def focal_length_sum(boxes):
	return sum(((1+box)*focal_length_box(lst) for box, lst in boxes.items()))

def calculate_focal_length(filename):
	instructions = read_instuctions(filename)
	boxes = generate_boxes(instructions)
	return focal_length_sum(boxes)

	
	
print(sum_instuctions("Inputs/Day_15_Test.txt"))
print(sum_instuctions("Inputs/Day_15_input.txt"))

print(calculate_focal_length("Inputs/Day_15_Test.txt"))
print(calculate_focal_length("Inputs/Day_15_input.txt"))