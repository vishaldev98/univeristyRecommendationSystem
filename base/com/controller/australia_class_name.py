import warnings
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import joblib

# Suppress warnings
warnings.filterwarnings('ignore')

# Load dataset
dataset_path = 'C:/Users/TanyaChamala/Desktop/UniversityRecommendation/UniversityRecommendation/university-recommendation/base/static/adminResources/dataset/Dataset_AUS.xlsx'

try:
    df = pd.read_excel(dataset_path)
except FileNotFoundError:
    print(f"Error: The dataset at {dataset_path} was not found.")
    exit()
except Exception as e:
    print(f"Error: Unable to load dataset. {e}")
    exit()

def read_excel(university_id):
    # Example mapping of university ID to name
    university_dict = {1: "University of Sydney", 2: "University of Melbourne"}
    return university_dict.get(university_id, None)

# Encode the 'UNIVERSITY' column with LabelEncoder
le1 = LabelEncoder()
df['UNIVERSITY'] = le1.fit_transform(df['UNIVERSITY'].astype(str))

# Check for missing values in the dataset and handle them
if df.isnull().sum().any():
    print("Warning: Missing values detected. Filling missing values with the median.")
    df.fillna(df.median(), inplace=True)

# Define features (X) and target (y)
X = df[['IELTS', 'TOFEL', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper', 'ConferenceAttend']]
y = df['UNIVERSITY']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Convert to NumPy arrays for compatibility
X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = y_train.to_numpy()
y_test = y_test.to_numpy()

# Initialize and train the RandomForestClassifier
classifier = RandomForestClassifier(random_state=42)
classifier.fit(X_train, y_train)

# Optionally, use cross-validation for more robust evaluation
cv_scores = cross_val_score(classifier, X, y, cv=5, scoring='accuracy')
print(f"Cross-Validation Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Save the trained model to a file
filename = 'C:/Users/TanyaChamala/Desktop/UniversityRecommendation/UniversityRecommendation/university-recommendation/base/static/adminResources/models/Model_AUS.sav'
joblib.dump(classifier, filename)

# Make predictions on the test set
predicted_y = classifier.predict(X_test)

# Decode predictions and actual values back to original labels
decoded_predictions = le1.inverse_transform(predicted_y)
decoded_actual = le1.inverse_transform(y_test)

# Display results
print('Predicted Labels:', decoded_predictions)
print('Actual Labels:', decoded_actual)
print("Mean Absolute Error (MAE): %.4f" % mean_absolute_error(y_test, predicted_y))

# Calculate accuracy on the test set
accuracy = classifier.score(X_test, y_test)
print('Accuracy on Test Set:', accuracy)
