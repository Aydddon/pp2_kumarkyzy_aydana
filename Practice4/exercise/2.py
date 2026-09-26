#1
def squares(n):
    for i in range(n + 1):
        yield i * i


n = int(input("Enter N: "))

for x in squares(n):
    print(x)

#2
def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i


n = int(input("Enter n: "))

print(",".join(map(str, even_numbers(n))))

#3
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


n = int(input("Enter n: "))

for x in divisible_by_3_and_4(n):
    print(x)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input("Enter a: "))
b = int(input("Enter b: "))

for x in squares(a, b):
    print(x)

