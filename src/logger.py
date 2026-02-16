"""Application Logger Configuration

This module sets up a logging system for the Expense Tracker application.
It configures both console and file handlers to capture application events
at different logging levels (DEBUG for files, INFO for console).
"""

import logging
import os

def setup_logger():
    """Configure and initialize the application logger.
    
    Sets up two logging handlers:
    - Console Handler: Displays INFO level messages to the console
    - File Handler: Logs all DEBUG and above messages to 'app.log' file
    
    The logger uses a standard format showing timestamp, logger name,
    log level, and message content.
    
    Returns:
        logging.Logger: Configured logger instance for the application
    """
    # Get or create the logger instance for the expense tracker
    logger = logging.getLogger("expense_tracker")

    # Set the minimum logging level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Only add handlers if they haven't been added yet (prevents duplicates)
    if not logger.handlers:
        # Define the logging message format
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s)')

        # Configure console handler (INFO level and above)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(format)
        console_handler.setLevel(logging.INFO)

        # Configure file handler (DEBUG level and above)
        file_handler = logging.FileHandler("app.log", encoding='utf-8')
        file_handler.setFormatter(format)
        file_handler.setLevel(logging.DEBUG)

        # Attach both handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Initialize and export the configured logger for use throughout the application
logger = setup_logger()