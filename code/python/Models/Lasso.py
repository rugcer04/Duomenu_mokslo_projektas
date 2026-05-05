import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

def select_features_lasso(df, target_column):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    feature_names = X.columns
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    lasso = LassoCV(cv=5, random_state=2026, max_iter=10000)
    lasso.fit(X_scaled, y)
    
    coef = pd.Series(lasso.coef_, index=feature_names)
    selected_features = coef[coef != 0].index.tolist()
    
    print(f"Pradinis požymių skaičius: {len(feature_names)}")
    print(f"Išlikusių požymių skaičius: {len(selected_features)}")
    print(f"Geriausias lambda (alpha): {lasso.alpha_:.4f}")
    print(f"Pašalinti požymiai: {list(set(feature_names) - set(selected_features))}")
    
    return selected_features
