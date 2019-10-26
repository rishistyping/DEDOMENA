# This script reads the Azure Container Instance info from aci_webservice.json and test it with sample input data.

# Source code reference: Microsoft Azure Machine Learning


import numpy
import os, json, datetime, sys
from operator import attrgetter
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.image import Image
from azureml.core.webservice import Webservice
from azureml.core.webservice import AciWebservice
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()
# Get workspace
ws = Workspace.from_config(auth=cli_auth)
# Get the ACI Details
try:
    with open("aml_config/aci_webservice.json") as f:
        config = json.load(f)
except:
    print("No new model, thus no deployment on ACI")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

service_name = config["aci_name"]
# Get the hosted web service
service = Webservice(name=service_name, workspace=ws)

# Input for Model with all features
input_j = [[200,3000,"Y",2,"Y","Y",100,100,10],[200,3000,"N",2,"N","N",130,100,5]]
print("Input model with all features")
print(input_j)
test_sample = json.dumps({"data": input_j})
test_sample = bytes(test_sample, encoding="utf8")
try:
    prediction = service.run(input_data=test_sample)
    print(prediction)
except Exception as e:
    result = str(e)
    print(result)
    raise Exception("ACI service is not working as expected")