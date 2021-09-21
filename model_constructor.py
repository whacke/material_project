from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

print("Loadig DataFrame...")
df_total = pd.read_csv('output/TOTAL_frame.csv')
df_total = df_total.drop(['name', 'name.1'],axis=1)

print("Building Model...")
scaler = StandardScaler()
X = df_total[list(set(df_total.columns)-set(['dimension']))]
y= df_total['dimension']
y= y.astype('int')
X = X.replace(np.nan,0) #make sure we have no NaN's left

X_norm = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.60)

scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

clf = RandomForestClassifier(n_jobs=2, random_state=0)
clf.fit(X_train, y_train)

import datetime
# View a list of the features and their importance scores (how important was this feature to the decision)
f = open('output/model_report.txt', 'a')
time = datetime.datetime.now()
f.write(time.strftime("%c"))
f.write("\n-------------------------------------\n")
f.write("Importance scores\n")
y_pred = clf.predict(X_test)
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

for x in range(X.shape[1]):
    f.write('%d. features %d (%f)\n'% (x+1, indices[x], importances[indices[x]]))
f.write("-------------------------------------\n")
# Create confusion matrix
f.write("Confusion matrix\n")
f.write(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted']).to_string())
f.write("\n-------------------------------------\n")
f.write("Accuracy Scores\n")
f.write(classification_report(y_test, y_pred))
f.write("-------------------------------------\n\n\n")

f.close()

print("Pickling...")
import pickle5 as pickle
with open('output/model.pkl', 'wb') as file:
    pickle.dump(clf, file)

print("[[ALL DONE]]")