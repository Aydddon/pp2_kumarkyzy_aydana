#1
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)

#2
def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1

for num in count_up_to(5):
  print(num)

#3
def simple_gen():
  yield "Emil"
  yield "Tobias"
  yield "Linus"

gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))

#4 iterator
mytuple = ("apple","banana", "cherry")
myit=iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

#5
mystr="banana"
myit=iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
