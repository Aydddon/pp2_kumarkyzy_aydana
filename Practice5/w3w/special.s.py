#1 "\A" returns a match at the beginning of the string
import re
txt="rain in Spain The"
x=re.findall("\AThe",txt)
print(x)

if(x):
    print("Yes")
else:
    print("No match")

#2 "\b" a match w/e the s/d c/s are the beg. or at the end of a word
#no match "\B"
txt = "The rain in Spain"

x = re.findall(r"ain\b", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#3 "\d" contains digits num(0-9)
# "\D" not contains
txt = "The rain in Spain"
x = re.findall("\d", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#4 "\s"  white space character
# "\S" does not contain 
txt = "The rain in Spain"

x = re.findall("\s", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#5 "\w" r/m the string contains any word c/s (a-z,0-9)
# "\W" DOES NOT contain any word characters
txt = "The rain in Spain"
x = re.findall("\w", txt)

print(x)

if x:
  print("Yes, there is at least one match!")
else:
  print("No match")

#6 "\z" Returns m/s c/s are at the end of the string
txt = "The rain in Spain"
x = re.findall("Spain\Z", txt)

print(x)

if x:
  print("Yes, there is a match!")
else:
  print("No match")