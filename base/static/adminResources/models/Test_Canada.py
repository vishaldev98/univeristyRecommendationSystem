import warnings

import pandas as pd
from sklearn import preprocessing
from sklearn.externals import joblib

warnings.filterwarnings('ignore')

model_dump = joblib.load('Model_Canada.sav')

df = pd.read_excel('Dataset_Canada.xlsx')
X = df[['GRE', 'IELTS', 'GPA', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper', 'ConferenceAttend']]

university_list = list(df['UNIVERSITY'])

le1 = preprocessing.LabelEncoder()
df['UNIVERSITY'] = le1.fit_transform(df['UNIVERSITY'].astype(str))

X_test = X.as_matrix()
print(type(X_test))

y_pred = model_dump.predict(X_test)
print(y_pred)
print(y_pred.shape)

y_pred1 = le1.inverse_transform(y_pred)
print(y_pred1)

print('Accuracy::::', model_dump.score(X_test, y_pred))

predicted_UniversityList = []
lable = []
for i in y_pred:
    predicted_UniversityList.append(str(le1.inverse_transform([i])))
    lable.append(i)

columnName = ['Original_Uni', 'Predicted_Uni', 'Lable']

df1 = pd.DataFrame({'Original_Uni': university_list, 'Predicted_Uni': predicted_UniversityList, 'Lable': lable},
                   columns=columnName)

df1.to_csv('Result_Canada.csv')