#1
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() - multiply every number by 2
result = list(map(lambda x: x * 2, numbers))
print("Map:", result)

# filter() - select even numbers
result = list(filter(lambda x: x % 2 == 0, numbers))
print("Filter:", result)

# reduce() - calculate the sum
result = reduce(lambda x, y: x + y, numbers)
print("Reduce:", result)

