## Read in the data
END = "*"
def make_trie(*words):
	root = {}
	for word in words:
		current_dic = root
		for letter in word:
			current_dic = current_dic.setdefault(letter, {})
		current_dic["*"] = END 
	return root

def check_in_trie(string, trie, index):
	if END in trie:
		return index

	if index >= len(string) or (string[index] not in trie):
		return 0
	
	return check_in_trie(string, trie[string[index]], index+1)


def calculate_sum(filename):
	total = 0 
	with open(filename) as file:
		for line in file.readlines():
			total += get_numbers(line)
		
	return total



def get_numbers(line):
	l = 0
	numbers = []
	trie = make_trie("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
	mapping = {"zero" : 0, "one" : 1, "two" : 2, "three" : 3, "four" : 4, "five" : 5, "six" : 6, "seven" : 7, "eight" : 8, "nine" : 9}

	while l < len(line):
		index_skip = check_in_trie(line, trie, l)
		
		if line[l].isnumeric(): 
			numbers.append(int(line[l]))
			l += 1
		
		elif index_skip > 0: 
			numbers.append(mapping[line[l:index_skip]])
			l += 1
		else:
			l += 1
	
	return 10*numbers[0] + numbers[-1]
	
print(calculate_sum("Day_1_test.txt")) 
print(calculate_sum("Day_1_test_2.txt")) 
print(calculate_sum("Day_1_input.txt")) 