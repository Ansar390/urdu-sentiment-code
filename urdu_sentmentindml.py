# -*- coding: utf-8 -*-
"""urdu_sentmentINDML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VrZoEHvJ5wfg-8fn_SMv89KUMFma5GFA
"""

from google.colab import drive
drive.mount('/content/drive/')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/urdu sentiments

import pandas as pd
import numpy as np

train=pd.read_csv('trainHYBRID.csv')

test=pd.read_csv('testHYBRID.csv')

y_train=train['class']
X_train=train.drop(['Unnamed: 0','class'],axis=1)

y_test=test['class']
X_test=test.drop(['Unnamed: 0','class'],axis=1)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, make_scorer
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold, LeaveOneOut, train_test_split
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import RidgeClassifier, Perceptron
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
# from catboost import CatBoostClassifier
import numpy as np

lgbm=LGBMClassifier().fit(X_train.values,y_train)
rf=RandomForestClassifier().fit(X_train,y_train)
svc=SVC(probability=True).fit(X_train,y_train)
# et=ExtraTreesClassifier().fit(X_train,y_train)
xgb=XGBClassifier().fit(X_train.values,y_train)
lr=LogisticRegression().fit(X_train,y_train)

import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, matthews_corrcoef
y_true = y_test
y_pred_1 = lgbm.predict(X_test)
y_pred_2 = rf.predict(X_test.values)
y_pred_3 = svc.predict(X_test)
y_pred_4 = xgb.predict(X_test)
y_pred_5 = lr.predict(X_test)
# y_pred_6 = xgb.predict(X_test.values)

preds = [y_pred_1, y_pred_2, y_pred_3, y_pred_4, y_pred_5]

for i, y_pred in enumerate(preds, 1):
    print("Classifier ", i)
    # Accuracy
    acc = accuracy_score(y_true, y_pred)
    print("Accuracy: ", acc)


    # Recall
    recall = recall_score(y_true, y_pred, average='macro')
    print("Recall: ", recall)

    # Specificity
    # tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    # specificity = tn / (tn+fp)
    # print("Specificity: ", specificity)
    pr=precision_score(y_test, y_pred)
    print("pr: ", pr)

    f1=f1_score(y_test, y_pred)
    print("f1: ", f1)

    # MCC
    mcc = matthews_corrcoef(y_true, y_pred)
    print("MCC: ", mcc)

    print("\n")
y_pred_4 = xgb.predict(X_test)
y_pred_5 = lr.predict(X_test)
# y_pred_6 = xgb.predict(X_test.values)

from sklearn.ensemble import StackingClassifier
import xgboost as xgb

# Define the base classifiers
xgb_clf = xgb.XGBClassifier(random_state=42)
svc_clf = SVC(random_state=42)

# Define the meta-classifier
meta_clf = LogisticRegression(random_state=42)

# Create the stacking ensemble model
stacked_model = StackingClassifier(
    estimators=[('xgb', xgb_clf), ('svc', svc_clf)],
    final_estimator=meta_clf
)

# Train the stacking ensemble model
stacked_model=stacked_model.fit(X_train, y_train)

# Make predictions on the test data
stacked_pred = stacked_model.predict(X_test)

xgb_clf = xgb.XGBClassifier(random_state=42).fit(X_train,y_train)

# Calculate the accuracy
stacked_accuracy = accuracy_score(y_test, stacked_pred)
print("Stacked Ensemble Accuracy:", stacked_accuracy)
recall = recall_score(y_test, stacked_pred)
print("recall",recall)

pre = precision_score(y_test, stacked_pred)
print("precision",pre)

f1 = f1_score(y_test, stacked_pred)
print("precision",f1)

mcc = matthews_corrcoef(y_true, stacked_pred)
print("MCC: ", mcc)

# replace X1 with X_test and Y1 with y_test
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt


st_probs = stacked_model.predict_proba(X_test)
st_probs = st_probs[:, 1]
# st=st[:, 1]
st_auc = roc_auc_score(y_test, st_probs)
st_fpr, st_tpr, threshold = roc_curve(y_test, st_probs)


rf_probs = rf.predict_proba(X_test)
rf_probs = rf_probs[:, 1]
#clf3=clf3[:,1]
rf_auc = roc_auc_score(y_test, rf_probs)
rf_fpr, rf_tpr, threshold = roc_curve(y_test, rf_probs)

lr_probs = lr.predict_proba(X_test)
lr_probs = lr_probs[:, 1]
#clf1=clf1[:,1]
lr_auc = roc_auc_score(y_test, lr_probs)
lr_fpr, lr_tpr, threshold = roc_curve(y_test, lr_probs)

#ADA
# ada_probs = ada.predict_proba(X_test)
# ada_probs = ada_probs[:, 1]
# #clf4=clf4[:,1]
# ada_auc = roc_auc_score(y_test, ada_probs)
# ada_fpr, ada_tpr, threshold = roc_curve(y_test, ada_probs)

#lgbm
lgbm_probs = lgbm.predict_proba(X_test)
lgbm_probs = lgbm_probs[:, 1]
# clf6=clf6[:,1]
lgbm_auc = roc_auc_score(y_test, lgbm_probs)
lgbm_fpr, lgbm_tpr, thresholdb = roc_curve(y_test, lgbm_probs)

xgb_probs = xgb_clf.predict_proba(X_test)
xgb_probs = xgb_probs[:, 1]
#clf4=clf4[:,1]
xgb_auc = roc_auc_score(y_test, xgb_probs)
xgb_fpr, xgb_tpr, threshold = roc_curve(y_test, xgb_probs)

svc_probs = svc.predict_proba(X_test)
svc_probs = svc_probs[:, 1]
#clf5=clf5[:,1]
svc_auc = roc_auc_score(y_test, svc_probs)
svc_fpr, svc_tpr, thresholde = roc_curve(y_test, svc_probs)


# final_preds = final_preds.reshape(-1, 1)
# blend_probs = blend.predict_proba(final_preds)
# blend_probs = blend_probs[:, 1]
# #clf5=clf5[:,1]
# blend_auc = roc_auc_score(y_test, blend_probs)
# blend_fpr, blend_tpr, thresholde = roc_curve(y_test, blend_probs)


#['purple', 'orange', 'brown', 'gray', 'pink']

plt.figure(figsize=(20, 10), dpi=600)
plt.plot([0, 1], [0, 1], linestyle="--", lw=2,  label="Chance", alpha=0.8)
plt.plot(rf_fpr, rf_tpr, marker='.', label='RF (auc = %0.3f)' % rf_auc)
plt.plot(lr_fpr, lr_tpr, marker='.', label='LR (auc = %0.3f)' % lr_auc)
plt.plot(svc_fpr, svc_tpr, linestyle='-', label='SVC (auc = %0.3f)' % svc_auc)
plt.plot(st_fpr, st_tpr, linestyle='-', label='Stacking (SVC,XGB-->LR) (auc = %0.3f)' % st_auc)
plt.plot(xgb_fpr, xgb_tpr, linestyle='-', label='XGB (auc = %0.3f)' % xgb_auc)
# plt.plot(ada_fpr, ada_tpr, linestyle='-', label='ADA (auc = %0.3f)' % ada_auc)
plt.plot(lgbm_fpr, lgbm_tpr, linestyle='-',color='black', label='LGBM (auc = %0.3f)' % lgbm_auc)




# plt.xlabel('False Positive Rate -->')
# plt.ylabel('True Positive Rate -->')

plt.legend(loc="lower right", fontsize=20, ncol=1)

plt.show()



