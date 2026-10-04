#1 "[arn]"  Returns a match where one of the specified characters
import re

txt = "The rain in Spain"
x = re.findall("[arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#2 "[a-n]" 
txt = "The rain in Spain"
x = re.findall("[a-n]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#3 "[^arn]" Returns a match for any character EXCEPT a, r, and n

txt = "The rain in Spain"
x = re.findall("[^arn]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#4 "[0123]" Returns a match where any of the specified digits 
txt = "The rain in Spain"

x = re.findall("[0123]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#5 "[0-9]" Returns a match for any digit between 0 and 9
txt = "8 times before 11:45 AM"

x = re.findall("[0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#6 "[0-5][0-9]" Returns a match for any two-digit numbers from 00 and 59	


txt = "8 times before 11:45 AM"
x = re.findall("[0-5][0-9]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


#7 "[a-zA-Z]" Returns a match for any character alphabetically between a and z, lower case OR upper case

txt = "8 times before 11:45 AM"

x = re.findall("[a-zA-Z]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#8 "[+]" 	In sets, +, *, ., |, (), $,{} has no special meaning, so [+] means: return a match for any + character in the string	

txt = "8 times  before 11:45 AM"

x = re.findall("[+]", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")