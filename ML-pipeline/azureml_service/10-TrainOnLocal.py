# This script triggers the run of ./notebooks/Training.py script on the local compute(Host agent in case of build pipeline). 
# The training script generates an output file aml_config/run_id.json which records the run_id and run history name of the training run. 
# The run_id.json is used by 20-RegisterModel.py to get the trained model.

# Source code reference: Microsoft Azure Machine Learning.

from azureml.core.runconfig import RunConfiguration
from azureml.core import Workspace
from azureml.core import Experiment
from azureml.core import ScriptRunConfig
import json
import os
from azureml.core.authentication import AzureCliAuthentication
cli_auth = AzureCliAuthentication()

# Get workspace
ws = Workspace.from_config(auth=cli_auth)

# Attach Experiment
experiment_name = "mldev-svm-creditexperiment"
exp = Experiment(workspace=ws, name=experiment_name)
print(exp.name, exp.workspace.name, sep="\n")

# Editing a run configuration property on-fly.
run_config_user_managed = RunConfiguration()
run_config_user_managed.environment.python.user_managed_dependencies = True

print("Submitting an experiment.")
src = ScriptRunConfig(
    source_directory=".",
    script="notebooks/Training.py",
    run_config=run_config_user_managed,
)

print("The current work directory in Train on Local", os.getcwd())

run = exp.submit(src)

# Shows output of the run on stdout.
run.wait_for_completion(show_output=True, wait_post_processing=True)

# Raise exception if run fails
if run.get_status() == "Failed":
    raise Exception(
        "Training on local failed with following run status: {} and logs: \n {}".format(
            run.get_status(), run.get_details_with_logs()
        )
    )

# Writing the run id to /aml_config/run_id.json

run_id = {}
run_id["run_id"] = run.id
run_id["experiment_name"] = run.experiment.name
with open("aml_config/run_id.json", "w") as outfile:
    json.dump(run_id, outfile)