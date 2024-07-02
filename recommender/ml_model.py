import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from .models import InsuranceProduct

def train_model():
    # Load data from your database or CSV file
    # Preprocess data
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def get_recommendations(model, customer, top_n=3):
    # Preprocess customer data
    customer_data = pd.DataFrame({
        'age': [customer.age],
        'income': [customer.income],
        'credit_score': [customer.credit_score],
        'gender': [customer.gender],
        'occupation': [customer.occupation],
        'marital_status': [customer.marital_status],
        'number_of_dependents': [customer.number_of_dependents]
    })
    
    # Feature engineering
    customer_data = engineer_features(customer_data)
    
    # Get model predictions
    probabilities = model.predict_proba(customer_data)
    
    # Get top N recommendations
    top_indices = probabilities.argsort()[0][-top_n:][::-1]
    top_products = [InsuranceProduct.objects.get(id=i+1) for i in top_indices]
    top_scores = probabilities[0][top_indices]
    
    return list(zip(top_products, top_scores))

def engineer_features(data):
    # Implement feature engineering as before
    return data