# This script reads the image.json which is published as an artifact from build pipeline.
# It also creates Azure Container Instance cluster and deploy the scoring web service on it. It writes the scoring service details to aci_webservice.json file.

# Source code reference: Microsoft Azure Machine Learning

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
ws = Workspace.from_config(auth=cli_auth)# Get the Image to deploy details

try:
    with open("aml_config/image.json") as f:
        config = json.load(f)
except:
    print("No new model, thus no deployment on ACI")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)


image_name = config["image_name"]
image_version = config["image_version"]

images = Image.list(workspace=ws)
image, = (m for m in images if m.version == image_version and m.name == image_name)
print(
    "From image.json, Image used to deploy webservice on ACI: {}\nImage Version: {}\nImage Location = {}".format(
        image.name, image.version, image.image_location
    )
)


aciconfig = AciWebservice.deploy_configuration(
    cpu_cores=1,
    memory_gb=1,
    location="canadacentral",
    tags={"area": "credittransactions", "type": "classification"},
    description="ml webservice to detect fradulent transactions",
)

print("cureent workspace", ws.name)
print(aciconfig) 

aci_service_name = "acicreditmldevops" + datetime.datetime.now().strftime("%m%d%H")

service = Webservice.deploy_from_image(
    deployment_config=aciconfig, image=image, name=aci_service_name, workspace=ws
)

service.wait_for_deployment()
print(
    "Deployed ACI Webservice: {} \nWebservice Uri: {}".format(
        service.name, service.scoring_uri
    )
)

# Writing the ACI details to /aml_config/aci_webservice.json
aci_webservice = {}
aci_webservice["aci_name"] = service.name
aci_webservice["aci_url"] = service.scoring_uri
with open("aml_config/aci_webservice.json", "w") as outfile:
    json.dump(aci_webservice, outfile)