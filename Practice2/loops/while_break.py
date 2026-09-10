#1
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

#2
s = 1
while s < 5:
  print(s)
  if s == 3:
    break
  i += 1

#3
a = 1
while a < 6:
  print(a)
  if a == 2:
    break
  a += 1

#4

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    if fruit == "banana":
        print("Found banana, exiting!")
        break
    print(fruit)

#5

numbers = [4, 8, 15, -2, 16, 23]
for n in numbers:
    if n < 0:
        print("First negative number:", n)
        break