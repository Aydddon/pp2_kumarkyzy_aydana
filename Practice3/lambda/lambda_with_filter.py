#1
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Оставляем только четные числа
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print("Изначальный список:", numbers)
print("Только четные:", even_numbers)  

#2
nums = [1, 2, 3, 4, 5, 6]
result = list(filter(lambda x: x % 2 == 0, nums))
print(result)  # Выведет: [2, 4, 6]

#3
nums = [-5, 3, 0, -1, 8]
result = list(filter(lambda x: x > 0, nums))
print(result)  # Выведет: [3, 8]

#4
words = ["кот", "собака", "дом", "машина"]
result = list(filter(lambda w: len(w) > 4, words))
print(result)  # Выведет: ['собака', 'машина']