import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from .models import InsuranceProduct, Customer

def train_model():
    # Load data from your database
    customers = Customer.objects.all().values()
    data = pd.DataFrame(list(customers))
    
    # Preprocess data
    data = preprocess_data(data)
    
    # Split features and target
    X = data.drop('recommended_product', axis=1)
    y = data['recommended_product']
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    return model, scaler

def preprocess_data(data):
    # Handle missing values
    data = data.dropna()
    
    # Encode categorical variables
    data = pd.get_dummies(data, columns=['gender', 'occupation', 'marital_status'])
    
    # Feature engineering
    data = engineer_features(data)
    
    # Ensure 'recommended_product' column exists
    if 'recommended_product' not in data.columns:
        # If it doesn't exist, you might want to create it based on some logic
        # For example, you could use the most common insurance product for each customer
        most_common_product = InsuranceProduct.objects.all().first()  # This is a simplification
        data['recommended_product'] = most_common_product.id
    
    return data

def engineer_features(data):
    # Calculate age from birth date if it exists
    if 'birth_date' in data.columns:
        data['age'] = (pd.Timestamp.now() - pd.to_datetime(data['birth_date'])).astype('<m8[Y]')
    
    # Create risk score based on age, income, and credit score
    data['risk_score'] = (data['age'] * 0.2 + data['income'] * 0.5 + data['credit_score'] * 0.3) / 100
    
    # Create family size feature
    data['family_size'] = data['number_of_dependents'] + 1
    
    return data

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

