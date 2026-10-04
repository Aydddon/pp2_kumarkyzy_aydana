#1 ASCII- "re.A"
import re
txt="Åland"
t=re.findall("\w",txt, re.A)
print(t)

#2 Debug 
txt="The rain in Spain"
print(re.findall("spain", txt, re.DEBUG))

#3 Dotall "re.S"

txt = """Hi 
my 
name
is
Sally"""
print(re.findall("me.is", txt, re.S))

#4 Ignorecase "re.I"

txt = "The rain in Spain"
print(re.findall("spain", txt, re.I))

#5 Multiline "re.M"
txt = """There
aint much
rain in 
Spain"""

print(re.findall("^ain", txt, re.M))

#6 unicode "re.U"
import re

txt = "Åland"
print(re.findall("\w", txt, re.U))

#7 verbose "re.X"

text = "The rain in Spain falls mainly on the plain"

pattern = """
[A-Za-z]* #starts with any letter
ain+      #contains 'ain'
[a-z]*    #followed by any small letter
"""
print(re.findall(pattern, text, re.X))

