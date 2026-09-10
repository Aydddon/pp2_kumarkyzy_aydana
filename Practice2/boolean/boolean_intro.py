print(10 > 9)   #1
print(10 == 9)
print(10 < 9)


a = 200      #2
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")


x = "Hello"      #3
y = 15

print(bool(x))
print(bool(y))

print(bool("Hi"))
print(bool(15))


bool("abc")     #4
bool(123)
bool(["apple", "cherry", "banana"])

def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

x = 200
print(isinstance(x, int))


#5
print(bool("Hello"))  # True (no empty line)   
print(bool(""))   # False (empty line)

