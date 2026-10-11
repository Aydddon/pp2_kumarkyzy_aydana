#1
f = open("demofile.txt", "r")
print(f.read())
f.close()

#2
f = open("demofile.txt")
print(f.read())

#3
f = open("D:\\myfiles\welcome.txt")
print(f.read())

#4
with open("demofile.txt") as f:
  print(f.read())

#5
with open("demofile.txt") as f:
  print(f.read(5))

#6
with open("demofile.txt") as f:
  print(f.readline())

#7
with open("demofile.txt") as f:
  for x in f:
    print(x)