import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit

def select_features_lasso(df, target_column, th=0, print_table=False):
    df = df.copy()

    X = df.drop(columns=[target_column]).copy()
    y = df[target_column].shift(-1).copy()

    X[target_column] = df[target_column]

    X = X.iloc[:-1].reset_index(drop=True)
    y = y.iloc[:-1].reset_index(drop=True)

    feature_names = X.columns

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    tscv = TimeSeriesSplit(n_splits=3)
    lasso = LassoCV(cv=tscv, random_state=2026, max_iter=10000)
    lasso.fit(X_scaled, y)

    coef = pd.Series(lasso.coef_, index=feature_names)

    selected_coef = coef[coef > th]

    importance_table = (
        selected_coef.to_frame("importance")
        .assign(abs_importance=lambda x: x["importance"].abs())
        .sort_values("abs_importance", ascending=False)
    )

    selected_features = importance_table.index.tolist()

    if print_table:
        print(importance_table)

    return selected_features

# def select_features_lasso(df, target_column, th = 0):
#     X = df.drop(columns=[target_column]).copy()
#     y = df[target_column].shift(-1)
    
#     X[f'{target_column}'] = df[target_column]
    
#     X = X.iloc[:-1]
#     y = y.iloc[:-1]
    
#     feature_names = X.columns
    
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
    
#     tscv = TimeSeriesSplit(n_splits=3)
#     lasso = LassoCV(cv=tscv, random_state=2026, max_iter=10000)
#     lasso.fit(X_scaled, y)
    
#     coef = pd.Series(lasso.coef_, index=feature_names)
#     selected_features = coef[coef > th].index.tolist()
    
#     print(f"Pradinis požymių skaičius: {len(feature_names)}")
#     print(f"Išlikusių požymių skaičius: {len(selected_features)}")
#     print(f"Geriausias lambda (alpha): {lasso.alpha_:.4f}")
#     print(f"Pašalinti požymiai: {list(set(feature_names) - set(selected_features))}")
    
#     return selected_features