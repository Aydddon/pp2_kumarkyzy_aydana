import os

# Create a directory
if not os.path.exists("PracticeFolder"):
    os.mkdir("PracticeFolder")

# Create nested directories
os.makedirs("PracticeFolder/Folder1/Folder2", exist_ok=True)

print("Current directory:", os.getcwd())
print("All items:", os.listdir("."))

# List only directories
for item in os.listdir("."):
    if os.path.isdir(item):
        print("Directory:", item)

# List only files
for item in os.listdir("."):
    if os.path.isfile(item):
        print("File:", item)