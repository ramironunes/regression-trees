# -*- coding: utf-8 -*-
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 11:11:05
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-12 13:31:51


import os
import pandas as pd

from datetime import datetime
from typing import List, Tuple

from sklearn.datasets import (
    fetch_california_housing,
    load_diabetes,
    load_iris,
)


# Create 'dataset' directory if it does not exist
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Tuple of datasets to be loaded and their respective function calls
datasets_to_load: List[Tuple[str, callable]] = [
    ('Iris', load_iris),
    ('Diabetes', load_diabetes),
    ('California Housing', fetch_california_housing)
]

# Function to load a dataset and save it to an Excel file
def dataset_to_excel(dataset_info: Tuple[str, callable]) -> None:
    dataset_name, dataset_function = dataset_info

    # Try to load the dataset and handle potential errors
    try:
        data = dataset_function()
        df = pd.DataFrame(data=data.data, columns=data.feature_names)
        df['Target'] = data.target

        # If the dataset has target names, map these to the target column
        if hasattr(data, 'target_names'):
            target_name_map: dict = {
                i: name for i, name in enumerate(data.target_names)
            }
            df['Target Name'] = df['Target'].map(target_name_map)

        # Current datetime for sheet naming
        current_time: str = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Define the file path for the Excel file
        file_path: str = f"dataset/{dataset_name}.xlsx"

        # Save the dataframe to an Excel file in the 'dataset' folder with a custom sheet name
        df.to_excel(file_path, index=False, sheet_name=current_time)
        print(f"{dataset_name} dataset saved to {file_path} in sheet {current_time}")
    except Exception as e:
        print(f"ERROR: Failed to load {dataset_name}: {e}")

# Process each dataset
for dataset_info in datasets_to_load:
    dataset_to_excel(dataset_info)
