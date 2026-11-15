
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

# 4. Data ko Training aur Testing me baantna
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# 5. Machine Learning Model banana
model = RandomForestClassifier(random_state=42)

# 6. Model ko train karna
model.fit(X_train, y_train)

print("VEER AI ML Model Training Complete!")
print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))

