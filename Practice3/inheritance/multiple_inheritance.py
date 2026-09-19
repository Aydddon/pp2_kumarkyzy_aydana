#1
class Walker:
    def walk(self): print("Иду по земле")
class Swimmer:
    def swim(self): print("Плыву в воде")
class Frog(Walker, Swimmer): pass

f = Frog(); f.walk(); f.swim()

#2
class Phone:
    def call(self): print("Звонок...")
class Camera:
    def take_photo(self): print("Фото!")
class SmartPhone(Phone, Camera): pass

s = SmartPhone(); s.call(); s.take_photo()

#3
class Singer:
    def sing(self): print("Пою песню")
class Guitarist:
    def play_guitar(self): print("Играю на гитаре")
class RockStar(Singer, Guitarist): pass

r = RockStar(); r.sing(); r.play_guitar()

#4
class Human:
    def speak(self): print("Говорю")
class Robot:
    def recharge(self): print("Заряжаюсь")
class Cyborg(Human, Robot): pass

c = Cyborg(); c.speak(); c.recharge()