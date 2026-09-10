#1
i = 1
while i < 6:
  print(i)
  i += 1
#2
a = 1
while a < 6:
  print(a)
  if a == 3:
    break
  a += 1
#3
b = 0
while b < 6:
  b += 1
  if b == 3:
    continue
  print(b)
#4
c = 1
while c < 6:
  print(c)
  c += 1
else:
  print("c is no longer less than 6")

#5
z = 1
while z <= 5:
    print("Count:", z)
    z += 1
    