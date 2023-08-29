#mcc-deps-networkx.py
import os
import pandas as pd
import networkx as nx
import subprocess
from radon.complexity import cc_visit
from dotenv import load_dotenv
import pygraphviz as pgv  # You might need to install this using pip
from print_python_files import print_python_files

print_python_files('/home/scott/habit-tracker-app/habit_tracker/')

# Load all environment variables
load_dotenv()

# Get the path from the environment variable
directory_path_MCC = os.getenv('DIRECTORY_PATH_MCC')  # McCabe's cyclomatic complexity
print(f"The variable in the .env file of directory_path_MCC is {directory_path_MCC}")

# Run pydeps on the directory and output to a dot file
dot_output = 'output.dot'
try:
    result = subprocess.run(['pydeps', directory_path_MCC, '--noshow', '-o', dot_output], 
                            check=True, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            text=True)
    print("Standard Output:\n", result.stdout)
    print("Standard Error:\n", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"pydeps command failed with error code {e.returncode}, stderr:\n{e.stderr}")

# Read in the dot output file and create a directed graph
print(f"dot_output is: {dot_output}")

try:
    A = pgv.AGraph(dot_output)
except Exception as e:
    print(f"Failed to read .dot file: {e}")

#A = pgv.AGraph(dot_output)
#A = pgv.AGraph("/home/scott/code-complexity-app/test.dot")
G = nx.nx_agraph.from_agraph(A)

# This will give us a new directed graph H representing the transitive closure of G
H = nx.transitive_closure(G)

# Get all .py files in a directory
py_files = [f for f in os.listdir(directory_path_MCC) if f.endswith('.py')]
print(py_files)

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

