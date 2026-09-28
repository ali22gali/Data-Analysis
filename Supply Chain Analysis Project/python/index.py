import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data/cleaned_data.csv")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print(df.head())