# This script invoke the trained model and score on the test data.
# There is a conda_dependencies.yml in this directory which is exactly same as the one in aml_config. 
# score.py and conda dependencies are required by the 30-CreateScoringImage.py scripts to be in same root directory while creating the image.

# Source code reference: Microsoft Azure machine learning.

import pickle
import json
from sklearn.svm import SVC
import pandas as pd
from sklearn.externals import joblib
from azureml.core.model import Model
import numpy
from sklearn import preprocessing

def init():
    global model
    model_path = Model.get_model_path(model_name='svm_mldevcredit_model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    try:
        # print("testing")
        data = json.loads(raw_data)["data"]
        df = pd.DataFrame(data,columns=["Average Amount/transaction/day","Transaction_amount","Is declined","Total Number of declines/day","isForeignTransaction","isHighRiskCountry","Daily_chargeback_avg_amt","6_month_avg_chbk_amt","6-month_chbk_freq"])
        # display(df)
        for column in df.columns:
            if df[column].dtype == type(object):
                le = preprocessing.LabelEncoder()
                df[column] = le.fit_transform(df[column])
        result = model.predict(df)
        
        # result2 = le.inverse_transform(result) 
        resultoutput = ['Y' if i == 1 else 'N' for i in result.tolist()]   

        return json.dumps({"Prediction for the given transaction": resultoutput})
        # return result 
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})

if __name__ == "__main__":
# Test scoring
    init()
    test_row = '{"data":[[200,3000,"N",4,"N","N",700,800,9],[100,9000,"Y",7,"Y","Y",400,300,2]]}'
    prediction = run(test_row)
    print("Test result: ", prediction)