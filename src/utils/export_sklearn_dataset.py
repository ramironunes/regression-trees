# -*- coding: utf-8 -*-
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 11:11:05
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-13 20:47:28


import os
import pandas as pd

from datetime import datetime
from typing import List, Tuple

from sklearn.datasets import (
    fetch_california_housing,
    load_diabetes,
    load_iris,
)


# Function to create directories for each dataset
def create_directories(base_path: str, dataset_name: str) -> Tuple[str, str]:
    # Format the dataset name to lower case with underscores
    formatted_name: str = dataset_name.lower().replace(' ', '_')
    # Define the main directory path
    dataset_dir: str = os.path.join(base_path, formatted_name)
    # Define the dataset and img subdirectories
    dataset_subdir: str = os.path.join(dataset_dir, 'dataset')
    img_subdir: str = os.path.join(dataset_dir, 'img')
    test_subdir: str = os.path.join(dataset_dir, 'test')

    # Create the directories if they do not exist
    os.makedirs(dataset_subdir, exist_ok=True)
    os.makedirs(img_subdir, exist_ok=True)
    os.makedirs(test_subdir, exist_ok=True)

    return dataset_subdir, img_subdir


# Base path for the resources
base_path = 'src/resources/'

# Tuple of datasets to be loaded and their respective function calls
datasets_to_load: List[Tuple[str, callable]] = [
    ('Iris', load_iris),
    ('Diabetes', load_diabetes),
    ('California Housing', fetch_california_housing)
]

# Function to load a dataset and save it to an Excel file
def dataset_to_excel(dataset_info: Tuple[str, callable]) -> None:
    dataset_name, dataset_function = dataset_info

    # Create directories for the dataset
    dataset_subdir, img_subdir = create_directories(base_path, dataset_name)

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
        file_path: str = os.path.join(dataset_subdir, f"{dataset_name}.xlsx")

        # Save the dataframe to an Excel file in the 'dataset' folder with a custom sheet name
        df.to_excel(file_path, index=False, sheet_name=current_time)
        print(f"{dataset_name} dataset saved to {file_path} in sheet {current_time}")
    except Exception as e:
        print(f"ERROR: Failed to load {dataset_name}: {e}")

# Process each dataset
for dataset_info in datasets_to_load:
    dataset_to_excel(dataset_info)


# Function to load the Boston Housing dataset and save it to an Excel file
def load_boston_housing_dataset() -> None:
    dataset_name = 'Boston Housing'

    # Create directories for the dataset
    dataset_subdir, img_subdir = create_directories(base_path, dataset_name)

    # URL of the Boston dataset
    url = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
    # Load the dataset into a pandas DataFrame
    boston = pd.read_csv(url)
    # Current datetime for sheet naming
    current_time: str = datetime.now().strftime("%Y%m%d-%H%M%S")
    # Save the DataFrame to an Excel spreadsheet in .xlsx format
    file_path: str = os.path.join(dataset_subdir, f"{dataset_name}.xlsx")
    boston.to_excel(file_path, index=False, sheet_name=current_time)
    print(f"Boston Housing dataset saved to {file_path} in sheet {current_time}")
    print("Excel spreadsheet 'BostonHousing.xlsx' generated successfully.")

load_boston_housing_dataset()
