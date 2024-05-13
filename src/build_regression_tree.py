# -*- coding: utf-8 -*-
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-13 20:18:11
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-13 20:36:09


import os
import pandas as pd

from graphviz import Source
from sklearn.tree import DecisionTreeRegressor, export_graphviz


# Directory to save the tree dataset
package_path = 'src/resources/boston_housing/'
# Check if the directory exists, if not, create it
if not os.path.exists(package_path):
    os.makedirs(package_path)

dataset_path = 'src/resources/boston_housing/dataset/'
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Load the Boston Housing dataset from an Excel file
file_path: str = f'{dataset_path}BostonHousing.xlsx'
df = pd.read_excel(file_path)

# Automatically identify the target column
# (assume the last column is the target)
target_column: str = df.columns[-1]

# Separate features and target
X = df.drop(columns=[target_column])
y = df[target_column]

# Train the regression tree
tree_regressor = DecisionTreeRegressor()
tree_regressor.fit(X, y)

# Export the regression tree to a DOT file
dot_data = export_graphviz(
    tree_regressor,
    out_file=None,
    feature_names=X.columns,
    filled=True,
    rounded=True,
    special_characters=True,
)

img_path: str = f"{package_path}/img"
if not os.path.exists(img_path):
    os.makedirs(img_path)

# Use Graphviz to visualize the tree
graph = Source(dot_data, format='png')
# Save the tree image to a file
graph.render(
    f"{img_path}/boston_housing_tree",
    format='png',
)
# Show the tree
graph.view()
