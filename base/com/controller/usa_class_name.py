import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings('ignore')

df = pd.read_excel('C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/dataset/Dataset_USA.xlsx')

le1 = LabelEncoder()
df['UNIVERSITY'] = le1.fit_transform(df['UNIVERSITY'].astype(str))
X = df[
    ['GRE', 'IELTS', 'GPA', 'TOFEL', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper', 'ConferenceAttend']]
y = df['UNIVERSITY']
print('X>>>>>>>>>>', X)
print('y>>>>>>>>>>', y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
X_train = X_train.to_numpy()
X_test = X_test.to_numpy()
y_train = np.array(y_train).reshape(-1, 1)  # or y_train.to_numpy().reshape(-1, 1)
y_test = np.array(y_test).reshape(-1, 1)

print("X_train=", X_train.shape, type(X_train))
print("X_test=", X_test.shape, type(X_test))
print("y_train=", y_train.shape, type(y_train))
print("y_test=", y_test.shape, type(y_test))

Canada_Classifier = RandomForestClassifier()
Canada_Classifier.fit(X_train, y_train)
filename = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_USA.sav'
joblib.dump(Canada_Classifier, filename)

predicted_y = Canada_Classifier.predict(X_test)
print('predicted_y>>>>>', predicted_y)
print(le1.inverse_transform(predicted_y))
print("MAE: %.4f" % mean_absolute_error(y_test, predicted_y))
accuracy = Canada_Classifier.score(X_test, y_test)
print('Accuracy::', accuracy)
