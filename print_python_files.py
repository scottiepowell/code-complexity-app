import os
import glob

def print_python_files(directory_path):
    python_files = glob.glob(os.path.join(directory_path, "*.py"))
    for file in python_files:
        print(file)

# usage:
print_python_files('/home/scott/habit-tracker-app/habit_tracker/')