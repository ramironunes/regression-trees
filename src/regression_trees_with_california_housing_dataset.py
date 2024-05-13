# -*- coding: utf-8 -*-
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 17:24:30
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-13 20:25:12


import os
import numpy as np
import pandas as pd

from graphviz import Source
from matplotlib import pyplot as plt

from sklearn import datasets
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


# Define the base path for resources
base_path: str = "src/resources"

# Create the directory if it does not exist
os.makedirs(base_path, exist_ok=True)

# Load the data
data = datasets.fetch_california_housing()
X: np.ndarray = data.data
y: np.ndarray = data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# Prepare DataFrame to store tree metrics
tree_metrics = pd.DataFrame(
    columns=[
        'Depth',
        'Train MSE',
        'Test MSE',
        'R² Score',
        'MAE',
        'RMSE',
        'Is Best',
    ]
)

# Evaluate trees of varying depths and find the best one
best_depth: int = 0
lowest_test_mse: float = float('inf')

# Train and evaluate trees of varying depths
for depth in range(1, 6):  # Adjust the range if you want to evaluate more trees
    regressor = DecisionTreeRegressor(max_depth=depth)
    regressor.fit(X_train, y_train)

    # Predict and evaluate
    y_train_pred: np.ndarray = regressor.predict(X_train)
    y_test_pred: np.ndarray = regressor.predict(X_test)
    train_mse: float = mean_squared_error(y_train, y_train_pred)
    test_mse: float = mean_squared_error(y_test, y_test_pred)
    r2: float = r2_score(y_test, y_test_pred)
    mae: float = mean_absolute_error(y_test, y_test_pred)
    rmse: float = np.sqrt(test_mse)

    # Store metrics in DataFrame using concat
    is_best: str = 'no'
    if test_mse < lowest_test_mse:
        lowest_test_mse = test_mse
        best_depth = depth
        tree_metrics['Is Best'] = 'no'  # Reset previous bests
        is_best = 'yes'

    new_row: dict = {
        'Depth': depth,
        'Train MSE': train_mse,
        'Test MSE': test_mse,
        'R² Score': r2,
        'MAE': mae,
        'RMSE': rmse,
        'Is Best': is_best,
    }
    tree_metrics = pd.concat(
        [tree_metrics, pd.DataFrame([new_row])],
        ignore_index=True,
    )

    dot_data: str = export_graphviz(
        regressor,
        out_file=None,
        feature_names=data.feature_names,
        filled=True,
        rounded=True,
        special_characters=True,
    )
    graph = Source(dot_data)
    graph.render(
        f"{base_path}/img/california_housing_tree_depth_{depth}",
        format="png",
        view=True,
    )

    print(
        f"Tree Depth: {depth}, Train MSE: {train_mse:.2f}, Test MSE: " + \
        f"{test_mse:.2f}, R²: {r2:.2f}, MAE: {mae:.2f}, RMSE: {rmse:.2f}"
    )

tree_metrics.to_excel(
    f"{base_path}/test/tree_metrics_california_housing.xlsx",
    index=False,
)
print(f"Metrics saved to {base_path}/test/tree_metrics_california_housing.xlsx")
print(
    f"The best performing tree is at depth {best_depth} with Test MSE: " + \
    f"{lowest_test_mse:.2f}, based on the criteria of lowest Test MSE."
)

# Display the DataFrame
print(tree_metrics)

# Visualizing the decision tree for the best model
best_tree = DecisionTreeRegressor(max_depth=best_depth)
best_tree.fit(X_train, y_train)
dot_data: str = export_graphviz(
    best_tree,
    out_file=None,
    feature_names=data.feature_names,
    filled=True,
    rounded=True,
    special_characters=True,
)
graph = Source(dot_data)
graph.render(
    f"{base_path}/img/california_housing_best_tree_depth_{best_depth}",
    format='png',
)

# Optionally, plot MSE and R² Score from the DataFrame
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(
    tree_metrics['Depth'],
    tree_metrics['Test MSE'],
    marker='o',
    label='Test MSE',
)
plt.plot(
    tree_metrics['Depth'],
    tree_metrics['Train MSE'],
    marker='o',
    label='Train MSE',
)
plt.xlabel('Depth of Tree')
plt.ylabel('MSE')
plt.title('MSE by Tree Depth')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(
    tree_metrics['Depth'],
    tree_metrics['R² Score'],
    marker='o',
    color='r',
    label='R² Score',
)
plt.xlabel('Depth of Tree')
plt.ylabel('R² Score')
plt.title('R² Score by Tree Depth')
plt.tight_layout()
plt.legend()
plt.show()
