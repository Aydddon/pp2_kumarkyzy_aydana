#1
import os

path = "."

for item in os.listdir(path):
    full_path = os.path.join(path, item)

    if os.path.isdir(full_path):
        print("Directory:", item)
    elif os.path.isfile(full_path):
        print("File:", item)

#2
import os

path = "data.txt"

print("Exists:", os.path.exists(path))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))

#3
import os

path = "FolderA/test.txt"

if os.path.exists(path):
    print("Filename:", os.path.basename(path))
    print("Directory:", os.path.dirname(path))
else:
    print("Path does not exist.")

#4
with open("data.txt", "r") as file:
    lines = file.readlines()
    print("Number of lines:", len(lines))

#5
students = ["Aida", "Dana", "Ali"]

with open("students.txt", "w") as file:
    for student in students:
        file.write(student + "\n")

print("List saved.")

#6
import string

for letter in string.ascii_uppercase:
    with open(letter + ".txt", "w") as file:
        file.write("This is file " + letter)

print("26 files created.")

#7
with open("data.txt", "r") as source:
    content = source.read()

with open("copy.txt", "w") as destination:
    destination.write(content)

print("Content copied.")

#8
import os

path = "test_delete.txt"

if os.path.isfile(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted.")
    else:
        print("No write permission.")
else:
    print("File does not exist.")
