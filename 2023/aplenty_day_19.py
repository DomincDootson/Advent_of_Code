from dataclasses import dataclass
from operator import lt, gt
from collections import defaultdict
@dataclass
class Part:
	x : int
	m : int  
	a : int
	s : int 

	def add_values(self):
		return self.x + self.m + self.a + self.s

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

	def critical_values(self):
		cv = defaultdict(list)
		for s in self.steps:
			cv[s.var].append(s.value)
			cv[s.var].append(s.value-1 if s.comparison == lt else s.value+1)

		return cv
		
class Workflows(object):
	def __init__(self, workflows):
		self.workflows = {wf.name : wf for wf in workflows}

	def check(self, part):
		workflow = 'in'
		while workflow != 'A' and workflow != 'R':
			workflow = self.workflows[workflow].check(part)
		return True if workflow == "A" else False
		

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

def check_parts(filename):
	wf, parts = read_in_workflows(filename)	
	accepted_parts = [p for p in parts if wf.check(p)]

	return sum((p.add_values() for p in accepted_parts))

print(check_parts("Inputs/Day_19_Test.txt"))
print(check_parts("Inputs/Day_19_input.txt"))


# wf, _ = read_in_workflows("Inputs/Day_19_input.txt")
# print(wf.workflows['in'].critical_values())
# cv = defaultdict(list)
# for w in wf.workflows.values():
# 	cv_w = w.critical_values()

# 	for k, values in cv_w.items():
# 		cv[k].extend(values)

# print(len(cv['x'])*len(cv['a'])*len(cv['m'])*len(cv['s']))

