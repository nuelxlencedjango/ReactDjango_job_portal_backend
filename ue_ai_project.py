import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE

# Step 1: Load the Dataset
# Dataset is assumed to be already loaded. We will work with the columns:
# ['id', 'age', 'sex', 'dataset', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
#  'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num']

# Assuming 'num' column is the target variable (0 = no heart disease, 1 = heart disease)
data = pd.read_csv('heart.csv')

# Step 2: Data Preprocessing

# Drop unnecessary 'id' and 'dataset' columns
data = data.drop(columns=['id', 'dataset'])

# Check for null values and handle them
print("Missing values in each column:")
print(data.isnull().sum())

# If missing values exist, you can handle them (e.g., fill with the mean or mode)
# For simplicity, we'll drop rows with missing values
data = data.dropna()

# Check data types and perform any necessary encoding
data['sex'] = data['sex'].astype(int)  # Converting categorical to numerical if needed (already in numeric format)

# Step 3: Feature Selection (X) and Target Variable (y)
X = data.drop(columns=['num'])  # Features (all columns except the target 'num')
y = data['num']  # Target

# Step 4: Split Data into Training and Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Standardize the Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------- Ablation Study --------------------
# Ablation Study: Evaluate model performance by removing features one at a time

def ablation_study(X, y):
    results = {}
    for feature in X.columns:
        X_ablation = X.drop([feature], axis=1)  # Drop one feature
        X_train, X_test, y_train, y_test = train_test_split(X_ablation, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        results[feature] = accuracy
    return results

ablation_results = ablation_study(X, y)
print("\nAblation Study Results (Accuracy per feature removal):")
for feature, accuracy in ablation_results.items():
    print(f"Feature '{feature}' removal: Accuracy = {accuracy}")

# -------------------- Model Stability Study --------------------
# Stability Study: Use cross-validation to test model stability

def model_stability(X, y, model):
    scores = cross_val_score(model, X, y, cv=5)  # 5-fold cross-validation
    return scores.mean()

# Testing with all models
models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Naive Bayes': GaussianNB(),
    'Logistic Regression': LogisticRegression(random_state=42)
}

for model_name, model in models.items():
    stability_score = model_stability(X_train_scaled, y_train, model)
    print(f"\nModel Stability ({model_name}, 5-fold CV): {stability_score}")

# -------------------- Attribute Selection Study --------------------
# Attribute Selection using Recursive Feature Elimination (RFE)

def attribute_selection(X, y):
    model = LogisticRegression(random_state=42)
    selector = RFE(model, n_features_to_select=5)  # Select top 5 features
    X_selected = selector.fit_transform(X, y)
    return X_selected, selector.support_

X_selected, selected_features = attribute_selection(X, y)
print("\nSelected features after RFE:")
print(X.columns[selected_features])

# -------------------- Fairness and Bias Study --------------------
# Fairness Study: Compare performance across subgroups (e.g., sex)

def fairness_study(X, y, subgroup_column):
    model = LogisticRegression(random_state=42)
    model.fit(X, y)
    subgroup = X[subgroup_column]
    subgroup_accuracy = {}
    for group in subgroup.unique():
        group_data = X[subgroup == group]
        group_target = y[subgroup == group]
        group_pred = model.predict(group_data)
        group_accuracy = accuracy_score(group_target, group_pred)
        subgroup_accuracy[group] = group_accuracy
    return subgroup_accuracy

fairness_results = fairness_study(X, y, 'sex')
print("\nFairness Study Results (Accuracy by Sex):")
for group, accuracy in fairness_results.items():
    print(f"Group '{group}': Accuracy = {accuracy}")

# -------------------- Computation Time vs Performance --------------------
# Measure time for training and prediction

def measure_computation_time(model, X_train, y_train, X_test, y_test):
    start_time = time.time()
    model.fit(X_train, y_train)  # Train the model
    training_time = time.time() - start_time
    
    start_time = time.time()
    y_pred = model.predict(X_test)  # Test the model
    prediction_time = time.time() - start_time
    
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy, training_time, prediction_time

# Measure for all models
for model_name, model in models.items():
    accuracy, training_time, prediction_time = measure_computation_time(model, X_train_scaled, y_train, X_test_scaled, y_test)
    print(f"\n{model_name} - Accuracy: {accuracy}, Training Time: {training_time}s, Prediction Time: {prediction_time}s")

# -------------------- Sampling Comparison (Correct vs Incorrect Sampling) --------------------
# SMOTE (Synthetic Minority Over-sampling Technique) for resampling
def sampling_comparison(X, y):
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Train the model on resampled data
    model = LogisticRegression(random_state=42)
    model.fit(X_resampled, y_resampled)
    y_pred = model.predict(X_test_scaled)
    
    accuracy_resampled = accuracy_score(y_test, y_pred)
    return accuracy_resampled

accuracy_resampled = sampling_comparison(X, y)
print(f"\nAccuracy after SMOTE Resampling: {accuracy_resampled}")
