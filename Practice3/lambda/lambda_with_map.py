#1
numbers = [1, 2, 3, 4, 5]

# Умножаем каждый элемент списка на 2 с помощью map и lambda
doubled = list(map(lambda x: x * 2, numbers))

print("Изначальный список:", numbers)
print("Удвоенный список:", doubled)  

#2
nums = [1, 2, 3]
result = list(map(lambda x: x * 3, nums))
print(result)  # Выведет: [3, 6, 9]

#3
words = ["hello", "world"]
result = list(map(lambda w: w.upper(), words))
print(result)  # Выведет: ['HELLO', 'WORLD']

#4
names = ["Айдана", "Диас", "Тимур"]
result = list(map(lambda name: len(name), names))
print(result)  # Выведет: [6, 4, 5]

