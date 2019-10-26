# Databricks notebook source
# MAGIC %md ** Credit Card Fraud Detection ** : Supervised Machine Learning model is built to classify whether the transaction is fraud or not.<br>
# MAGIC ** Dataset Source ** : The dataset used in this experiment has been downloaded from kaggle. The input dataset contains  3075 rows and 12 numeric/string columns. <br>
# MAGIC ** Algorithms ** - Support Vector Machine algorithm is used in this experiment.<br>
# MAGIC ** Note: ** This script is integrated to train the ML model in Azure Machine Learning Service in DevOps pipeline.<br>
# MAGIC To run this script independently in Azure Databricks and view the results, please comment out cells 17-20 and uncomment cell 4- load input CSV data in dataframe.<br>
# MAGIC Run the experiment from the beginning.<br>

# COMMAND ----------

#Import Required Python Libraries for ML experiment

import pickle
from azureml.core import Workspace
from azureml.core.run import Run
import os
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import numpy as np
import pandas as pd 
import json
import subprocess
from typing import Tuple, List
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score,auc
from sklearn import preprocessing
from sklearn.svm import SVC



# COMMAND ----------

# Start recording results to Azure Machine Learning
run = Run.get_context()

# COMMAND ----------

#load input CSV data in dataframe
# df_credit = pd.read_csv('/dbfs/FileStore/tables/creditcardcsvpresent.csv')
# display(df_credit)

# load input CSV data from local git repo
df_credit = pd.read_csv('data/creditcardcsvpresent.csv')

# COMMAND ----------

# Statistical summary of input dataset
# df_credit.describe()

# COMMAND ----------

# Total number of rows and columns 
print("Number of rows, number of columns in the input dataset:",df_credit.shape)
# print("List of attributes or cloumns:\n",df_credit.columns)

# COMMAND ----------

#Check if there is any missing rows and columns and Count the number of rows with missing values
print("The Column contains null values:", df_credit.columns[df_credit.isnull().any()].tolist())
print("Number of missing values: ",df_credit.isnull().sum().max())

# COMMAND ----------

# drop the missing column
newdf_credit = df_credit.drop(['Transaction date'], axis='columns')
print("List of columns or attributes:\n",newdf_credit.columns)

# COMMAND ----------

#Select the specific columns as features.
newdf_credit = newdf_credit[['Average Amount/transaction/day', 'Transaction_amount', 'Is declined', 'Total Number of declines/day', 'isForeignTransaction','isHighRiskCountry', 'Daily_chargeback_avg_amt', '6_month_avg_chbk_amt', '6-month_chbk_freq','isFradulent']]
# display(newdf_credit)

# COMMAND ----------

# Hold all the columns in the same data type using label encoder
for column in newdf_credit.columns:
    if newdf_credit[column].dtype == type(object):
        le = preprocessing.LabelEncoder()
        newdf_credit[column] = le.fit_transform(newdf_credit[column])

# COMMAND ----------

#Divide the data into attributes and labels
X = newdf_credit.drop('isFradulent', axis=1)  
y = newdf_credit['isFradulent']  

# COMMAND ----------

# Split the data: 70% to training and 30% to testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30,random_state=0)
X_train.shape, X_test.shape

# COMMAND ----------

# Running training script 
print("Running CreditMlExperiment.py")

# COMMAND ----------

# Training the model using SVM algorithm
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(X_train, y_train)

# COMMAND ----------

# Prediction on test data
y_pred = svm_classifier.predict(X_test)  

# COMMAND ----------

# SVM Classifier results 
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)  
# print("Classification Metrcis:\n", classification_report(y_test, y_pred))  

# COMMAND ----------

TP = cm[0][0]
FP = cm[0][1]
FN = cm[1][0]
TN = cm[1][1]
sensitivity = (TP)/ float(TP+FN)
specificity = TN / float(TN+FP)
precision = TP / float(TP+FP)
accuracy = (TN+TP) / float(TP+TN+FP+FN)
print("SVM classifier results for test data:")
print("Recall: ", sensitivity)
print("Specificity: ", specificity)
print("Precision: ", precision)
print("Accuracy: ", accuracy)

# COMMAND ----------

# Adding classification results to machine learning experiment in Azure Machine Learning service workspace
run.log("Accuracy",accuracy)
run.log("Precision",precision)
run.log("True Positive Rate",sensitivity)
run.log("True Negative Rate",specificity)

# COMMAND ----------

# Save model as part of the run history
model_name = "svm_mldevcredit_model.pkl"

with open(model_name, "wb") as file:
    joblib.dump(value=svm_classifier, filename=model_name)

# COMMAND ----------

# upload the model file explicitly into artifacts
run.upload_file(name="./outputs/" + model_name, path_or_stream=model_name)
print("Uploaded the model {} to experiment {}".format(model_name, run.experiment.name))
dirpath = os.getcwd()
print(dirpath)

# COMMAND ----------

print("Following files are uploaded ")
print(run.get_file_names())
run.complete()