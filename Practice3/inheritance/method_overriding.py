#1
class Animal:
    def make_sound(self): print("Звук")
class Dog(Animal):
    def make_sound(self): print("Гав-гав!")

Dog().make_sound()

#2
class Transport:
    def speed(self): print("Обычная скорость")
class SportsCar(Transport):
    def speed(self): print("Очень быстро!")

SportsCar().speed()

#3
class User:
    def get_discount(self): return 0
class VIPUser(User):
    def get_discount(self): return 20

print(VIPUser().get_discount())

#4
class Greeter:
    def greet(self): print("Здравствуйте")
class FriendGreeter(Greeter):
    def greet(self): print("Сәлем!")

FriendGreeter().greet()