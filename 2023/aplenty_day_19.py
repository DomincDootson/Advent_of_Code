from typing import Tuple
from dataclasses import dataclass, asdict
from operator import lt, gt

@dataclass(slots = True)
class Part:
	x : int
	m : int  
	a : int
	s : int 

	def add_values(self):
		return self.x + self.m + self.a + self.s

@dataclass(slots = True)
class PartRange:
	x : tuple[int, int] = (1, 4000)
	m : tuple[int, int] = (1, 4000)
	a : tuple[int, int] = (1, 4000)
	s : tuple[int, int] = (1, 4000)

	def n_values(self):
		return (self.x[1]-self.x[0]+1) * (self.m[1]-self.m[0]+1) * (self.a[1]-self.a[0]+1) * (self.s[1]-self.s[0]+1)

class Step():
	def __init__(self, string):
		comparison, self.target = string.split(":")
		if "<" in comparison:
			self.var, self.value = comparison.split("<")
			self.comparison = lt 
		else:
			self.var, self.value = comparison.split(">")
			self.comparison = gt 
		
		self.value = int(self.value)
	

	def __repr__(self):
		return f"{self.var} {self.comparison} {self.value} --> {self.target}"

	def check(self, part) -> bool:
		return  self.comparison(getattr(part, self.var), self.value) 


	def split(self, part_range): # The first one will be the one that satisfies the condition 
		copy_values_true, copy_values_false = asdict(part_range), asdict(part_range)
		
		if self.comparison == lt:
			copy_values_true[self.var], copy_values_false[self.var] = (copy_values_true[self.var][0], self.value-1), (self.value, copy_values_true[self.var][1])
		else:
			copy_values_true[self.var], copy_values_false[self.var] = (self.value+1, copy_values_true[self.var][1]), (copy_values_true[self.var][0], self.value)
		
		part_range_true, part_range_false = PartRange(**copy_values_true), PartRange(**copy_values_false)
		return part_range_true, part_range_false


class Workflow():
	def __init__(self, name, steps, terminal):
		self.name = name
		self.steps = steps
		self.terminal = terminal

	def check(self, part):
		for step in self.steps: 
			if step.check(part):
				return step.target
		return self.terminal

	def check_ranges(self, part_range):
		to_check = []
		for step in self.steps:
			true_range, part_range = step.split(part_range)
			to_check.append((true_range, step.target))

		to_check.append((part_range, self.terminal))
		return to_check
		
class Workflows(object):
	def __init__(self, workflows):
		self.workflows = {wf.name : wf for wf in workflows}

	def check(self, part):
		workflow = 'in'
		while workflow != 'A' and workflow != 'R':
			workflow = self.workflows[workflow].check(part)
		return True if workflow == "A" else False


	def check_range(self):
		ranges_queue = [(PartRange(), 'in')]
		count = 0
		while len(ranges_queue) > 0: 
			current_range, current_workflow = ranges_queue.pop()
			if current_workflow == "A":
				count += current_range.n_values()
			elif current_workflow != "R":
				ranges_queue.extend(self.workflows[current_workflow].check_ranges(current_range))
		return count

## File Parsing ##
## ------------ ##
def string_2_parts(part_strings):
	part_string = part_strings[0][1:-1] 
	d = [{e.split('=')[0] : int(e.split('=')[1]) for e in part[1:-1].split(',')} for part in part_strings]
	return [Part(**values) for values in d]

def string_2_workflows(workflows_string):
	workflows = []
	for wf_s in workflows_string:
		name, wf = wf_s.split('{')
		wf = wf[:-1].split(',')
		end = wf.pop()
		steps = [Step(s) for s in wf]
		workflows.append(Workflow(name, steps, end))

	return Workflows(workflows)


def read_in_workflows(filename):
	with open(filename) as file:
		workflows, parts = file.read().split('\n\n')
	return string_2_workflows(workflows.split('\n')), string_2_parts(parts[:-1].split('\n'))


## Solution Functions ##
## ------------------ ## 

def check_parts(filename):
	wf, parts = read_in_workflows(filename)	
	accepted_parts = [p for p in parts if wf.check(p)]
	return sum((p.add_values() for p in accepted_parts))

def check_ranges(filename):
	wf, _ = read_in_workflows(filename)
	return wf.check_range()

print(check_parts("Inputs/Day_19_Test.txt"))
print(check_parts("Inputs/Day_19_input.txt"))

print(check_ranges("Inputs/Day_19_Test.txt"))
print(check_ranges("Inputs/Day_19_input.txt"))

