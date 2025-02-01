import pandas as pd
import os

# Loading dataset in chunks to avoid memory overload
chunk_size = 500000

# Construct the file path relative to the current script
file_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "processed_logs.csv")

print(f"Loading dataset from: {file_path}")

chunks = pd.read_csv(file_path, chunksize=chunk_size)

df_list = []
for chunk in chunks:
    chunk["message"] = chunk["message"].str.lower()
    df_list.append(chunk)

# Concatenate all processed chunks
dataset = pd.concat(df_list, ignore_index=True)

dataset.head()

print(f"Total rows loaded: {len(dataset)}")