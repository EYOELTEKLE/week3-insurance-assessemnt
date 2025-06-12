import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Set style
        # plt.style.use('seaborn')
        sns.set_palette("husl")

    def plot_distributions(self, numerical_cols):
        """Plot histograms for given numerical columns."""
        n = len(numerical_cols)
        plt.figure(figsize=(5 * n, 4))
        for i, col in enumerate(numerical_cols, 1):
            plt.subplot(1, n, i)
            sns.histplot(self.df[col].dropna(), kde=True, bins=30)
            plt.title(f'Distribution of {col}')
        plt.tight_layout()
        plt.show()

    def plot_boxplots(self, numerical_cols):
        """Plot boxplots for given numerical columns (outlier detection)."""
        n = len(numerical_cols)
        plt.figure(figsize=(5 * n, 4))
        for i, col in enumerate(numerical_cols, 1):
            plt.subplot(1, n, i)
            sns.boxplot(y=self.df[col].dropna())
            plt.title(f'Boxplot of {col}')
        plt.tight_layout()
        plt.show()

    def plot_loss_ratio_by_category(self, category_col):
        """Bar plot of loss ratio by a categorical column."""
        if 'TotalClaims' not in self.df.columns or 'TotalPremium' not in self.df.columns:
            print('Required columns not found.')
            return
        grouped = self.df.groupby(category_col).agg({'TotalClaims': 'sum', 'TotalPremium': 'sum'})
        grouped['LossRatio'] = grouped['TotalClaims'] / grouped['TotalPremium']
        grouped = grouped.sort_values('LossRatio', ascending=False)
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=grouped.index, y=grouped['LossRatio'])
        plt.title(f'Loss Ratio by {category_col}')
        plt.ylabel('Loss Ratio')
        plt.xlabel(category_col)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_claims_by_make(self, top_n=10):
        """Bar plot of average claim amount by top N vehicle makes."""
        if 'make' not in self.df.columns or 'TotalClaims' not in self.df.columns:
            print('Required columns not found.')
            return
        
        claims_by_make = self.df.groupby('make')['TotalClaims'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        claims_by_make = claims_by_make.head(top_n)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=claims_by_make.index, y=claims_by_make['mean'])
        plt.title(f'Average Claim Amount by Top {top_n} Vehicle Makes')
        plt.ylabel('Average Claim Amount')
        plt.xlabel('Vehicle Make')
        plt.xticks(rotation=45, ha='right')
        
        # Add count annotations
        for i, (make, row) in enumerate(claims_by_make.iterrows()):
            plt.text(i, row['mean'], f'n={int(row["count"])}', 
                    ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()

    def plot_temporal_trends(self):
        """Plot temporal trends in claims and premiums."""
        if 'TransactionMonth' not in self.df.columns:
            print('TransactionMonth column not found.')
            return
            
        monthly = self.df.groupby(self.df['TransactionMonth'].dt.to_period('M')).agg({
            'TotalClaims': 'sum',
            'TotalPremium': 'sum',
            'PolicyID': 'count'
        })
        monthly['LossRatio'] = monthly['TotalClaims'] / monthly['TotalPremium']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Claims and Premiums
        ax1.plot(monthly.index.astype(str), monthly['TotalClaims'], label='Total Claims', color='tab:red')
        ax1.plot(monthly.index.astype(str), monthly['TotalPremium'], label='Total Premium', color='tab:blue')
        ax1.set_title('Monthly Total Claims and Premiums')
        ax1.set_ylabel('Amount')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Loss Ratio
        ax2.plot(monthly.index.astype(str), monthly['LossRatio'], color='tab:green')
        ax2.set_title('Monthly Loss Ratio')
        ax2.set_ylabel('Loss Ratio')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()

    def plot_vehicle_characteristics(self, characteristic):
        """Plot vehicle characteristics and their impact on claims."""
        if characteristic not in self.df.columns or 'TotalClaims' not in self.df.columns:
            print('Required columns not found.')
            return
            
        plt.figure(figsize=(12, 6))
        sns.boxplot(x=characteristic, y='TotalClaims', data=self.df)
        plt.title(f'Claims Distribution by {characteristic}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

