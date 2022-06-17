import os

directory = os.fsencode('data')

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".feather"):
         print(os.path.join(filename))
         continue
     else:
         continue