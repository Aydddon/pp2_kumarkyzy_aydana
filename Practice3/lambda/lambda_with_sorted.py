#1
nums = [-5, 1, -3, 2]
result = sorted(nums, key=lambda x: abs(x))
print(result)  # Выведет: [1, 2, -3, -5]

#2
words = ["python", "ai", "code"]
result = sorted(words, key=lambda w: len(w))
print(result)  # Выведет: ['ai', 'code', 'python']

#3
users = [{"name": "Али", "age": 25}, {"name": "Айгерим", "age": 20}]
result = sorted(users, key=lambda u: u["age"])
print(result)  # Выведет сначала Айгерим (20), потом Али (25)

#4
items = [("apple", 150), ("banana", 100), ("orange", 200)]
result = sorted(items, key=lambda item: item[1])
print(result)  # Выведет по возрастанию цены: banana, apple, orange