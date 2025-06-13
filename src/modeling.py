import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import shap

class DataPreparer:
    def __init__(self, df):
        self.df = df.copy()
    def handle_missing(self):
        missing = self.df.isnull().mean()
        self.df = self.df.drop(columns=missing[missing > 0.3].index)
        imputer = SimpleImputer(strategy='median')
        for col in self.df.select_dtypes(include='number').columns:
            self.df[col] = imputer.fit_transform(self.df[[col]])
        for col in self.df.select_dtypes(include='object').columns:
            self.df[col] = self.df[col].fillna('Unknown')
        return self.df
    def feature_engineering(self):
        if 'VehicleYear' in self.df.columns and 'TransactionMonth' in self.df.columns:
            self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'], errors='coerce')
            self.df['VehicleAge'] = self.df['TransactionMonth'].dt.year - self.df['VehicleYear']
        return self.df
    def encode_categoricals(self):
        return pd.get_dummies(self.df, columns=self.df.select_dtypes(include='object').columns, drop_first=True)

class ClaimSeverityModel:
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        if model_type == 'linear':
            self.model = LinearRegression()
        elif model_type == 'rf':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            self.model = XGBRegressor(n_estimators=100, random_state=42)
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    def predict(self, X):
        return self.model.predict(X)
    def evaluate(self, y_true, y_pred):
        rmse = mean_squared_error(y_true, y_pred) ** 0.5
        r2 = r2_score(y_true, y_pred)
        return {'RMSE': rmse, 'R2': r2}
    def shap_summary(self, X):
        explainer = shap.Explainer(self.model)
        shap_values = explainer(X)
        return shap_values

class ClaimProbabilityModel:
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        if model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            self.model = XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss', random_state=42)
    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
    def predict(self, X):
        return self.model.predict(X)
    def predict_proba(self, X):
        return self.model.predict_proba(X)[:,1]
    def evaluate(self, y_true, y_pred):
        return {
            'Accuracy': accuracy_score(y_true, y_pred),
            'Precision': precision_score(y_true, y_pred),
            'Recall': recall_score(y_true, y_pred),
            'F1': f1_score(y_true, y_pred),
            'ROC_AUC': roc_auc_score(y_true, y_pred)
        }

# Utility function for premium calculation
def calculate_risk_based_premium(prob_claim, severity_pred, expense_loading=500, profit_margin=0.1):
    risk_based_premium = prob_claim * severity_pred + expense_loading
    risk_based_premium = risk_based_premium * (1 + profit_margin)
    return risk_based_premium
