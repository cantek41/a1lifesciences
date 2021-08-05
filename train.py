# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 19:28:25 2021

@author: cantek
"""
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression

import numpy as np
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from joblib import dump, load

#data Read
raw_data =pd.read_csv(r"C:\Users\cantek\Desktop\a1\Problem_3_Data.txt",sep="\t")


#data Process
data = raw_data.copy()
target = {"No":0, "Yes":1}
data["Healthy"] = data["Healthy"].map(target)

#add ne feature
bins= [0,2,4,7,13,18,30,45,110]
labels = [1,2,3,4,5,6,7,8]
data["Age_group"]=pd.cut(data['Age'], bins=bins, labels=labels, right=False)
data["Age_group"]=data["Age_group"].astype(int)


# weight, age corr formul
# https://www.researchgate.net/figure/Weight-changes-with-different-treatment-modalities-Data-are-presented-as-means-SE_fig3_7273156
data["r2"]=-0.04*data['Age']+2.5 



x=data.drop(["Healthy"],axis=1).values
y=data["Healthy"].values

#data normalize
sc=StandardScaler()
x=sc.fit_transform(x)

#seperate
X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.1, shuffle=True)


#model
lr = LogisticRegression()
clf = lr.fit(X_train, y_train)

#score
score = clf.score(X_test, y_test)
print("LR",score)


#test
p = clf.predict_proba(X_test[0].reshape(1,-1))

#save
dump(clf,r"C:\Users\cantek\Desktop\a1\model.joblib")

dump(sc,r"C:\Users\cantek\Desktop\a1\scaler.joblib")
