import warnings
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Suppress warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_excel('C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/dataset/Dataset_AUS.xlsx')

def read_excel(university_id):
    # Implement function logic to retrieve the university name by its ID
    # For example, you might retrieve from a dictionary or load from a file
    university_dict = {1: "University of Sydney", 2: "University of Melbourne"}  # Example mapping
    return university_dict.get(university_id, None)
# Encode the 'UNIVERSITY' column with LabelEncoder
le1 = LabelEncoder()
df['UNIVERSITY'] = le1.fit_transform(df['UNIVERSITY'].astype(str))

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

# Save the trained model to a file
filename = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_AUS.sav'
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
accuracy = classifier.score(X_test, y_test)
print('Accuracy:', accuracy)
