# enumerate()
students = ["Aida", "Dana", "Ali"]

for index, name in enumerate(students):
    print(index, name)

# zip()
names = ["Aida", "Dana", "Ali"]
grades = [90, 85, 95]

for name, grade in zip(names, grades):
    print(name, grade)



numbers = [5, 2, 8, 1, 9]

# len()
print("Length:", len(numbers))

# sum()
print("Sum:", sum(numbers))

# min() and max()
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))

# sorted()
print("Sorted:", sorted(numbers))

# type()
print(type(numbers))

# Type conversion
number = "123"
print(int(number))

price = 10
print(float(price))

value = 123
print(str(value))

# Check types
print(isinstance(123, int))
print(isinstance("Hello", str))