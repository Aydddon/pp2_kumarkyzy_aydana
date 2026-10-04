#1
import re

txt="The rain in Spain"
x=re.search("^The.*Spain$", txt)

if x:
     print("Yes! We have a match!")
else:
     print("No match")

#2 findall() returns a list containing all matches 
import re

txt="The rain in spain"
x=re.findall("ai",txt)
print(x)
#if not match return an empty
import re 

txt="The rain in spain"
x=re.findall("Portygal",txt)
print(x)
if(x):
     print("Yes,there is at least one match!")
else:
     print("No match")

#3 the search function, if no match return None 
import re
txt="The rain in Spain"
x=re.search("\s",txt)
print("The first white-space character is located in position:",x.start())

#4 the split() function returns a list you control count num
import re
txt="The rain in Spain"
t=re.split("\s",txt)
print(x)

#5 sub() function replace every white space character with the num/word also control count num
import re
txt="The rain in Spain"
x=re.sub("\s","9",txt)
print(x)

#6 position start and end of the first match
import re

txt="The rain in Spain"
x=re.search(r"\bS\w+",txt)
print(x.span())
#return strings starts S uppercase
import re
txt="The rain in Spain"
x=re.search(r"\bS\w+", txt)
print(x.group())

#7 find a set of characters "[a-m]"
import re
txt="The rain in Spain"
x=re.findall("[a-m]",txt)
print(x)

#8 signals a special sequence "\d"
import re
txt="The rain in Spain 59"
x=re.findall("\d",txt)
print(x)

#9 any character "he..o"
txt="hello word"
x=re.findall("he..o",txt)
print(x)

#10 "^" starts with 
txt="hello world"
x=re.findall("^hello",txt)
if(x):
     print("Yes")
else:
     print("No")

#11 ends with "$"
txt="Aidana"
x=re.findall("ana$",txt)
if(x):
     print("Yes")
else:
     print("No")

#12 zero or more occurences "*"
txt="hello world"
t=re.findall("he.*o",txt)
print(t)

#13 "+" one or more occurences
txt="hello world"
t=re.findall("he.+o",txt)
print(t)

#14 "?" zero or one occurences 
txt="hello world"
t=re.findall("he.?o",txt)
print(t)

#15 "{}" exactly the cpesified num of occurences
txt="hello world"
t=re.findall("he.{2}o",txt)
print(t)

#16 "|" either or 
txt = "The rain in Spain falls mainly in the plain!"
x = re.findall("falls|stays", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")


