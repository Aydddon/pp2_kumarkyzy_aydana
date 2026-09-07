# day = 3
# match day:
#     case 1:
#         print("Monday")
#     case 2:
#         print("Tuesday")
#     case 3:
#         print("Wednesday")
#     case _:
#         print("Other day")


# film =["dazzling", "happiense", "enn with twi n", "Enola holmes","killer house"]
# film.append("All boys i love") 
# film.pop(1)
# print(len(film))


# day = ("Monday", "Tuesday","Wednesday", "Thursday", "Friday","Saturday","Sunday")
# print("Sunday" in day)

# set= {1, 2, 2, 3, 4, 4, 5}
# A={1, 2, 3}
# B={3, 4, 5}
# print(A-B)

# dict={"name": "Aidana", "age": 19, "major": "It"}
# dict.update({"gpa": 3.5})
# print(dict)

# a=[x*x for x in range(1,11)]
# print(a)

# b=[x for x in range(1,21)]
# d=[x for x in b if x%2==0]
# print(d)

# a=[x for x in range(1,21)]
# b=[x for x in a if x%3==0]
# print(b)

# names=['aida', 'ali', 'dana']
# upper_list=[a.upper() for a in names]
# print(upper_list)

# names=["AIDANA","SYMBAT","GULIM"]
# lower_list=[a.lower() for a in names]
# print(lower_list)


# name= input()
# vowels=['a','e','u','o','i]
# count= sum(1 for char in name.lower() if char in vowels)
# print(count)

# name= input()
# vowels=['a','e','u','o','i']
# count=sum(1 for char in name.lower() if char not in vowels)
# print(count)

# s=input()
# def is_palin(s):
#     s_lower=s.lower()
#     return s_lower==s_lower[::-1]
# print(is_palin(s))

# try:
#     a=int(input())
#     b=int(input())

#     result=a/b
#     print(result)
# except ValueError:
#     print("Error input numbers")
   
# except ZeroDivisionError:
#     print("Error zero division 0!")


# class Student:
#     def info(self,name,age):
#         self.name=name
#         self.age=age
# name=input()
# age=int(input())

# print(name,age)

# class recstangle:
#     def inf(self,width,height):
#         self.width=width
#         self.height=height

#     def area():
#       return width*height

# width=int(input())
# height=int(input())

# print(recstangle.area())

# from math import sqrt
# class hyp:
#     def inf(self,a,b):
#         self.a=a
     
#         self.b=b

#     def f():
#       return sqrt(a*a+b*b)
    
# a=int(input())
# b=int(input())

# print(hyp.f())



# class Animal:
#     def speak(self):
#         print("Song")

# class Dog(Animal):
#     def bark(self):
#         print("Gav")

# dog=Dog()

# dog.speak()
# dog.bark()


