#1
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

#2
class Student(Person):
  def __init__(self, fname, lname):
    Person.__init__(self, fname, lname)

#3
class Student(Person):
  pass

#4
# Родительский (базовый) класс
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} кушает")

# Дочерний класс (наследует Animal в круглых скобках)
class Dog(Animal):
    def bark(self):
        print(f"{self.name} лает: Гав-гав! ")

# Создаем объект дочернего класса Dog
my_dog = Dog(name="Шарик")

# Метод eat() взят из родительского класса Animal
my_dog.eat()  
# Метод bark()  -собственный метод класса Dog
my_dog.bark()  