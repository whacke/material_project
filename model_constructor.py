from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

print("Loadig DataFrame...")
df_total = pd.read_csv('output/TOTAL_frame.csv')

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

"""# Output

The final output is a list of every feature, scored as a percentage based on how important it was to the model during training. This can help us focus on what features are important. We then see a confusion matrix and classification report, which tell us how accurate our model should be. The most important value here is the F1-Score, which is a measure of the model's accuracy on a dataset by combining the model's recall and precision.
"""

import datetime
# View a list of the features and their importance scores (how important was this feature to the decision)
f = open('output/model_report.txt', 'a')
f.write(datetime.datetime.now())
f.write("\n-------------------------------------\n")
f.write("Importance scores\n")
y_pred = clf.predict(X_test)
f.write(*list(zip(df_total.columns, clf.feature_importances_ * 100)), sep = "\n")
f.write("\n-------------------------------------\n")
# Create confusion matrix
f.write("Confusion matrix\n")
f.write(pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted']))
f.write("\n-------------------------------------\n")
f.write("Accuracy Scores\n")
f.write(classification_report(y_test, y_pred))
f.write("\n-------------------------------------\n")

f.close()

print("Pickling...")
import pickle5 as pickle
with open('output/model.pkl', 'wb') as file:
    pickle.dump(model, file)

prnt("[[ALL DONE]]")