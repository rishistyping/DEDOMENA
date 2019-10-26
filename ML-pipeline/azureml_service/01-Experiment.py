# Create an Experiment under Azure Machine Learning workspace
# Source code reference: Microsoft Azure Machine Learning

import os
from azureml.core import Experiment
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
cli_auth = AzureCliAuthentication()

def getExperiment():
    ws = Workspace.from_config(auth=cli_auth)
    script_folder = "."
    experiment_name = "mldev-svm-creditexperiment"
    exp = Experiment(workspace=ws, name=experiment_name)
    print(exp.name, exp.workspace.name, sep="\n")
    return exp


if __name__ == "__main__":
    exp = getExperiment()