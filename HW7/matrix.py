
import heapq 
import math

matrix = [[1, -1, -1, "-y"], [1, 0, 1, "-y"], [0, 0, -1, "-y"], [0, -1, 1, "-y"], 
[1, 1, 1, "+y"], [0, 1, 0, "+y"], [0, 0, 1, "+y"], [-1, 0, 1, "+y"]]

input_ = [-1, 0, 1]

def find_manhattan_distance():

	heap = []
	for row in matrix:
		total = 0
		for i in range(3):
			dist = abs(input_[i] - row[i])
			total += dist
		both = (total, row)
		heapq.heappush(heap, both)

	for i in range(5):
		print(heapq.heappop(heap))

def euclidean_distance():

	heap = []
	for row in matrix:
		total = 0
		for i in range(3):
			dist = abs(input_[i] - row[i])
			total += (dist*dist)

		total = math.sqrt(total)
		both = (total, row)
		heapq.heappush(heap, both)

	for i in range(5):
		print(heapq.heappop(heap))

def hamming_distance():

	heap = []
	for row in matrix:
		diff = 0
		for i in range(3):
			if(input_[i] != row[i]):
				diff += 1
		heapq.heappush(heap, (diff, row))


	for i in range(5):
		print(heapq.heappop(heap))

print("manhattan distance - 5 closest neighbours")
find_manhattan_distance()
print("euclidean_distance - 5 closest neighbours")
euclidean_distance()
print("Hamming-distance - 5 closest neighbours")
hamming_distance()





