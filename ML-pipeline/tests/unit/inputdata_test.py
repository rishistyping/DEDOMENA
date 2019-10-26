# This script checks the input dataset using Pytest for the machine learning experiment.
# Sample unit testing for the workshop.

# Soure code reference: Microsoft Azure Machine Learning

import os
import numpy as np
import pandas as pd


# Get absolute path of csv files from data folder in your git repository.
def get_absPath(filename):
    """Returns the path of the notebooks folder"""
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), os.path.pardir, os.path.pardir, "data", filename
        )
    )
    return path


# Expected Number of features in the input data
expected_columns = 11

# Check the Input data exists 
def test_check_schema():
    datafile = get_absPath("creditcardcsvpresent.csv")
    # check that file exists
    assert os.path.exists(datafile)
    dataset = pd.read_csv(datafile)
    header = dataset[dataset.columns[:-1]]
    actual_columns = header.shape[1]
    # check header has expected number of columns
    assert actual_columns == expected_columns

# Check the missing values in the input data
def test_check_missing_values():
    datafile = get_absPath("creditcardcsvpresent.csv")
    # check that file exists
    assert os.path.exists(datafile)
    dataset = pd.read_csv(datafile)
    missing_value = dataset.isnull().sum().max()
    assert missing_value > 0