def read_values(filename):
	with open(filename) as file: sequences = [[int(v) for v in line.split()] for line in file.readlines()]
	return sequences

def all_zeros(sequence):
	return len(set(sequence)) == 1 and sequence[0] == 0

def make_prediction_forwards(sequence):
	if all_zeros(sequence): return 0
	return sequence[-1] + make_prediction_forwards([f - b for f, b in zip(sequence[1:], sequence)])

def make_predictions_forwards(filename):
	sequences = read_values(filename)
	return sum((make_prediction_forwards(seq) for seq in sequences))

def make_prediction_backwards(sequence):
	if all_zeros(sequence): return 0
	return sequence[0] - make_prediction_backwards([f - b for f, b in zip(sequence[1:], sequence)])

def make_predictions_backwards(filename):
	sequences = read_values(filename)
	return sum((make_prediction_backwards(seq) for seq in sequences))

print(make_predictions_forwards("Inputs/Day_9_Test.txt"))
print(make_predictions_forwards("Inputs/Day_9_input.txt"))

print(make_predictions_backwards("Inputs/Day_9_Test.txt"))
print(make_predictions_backwards("Inputs/Day_9_input.txt"))
