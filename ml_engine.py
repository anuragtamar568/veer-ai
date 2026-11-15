
import pandas as pd
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Dataset load karna
data = load_iris()

# 2. Input data (Features)
X = pd.DataFrame(data.data, columns=data.feature_names)

# 3. Output data (Target)
y = data.target

print("Dataset Loaded Successfully!")
print("Total Records:", len(X))
print("Features:", X.columns.tolist())

