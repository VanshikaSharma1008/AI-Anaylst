import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

class DataProcessor:
    """
    Class for processing and cleaning data from CSV/XLSX files.
    Handles missing values, standardizes formats, and removes duplicates.
    """
    
    def __init__(self):
        """Initialize the DataProcessor class."""
        self.numeric_imputer = SimpleImputer(strategy='mean')
        self.categorical_imputer = SimpleImputer(strategy='most_frequent')
        self.scaler = StandardScaler()
        
    def process_data(self, df):
        """
        Process the input DataFrame by cleaning and standardizing it.
        
        Args:
            df (pandas.DataFrame): The input DataFrame to process
            
        Returns:
            pandas.DataFrame: The processed DataFrame
        """
        # Make a copy to avoid modifying the original
        processed_df = df.copy()
        
        # Basic cleaning
        processed_df = self._remove_duplicates(processed_df)
        processed_df = self._handle_missing_values(processed_df)
        processed_df = self._standardize_formats(processed_df)
        
        return processed_df
    
    def _remove_duplicates(self, df):
        """Remove duplicate rows from the DataFrame."""
        return df.drop_duplicates()
    
    def _handle_missing_values(self, df):
        """
        Handle missing values in the DataFrame.
        - For numeric columns: impute with mean
        - For categorical columns: impute with most frequent value
        """
        # Separate numeric and categorical columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(exclude=['number']).columns
        
        # Handle numeric columns
        if len(numeric_cols) > 0:
            df[numeric_cols] = self.numeric_imputer.fit_transform(df[numeric_cols])
        
        # Handle categorical columns
        if len(categorical_cols) > 0:
            for col in categorical_cols:
                # Convert to string to handle mixed types
                df[col] = df[col].astype(str)
                # Replace empty strings with NaN
                df[col] = df[col].replace('', np.nan)
                # Replace 'nan' strings with NaN
                df[col] = df[col].replace('nan', np.nan)
                
            # Impute missing values
            df[categorical_cols] = self.categorical_imputer.fit_transform(df[categorical_cols])
        
        return df
    
    def _standardize_formats(self, df):
        """
        Standardize formats in the DataFrame:
        - Convert date columns to datetime
        - Standardize text case for string columns
        - Convert numeric strings to numbers
        """
        # Try to convert string columns that might be dates
        for col in df.select_dtypes(include=['object']).columns:
            # Check if column might contain dates
            try:
                # Try to convert to datetime
                df[col] = pd.to_datetime(df[col], errors='coerce')
                # If more than 70% converted successfully, keep as datetime
                if df[col].notna().sum() / len(df) < 0.7:
                    # Revert back to original if too many NaT values
                    df[col] = df[col].astype(str)
            except:
                pass
            
            # If still string type, standardize text
            if df[col].dtype == 'object':
                # Try to convert to numeric if possible
                numeric_series = pd.to_numeric(df[col], errors='coerce')
                # If more than 70% converted successfully, keep as numeric
                if numeric_series.notna().sum() / len(df) > 0.7:
                    df[col] = numeric_series
                else:
                    # Otherwise, standardize string format (lowercase)
                    df[col] = df[col].str.strip().str.lower()
        
        return df
    
    def get_column_types(self, df):
        """
        Identify column types in the DataFrame.
        
        Returns:
            dict: Dictionary with lists of column names by type
        """
        column_types = {
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object', 'category']).columns.tolist(),
            'datetime_columns': df.select_dtypes(include=['datetime']).columns.tolist()
        }
        return column_types