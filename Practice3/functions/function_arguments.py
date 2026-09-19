#1
def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Aydon") # "Aydon" is an argument

#2
def my_function(name, /):
  print("Hello", name)

my_function("Mariam")

#3
def my_function(*, name):
  print("Hello", name)

my_function(name = "Siko")


#4
def calculate_rectangle_area(length, width):
    area = length * width
    return area

# Calling the function and printing the result
result = calculate_rectangle_area(5.5, 3.0)
print(f"Area: {result}")  

print(calculate_rectangle_area.__doc__)