#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#2
subject = ["math", "", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

#3
for num in range(10):
    if num % 2 != 0:
        continue
    print("Even num:", num)

#4
vowels = "aeiou"
for char in "hello":
    if char in vowels:
        continue
    print("Consonant:", char)

#5
lines = ["line1", "", "line2", ""]
for line in lines:
    if not line:
        continue
    print("Valid line:", line)