#1
def my_function(fname):   #параметр
  print(fname + " Refsnes")

my_function("Aidana") #аргументы
my_function("Mariam")
my_function("Lazat")

#2
def my_function(fname, lname):
  print(fname + " " + lname) #двойной параметр

my_function("Kumarkyzy", "Aidana")

#3
def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)


#4
def my_function(*, name):
  print("Hello", name)

my_function(name = "Emil")