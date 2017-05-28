import os
import sys

import pandas as pd
import numpy as np

i, j, k = sys.argv[1:]
i = int(i)
j = int(j)
k = int(k)

# Create a matrix of i rows, j columns and max value of k
df = pd.DataFrame(np.random.randn(i, j) +k)

base_path = os.path.expanduser("~/dummy")
if not os.path.exists(base_path):
	os.makedirs(base_path)
store_path = "/".join([str(x) for x in [i, j, k]])
store_path = os.path.join(base_path, store_path)
if not os.path.exists(store_path):
	os.makedirs(store_path)
store_path = store_path + "/data.csv"

df.to_csv(store_path)
