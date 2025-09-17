import traceback
import logging
import os
from datetime import datetime

class ErrorHandler:
    """
    Class for handling errors and exceptions in the data analysis system.
    Provides logging, user-friendly error messages, and error tracking.
    """
    
    def __init__(self):
        """Initialize the ErrorHandler class."""
        # Set up logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Set up logging configuration."""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Set up logger
        self.logger = logging.getLogger('data_analyst_agent')
        self.logger.setLevel(logging.DEBUG)
        
        # Create file handler
        log_filename = f"logs/data_analyst_agent_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    
    def handle_error(self, exception, context=""):
        """
        Handle an exception by logging it and returning a user-friendly message.
        
        Args:
            exception (Exception): The exception to handle
            context (str): Additional context about where the error occurred
            
        Returns:
            str: User-friendly error message
        """
        # Get exception details
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()
        
        # Log the error
        self.logger.error(f"Error in {context}: {error_type} - {error_message}")
        self.logger.debug(f"Stack trace: {stack_trace}")
        
        # Generate user-friendly message
        user_message = self._generate_user_message(error_type, error_message, context)
        
        return user_message
    
    def _generate_user_message(self, error_type, error_message, context):
        """
        Generate a user-friendly error message.
        
        Args:
            error_type (str): The type of error
            error_message (str): The error message
            context (str): Additional context about where the error occurred
            
        Returns:
            str: User-friendly error message
        """
        # Common error types and their user-friendly messages
        error_messages = {
            'FileNotFoundError': "The file could not be found. Please check that the file exists and try again.",
            'PermissionError': "Permission denied. Please check that you have the necessary permissions to access the file.",
            'ValueError': "Invalid value provided. Please check your input and try again.",
            'KeyError': "A required key was not found. This might be due to missing column names.",
            'TypeError': "Type error occurred. This might be due to incompatible data types.",
            'IndexError': "Index error occurred. This might be due to accessing non-existent data.",
            'ImportError': "Failed to import a required module. Please check your installation.",
            'MemoryError': "Not enough memory to complete the operation. Try with a smaller dataset.",
            'ZeroDivisionError': "Division by zero occurred during calculation.",
            'AttributeError': "Attribute error occurred. This might be due to accessing non-existent attributes."
        }
        
        # Get user-friendly message for the error type, or use a generic message
        if error_type in error_messages:
            user_message = error_messages[error_type]
        else:
            user_message = f"An error occurred: {error_message}"
        
        # Add context if provided
        if context:
            user_message = f"{context}: {user_message}"
        
        return user_message
    
    def validate_file(self, file_path, file_type=None):
        """
        Validate a file exists and is of the correct type.
        
        Args:
            file_path (str): Path to the file
            file_type (str, optional): Expected file type (e.g., 'csv', 'xlsx')
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if file exists
        if not os.path.exists(file_path):
            return False, "File does not exist."
        
        # Check if file is a file (not a directory)
        if not os.path.isfile(file_path):
            return False, "Path is not a file."
        
        # Check file type if specified
        if file_type:
            if file_type.lower() == 'csv' and not file_path.lower().endswith('.csv'):
                return False, "File is not a CSV file."
            elif file_type.lower() == 'excel' and not file_path.lower().endswith(('.xlsx', '.xls')):
                return False, "File is not an Excel file."
        
        return True, ""
    
    def validate_dataframe(self, df):
        """
        Validate a pandas DataFrame.
        
        Args:
            df (pandas.DataFrame): DataFrame to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if df is a DataFrame
        if not hasattr(df, 'shape'):
            return False, "Input is not a valid DataFrame."
        
        # Check if DataFrame is empty
        if df.empty:
            return False, "DataFrame is empty."
        
        # Check if DataFrame has at least one column
        if df.shape[1] == 0:
            return False, "DataFrame has no columns."
        
        return True, ""