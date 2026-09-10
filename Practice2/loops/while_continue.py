#1
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

#2
e = 0
while e < 6:
  e += 1
  if e == 2:
    continue
  print(e)

#3
a = 0
while a < 7:
  a += 2
  if a == 4:
    continue
  print(a)

#4
for char in "Hello World":
    if char == " ":
        continue
    print(char)

#5

count = -3
while count < 3:
    count += 1
    if count < 0:
        continue
    print("Non-negative:", count)