import os
import shutil

# Create directories
os.makedirs("FolderA", exist_ok=True)
os.makedirs("FolderB", exist_ok=True)

# Create a file
with open("FolderA/test.txt", "w") as file:
    file.write("Hello!")

# Copy the file
shutil.copy("FolderA/test.txt", "FolderB/test.txt")
print("File copied.")

# Move the file
shutil.move("FolderB/test.txt", "FolderA/moved.txt")
print("File moved.")

for item in os.listdir("FolderA"):
    if item.endswith(".txt"):
        print("Text file:", item)