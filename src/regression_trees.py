# -*- coding: utf-8 -*-
# @Author: Ramiro Luiz Nunes
# @Date:   2024-05-12 13:38:12
# @Last Modified by:   Ramiro Luiz Nunes
# @Last Modified time: 2024-05-12 13:59:30


import numpy as np
import time

from graphviz import Source
from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import export_graphviz


# Load the data
data = datasets.load_diabetes()
X: np.ndarray = data.data
y: np.ndarray = data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start the timer to calculate training time
start_time: float = time.time()

# Train a regression tree
regressor: DecisionTreeRegressor = DecisionTreeRegressor(max_depth=4)
regressor.fit(X_train, y_train)

# Calculate the training time
training_time: float = time.time() - start_time

# Predict the values for the test set
y_pred: np.ndarray = regressor.predict(X_test)

# Performance metrics
mse: float = mean_squared_error(y_test, y_pred)
r2: float = r2_score(y_test, y_pred)

# Visualize the tree
dot_data: str = export_graphviz(
    regressor, out_file=None, feature_names=data.feature_names,
    filled=True, rounded=True, special_characters=True
)
graph: Source = Source(dot_data)
graph.render("diabetes_tree", format="png", view=True)

# Display metrics and training time
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")
print(f"Training Time: {training_time:.2f} seconds")

# Plot the feature importance
feature_importances: np.ndarray = regressor.feature_importances_
plt.figure(figsize=(10, 7))
plt.barh(data.feature_names, feature_importances)
plt.xlabel('Feature Importance')
plt.title('Feature Importance for the Regression Tree Model')
plt.show()
