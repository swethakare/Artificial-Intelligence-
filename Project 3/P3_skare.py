'''
Created on Apr 30, 2023

@author: Swetha Kare
GID: G01378458
'''
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import export_text
import pandas as pd

def print_decision_tree(decision_tree, feature_names):
    tree_rules = export_text(decision_tree, feature_names=feature_names)
    print("Decision Tree for the Training Data:\n", tree_rules)
          
def decisiontree():
# Load the wine dataset
    col_names = ['Type','Alcohol','MalicAcid','Ash','Alcalinity','Magnesium','Phenols','Flavanoids','Nonflavanoid','Proanthocyanins','ColorIntensity','Hue','DilutedWines','Proline']
    pima = pd.read_csv("wines.csv", header=None, names=col_names)#
    pima.head()
    #split dataset in features and target variable
    feature_cols = ['Alcohol','MalicAcid','Ash','Alcalinity','Magnesium','Phenols','Flavanoids','Nonflavanoid','Proanthocyanins','ColorIntensity','Hue','DilutedWines','Proline']
    X = pima[feature_cols] # Feature variables
    y = pima.Type #target variable
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    # Define the decision tree classifier
    decision_tree = DecisionTreeClassifier()
    # Define the hyperparameters to tune
    parameters = {'criterion':  ['entropy'],
        'max_depth':  [3,4],
        'max_features': [None],
        'splitter': ['random'],
        'random_state':[1]}
    # Perform a grid search to find the best hyperparameters
    grid_search = GridSearchCV(decision_tree, parameters, cv=5)
    grid_search.fit(X_train, y_train)
    # Print the best hyperparameters found by GridSearchCV
    print("Best hyperparameters:", grid_search.best_params_)
    # Train a decision tree classifier with the best hyperparameters
    best_decision_tree = DecisionTreeClassifier(criterion=grid_search.best_params_['criterion'], 
                                                max_depth=grid_search.best_params_['max_depth'], 
                                                max_features=grid_search.best_params_['max_features'], 
                                                splitter=grid_search.best_params_['splitter'],
                                                random_state=grid_search.best_params_['random_state'])
    
    best_decision_tree.fit(X_train, y_train)
    print_decision_tree(best_decision_tree, X.columns.tolist())
    
    # Use the trained decision tree to predict classes for the test data
    predictions = best_decision_tree.predict(X_test)
    print("Predicted classes for the Test Data: ", predictions)
    # Calculate the accuracy of the predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy of the Predictions on the Test Data: ", accuracy)

#Initially call the decision tree    
decisiontree()