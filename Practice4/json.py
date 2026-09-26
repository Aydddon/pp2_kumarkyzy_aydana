#1
import json
x='{"name:"Aidana,"age":19,"city":"Kostanay"}'
y=json.loads(x)
print(y["age"])

#2
import json
x={
    "name":"Aidana",
    "age":30,
    "city":"Kostanay"
}

y=json.dumps(x)
print(y)

#3
import json
print(json.dumps({"name":"Aidana","age":19}))
print(json.dumps(["apple","bananas"]))
print(json.dumps(("apple","bananas")))
print(json.dumps("hello"))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

#4
import json
x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
print(json.dumps(x))

