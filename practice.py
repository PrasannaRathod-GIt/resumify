import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
data = pd.read_csv("student-mat.csv")

# Encode categorical columns
for col in data.select_dtypes(['object']).columns:
    data[col] = LabelEncoder().fit_transform(data[col])

# Define features and target
X = data.drop('G3', axis=1)  # G3 = final grade
y = data['G3']

# Convert grade to pass/fail (binary classification)
y = (y >= 10).astype(int)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

