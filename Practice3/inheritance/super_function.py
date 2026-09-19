#1
class Person:
    def __init__(self, name): self.name = name
class Student(Person):
    def __init__(self, name, university):
        super().__init__(name)
        self.university = university

s = Student("Айдана", "KBTU")
print(s.name, s.university)

#2
class Parent:
    def say_hello(self): print("Привет", end=" ")
class Child(Parent):
    def say_hello(self):
        super().say_hello()
        print("мир!")

Child().say_hello()

#3
class Appliance:
    def __init__(self, power): self.power = power
class Blender(Appliance):
    def __init__(self, power, modes):
        super().__init__(power)
        self.modes = modes

b = Blender(500, 3)
print(b.power, b.modes)

#4
class Shape:
    def __init__(self, color): self.color = color
class Rectangle(Shape):
    def __init__(self, color, w, h):
        super().__init__(color)
        self.w, self.h = w, h

r = Rectangle("красный", 10, 5)
print(r.color, r.w, r.h)