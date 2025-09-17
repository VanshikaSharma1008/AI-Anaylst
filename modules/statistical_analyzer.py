import pandas as pd
import numpy as np

class StatisticalAnalyzer:
    """
    Class for performing statistical analysis on data.
    Provides methods for calculating descriptive statistics and correlations.
    """
    
    def __init__(self):
        """Initialize the StatisticalAnalyzer class."""
        pass
        
    def get_numerical_statistics(self, df):
        """
        Calculate descriptive statistics for numerical columns.
        
        Args:
            df (pandas.DataFrame): The input DataFrame
            
        Returns:
            pandas.DataFrame: DataFrame with statistics for numerical columns
        """
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return pd.DataFrame()
        
        # Calculate statistics
        stats = numeric_df.describe().T
        
        # Add additional statistics
        stats['median'] = numeric_df.median()
        stats['skew'] = numeric_df.skew()
        stats['kurtosis'] = numeric_df.kurtosis()
        stats['missing'] = numeric_df.isna().sum()
        stats['missing_pct'] = (numeric_df.isna().sum() / len(df) * 100).round(2)
        
        # Round values for better display
        stats = stats.round(2)
        
        return stats
    
    def get_categorical_statistics(self, df):
        """
        Calculate statistics for categorical columns.
        
        Args:
            df (pandas.DataFrame): The input DataFrame
            
        Returns:
            pandas.DataFrame: DataFrame with statistics for categorical columns
        """
        # Select non-numeric columns
        categorical_df = df.select_dtypes(exclude=['number'])
        
        if categorical_df.empty:
            return pd.DataFrame()
        
        # Initialize results DataFrame
        results = pd.DataFrame(
            index=categorical_df.columns,
            columns=['unique_values', 'top_value', 'top_count', 'top_percentage', 'missing', 'missing_pct', 'value_counts']
        )
        
        # Calculate statistics for each column
        for col in categorical_df.columns:
            value_counts = categorical_df[col].value_counts()
            results.loc[col, 'unique_values'] = len(value_counts)
            
            if not value_counts.empty:
                results.loc[col, 'top_value'] = value_counts.index[0]
                results.loc[col, 'top_count'] = value_counts.iloc[0]
                results.loc[col, 'top_percentage'] = (value_counts.iloc[0] / len(df) * 100).round(2)
            
            results.loc[col, 'missing'] = categorical_df[col].isna().sum()
            results.loc[col, 'missing_pct'] = (categorical_df[col].isna().sum() / len(df) * 100).round(2)
            
            # Store value counts as dictionary for later use
            results.loc[col, 'value_counts'] = value_counts.head(10).to_dict()
        
        return results
    
    def calculate_correlation_matrix(self, df):
        """
        Calculate correlation matrix for numerical columns.
        
        Args:
            df (pandas.DataFrame): The input DataFrame
            
        Returns:
            pandas.DataFrame: Correlation matrix
        """
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return pd.DataFrame()
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr().round(2)
        
        return corr_matrix
    
    def identify_outliers(self, df, column, method='iqr'):
        """
        Identify outliers in a numerical column.
        
        Args:
            df (pandas.DataFrame): The input DataFrame
            column (str): The column name to check for outliers
            method (str): Method to use for outlier detection ('iqr' or 'zscore')
            
        Returns:
            pandas.Series: Boolean series indicating outliers
        """
        if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
            return pd.Series(False, index=df.index)
        
        if method == 'iqr':
            # IQR method
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            return (df[column] < lower_bound) | (df[column] > upper_bound)
        
        elif method == 'zscore':
            # Z-score method
            mean = df[column].mean()
            std = df[column].std()
            z_scores = (df[column] - mean) / std
            return abs(z_scores) > 3
        
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")