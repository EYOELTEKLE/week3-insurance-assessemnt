import pandas as pd
import numpy as np

class EDAAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Convert TransactionMonth to datetime if it's not already
        if 'TransactionMonth' in self.df.columns and not pd.api.types.is_datetime64_any_dtype(self.df['TransactionMonth']):
            self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'], errors='coerce')

    def get_data_info(self):
        """Print DataFrame info (dtypes, non-nulls, etc.)."""
        return self.df.info()

    def get_summary_statistics(self):
        """Return descriptive statistics for numerical columns."""
        return self.df.describe()

    def check_missing_values(self):
        """Return a summary of missing values per column."""
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        return pd.DataFrame({
            'missing_count': missing,
            'missing_percentage': missing_pct
        }).sort_values('missing_count', ascending=False)

    def calculate_loss_ratio(self, group_by=None):
        """
        Calculate loss ratio (TotalClaims / TotalPremium).
        If group_by is provided, calculate by that column.
        """
        if group_by is None:
            total_claims = self.df['TotalClaims'].sum()
            total_premium = self.df['TotalPremium'].sum()
            if total_premium == 0:
                return float('nan')
            return total_claims / total_premium
        else:
            grouped = self.df.groupby(group_by).agg({
                'TotalClaims': 'sum',
                'TotalPremium': 'sum'
            })
            grouped['LossRatio'] = grouped['TotalClaims'] / grouped['TotalPremium']
            return grouped[['LossRatio']].sort_values('LossRatio', ascending=False)

    def analyze_claims_by_vehicle(self, top_n=10):
        """
        Return average claim amount by vehicle make (top N).
        """
        if 'make' not in self.df.columns or 'TotalClaims' not in self.df.columns:
            return None
        claims_by_make = self.df.groupby('make')['TotalClaims'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        claims_by_make.columns = ['AvgClaimAmount', 'Count']
        return claims_by_make.head(top_n)

    def analyze_temporal_trends(self):
        """
        Analyze trends over time using TransactionMonth.
        """
        if 'TransactionMonth' not in self.df.columns:
            return None
        
        monthly_stats = self.df.groupby(self.df['TransactionMonth'].dt.to_period('M')).agg({
            'TotalClaims': ['sum', 'mean', 'count'],
            'TotalPremium': ['sum', 'mean'],
            'PolicyID': 'count'
        })
        
        monthly_stats.columns = ['_'.join(col).strip() for col in monthly_stats.columns.values]
        monthly_stats['LossRatio'] = monthly_stats['TotalClaims_sum'] / monthly_stats['TotalPremium_sum']
        
        return monthly_stats

    def analyze_vehicle_characteristics(self):
        """
        Analyze vehicle-related characteristics and their impact on claims.
        """
        vehicle_cols = ['VehicleType', 'make', 'Model', 'RegistrationYear', 
                       'Cylinders', 'cubiccapacity', 'kilowatts', 'bodytype']
        
        analysis = {}
        for col in vehicle_cols:
            if col in self.df.columns:
                stats = self.df.groupby(col).agg({
                    'TotalClaims': ['mean', 'sum', 'count'],
                    'TotalPremium': ['mean', 'sum']
                })
                stats.columns = ['_'.join(col).strip() for col in stats.columns.values]
                stats['LossRatio'] = stats['TotalClaims_sum'] / stats['TotalPremium_sum']
                analysis[col] = stats.sort_values('TotalClaims_mean', ascending=False)
        
        return analysis

