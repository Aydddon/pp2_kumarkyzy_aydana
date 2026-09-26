#1
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

#2
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Aidana", "Tima", "Simba")

#3
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Aidana", "Tima", "Simba")

#4
print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")

#5
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function(name = "Tobias", age = 30, city = "Bergen")

#5
def greet():
  print("Hello")
greet()

#6
def add(a,b):
  return a+b
result=add(3,5)
print(result)

#7

def show(*args, **kwargs):
  print(args)
  print(kwargs)
  show(1,2, name='Aida')

  #7 
  square = lambda x: x*x
  print(square(4))

  #8

  class Student:
    def hello(self):
      print("Hello")

student= Student("Aida")
student.hello()


class Student:
  def __init__(self,name, age):
    self.name=name
    self.age=age

def show_info(self):
  print(self.name)
  print(self.age)

student = Student("Aida", 19)
student.show_info()