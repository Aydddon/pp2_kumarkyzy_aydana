#1 task
import re
txt="abb"
t=re.fullmatch(r"ab*",txt)
print(t)

#2 task
txt="abbb"
t=re.fullmatch(r"ab{2,3}",txt)
print(t)

#3 task
txt="Hello_world"
r=re.findall(r"[a-z]+_[a-z]",txt)
print(r)

#4 task
txt="Hello Python Apple"
t=re.findall(r"[A-Z][a-z]+",txt)
print(t)

#5 task
txt="a123b"
t=re.fullmatch(r"a.*b", txt)
print(t)

#6 task
txt="Hi my name is Aidana"
r=re.sub("\s",":",txt)
print(r)

#7 task 
txt="hello_word"
r=re.sub(r"_([a-z])", lambda x: x.group(1).upper(),txt)
print(r)

#8 task
txt="HelloWorldPython"
r=re.split(r"[A-Z]",txt)
print(r)

#9 task
txt="HelloWorldPython"
r=re.sub(r"(?<!^)([A-Z])", r" \1", txt)
print(r)

#10 task
txt="helloWorldPython"
r=re.sub(r"([A-Z])",r"_\1", txt).lower()
print(r)