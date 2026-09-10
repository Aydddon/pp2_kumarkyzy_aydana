#1
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

#2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#3
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break
  

#4
numbers = [4, 8, 15, -2, 16, 23]
for n in numbers:
    if n < 0:
        print("First negative number:", n)
        break

#5
codes = [101, 102, 404, 200]
for code in codes:
    if code == 404:
        print("Error code hit, terminating loop")
        break