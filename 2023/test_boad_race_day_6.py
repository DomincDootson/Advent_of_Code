from boat_race_day_6 import *
import pytest

def test_simple_solution() -> None:
	assert total_number_winning_way("Inputs/Day_6_Test.txt") == 320

def test_second_solution() -> None:
	assert total_number_winning_way_pt2("Inputs/Day_6_Test.txt") == 71503



## Testing the solving functions ##

def test_n_solu() -> None:
	assert n_solutions(7, 9) == 4

def test_n_solu_too_short() -> None:
	with pytest.raises(ValueError):
		n_solutions(1, 2)
	
def test_read_in_times() -> None:
	times, distances = read_in_races("Inputs/Day_6_Test.txt")

	assert times == [7, 15, 30]

def test_read_in_distances() -> None:
	times, distances = read_in_races("Inputs/Day_6_Test.txt")

	assert distances == [9, 40, 200]