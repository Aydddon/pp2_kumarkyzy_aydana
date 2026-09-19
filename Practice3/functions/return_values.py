#1
def my_function(x, y):  #параметры
  return x + y   #возвращает функцию

result = my_function(5, 3)  #аргумент
print(result)

#2
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0]) #возвращает по индексу в списке
print(fruits[1])
print(fruits[2])

#3
def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)

#4
def power_up(number, power=2):
    return number ** power

print(power_up(3))    # Использовать степень по умолчанию 3 в квадрате 
print(power_up(3, 3)) # Передать свою степень 3 в кубе

