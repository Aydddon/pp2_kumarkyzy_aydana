#1
class User:
    # Переменная класса 
    user_count = 0

    def __init__(self, name):
        self.name = name  # Переменная экземпляра
        User.user_count += 1  # Увеличиваем счетчик при создании каждого юзера

# Создаем объекты
u1 = User("Айдана")
print(User.user_count)  

u2 = User("Диас")
print(User.user_count)  

#2
class Student:
    # Переменная класса 
    university = "KBTU"

    def __init__(self, name, major):
        self.name = name
        self.major = major

student1 = Student("Тимур", "Computer Science")
student2 = Student("Томирис", "Finance")

print(student1.name, "учится в", student1.university)  
print(student2.name, "учится в", student2.university)


#3
class BankAccount:
    # Переменная класса — общая процентная ставка для всех счетов
    interest_rate = 5.5

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

acc1 = BankAccount("Али", 1000)
acc2 = BankAccount("Алия", 5000)

print(acc1.interest_rate) 
print(acc2.interest_rate)  

# Если ставка изменится, она обновится для всех
BankAccount.interest_rate = 6.0
print(acc1.interest_rate)  

#4

class Car:
    # Общий список всех машин на дороге
    all_cars = []

    def __init__(self, model):
        self.model = model
        Car.all_cars.append(self)  # Добавляем созданную машину в общий список

car1 = Car("Toyota")
car2 = Car("BMW")
car3 = Car("Tesla")

# Проверяем, сколько машин в списке через переменную класса
print(len(Car.all_cars)) 
for car in Car.all_cars:
    print(car.model)     