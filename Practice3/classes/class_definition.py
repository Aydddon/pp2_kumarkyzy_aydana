#1
class MyClass:
  x = 5

#2
class Cat:
    def __init__(self, name, age):
        self.name = name  # Атрибут
        self.age = age    # Атрибут

# Создаем конкретных котиков
cat1 = Cat("Барсик", 3)
cat2 = Cat("Мурка", 5)

print(cat1.name)  # Выведет: 
print(cat2.age)   # Выведет: 

#3
class Dog:
    def __init__(self, name):
        self.name = name

    # Метод класса 
    def bark(self):
        print(f"{self.name} говорит: Гав-гав! 🐕")

# Создаем собаку и заставляем ее «подать голос»
my_dog = Dog("Шарик")
my_dog.bark() 

#4

class Book:
    # Конструктор для создания книги с названием, автором и количеством страниц
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    # Метод, который выводит информацию о книге
    def description(self):
        print(f"Книга «{self.title}», автор: {self.author}, страниц: {self.pages}")

my_book = Book("Маленький принц", "Антуан де Сент-Экзюпери", 96)

# Используем атрибуты и метод
print(my_book.title)       
my_book.description()       