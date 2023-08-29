# app.py code-complexity-app
import os
import pandas as pd
from radon.complexity import cc_visit
from dotenv import load_dotenv

# load all environment variables
load_dotenv()

# Get the path from the environment variable
#directory_path = os.getenv('DIRECTORY_PATH') # 
directory_path_MCC = os.getenv('DIRECTORY_PATH_MCC') # McCabe's cyclic complexity



# Get all .py files in a directory
directory_path_MCC = '/home/scott/habit-tracker-app/habit_tracker'  # replace with your actual directory
py_files = [f for f in os.listdir(directory_path_MCC) if f.endswith('.py')]

results = []

# Compute McCabe's Cyclomatic Complexity for each file
for file_name in py_files:
    with open(os.path.join(directory_path_MCC, file_name)) as f:
        content = f.read()

    # Calculate cyclomatic complexity
    cc = cc_visit(content)

    # cc is a list of Complexity objects for each function
    # You might want to decide how you want to aggregate this, for now let's just take the average
    avg_complexity = sum(c.complexity for c in cc) / len(cc) if cc else 0

    results.append({
        'file': file_name,
        'avg_complexity': avg_complexity,
        'num_functions': len(cc),
    })

# Convert results to a DataFrame
df = pd.DataFrame(results)

# Print the DataFrame
print(df)
