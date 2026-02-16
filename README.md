# Expense Tracker

## Project Description

**Expense Tracker** is a comprehensive desktop application designed to help users manage, track, and analyze their personal expenses efficiently. The application provides an intuitive graphical interface for recording expenses, organizing them by category, and visualizing spending patterns through interactive analytics dashboards.

### Key Features

- **Expense Recording**: Add new expenses with title, amount, category, and optional notes
- **Database Management**: Persistent storage of all expense records using SQLite
- **Category Analysis**: Group and analyze expenses by category with detailed breakdowns
- **Visual Analytics**: Interactive pie charts showing expense distribution across categories
- **Data Insights**: Calculate total balance and category-wise spending summaries
- **Logging System**: Comprehensive application logging for debugging and monitoring

---

## Technology Stack

### Backend & Core
- **Python 3**: Primary programming language for backend logic and core functionality
- **SQLite3**: Lightweight, self-contained relational database for expense data persistence
- **Pandas**: Data analysis and manipulation library for expense aggregation and statistical calculations

### Frontend & GUI
- **Tkinter**: Python's standard GUI toolkit for creating the user interface
- **TTKBootstrap**: Modern Bootstrap-themed extension for Tkinter providing enhanced UI components and dark mode styling
- **Matplotlib**: Data visualization library for generating interactive pie charts and expense analysis graphs
- **FigureCanvasTkAgg**: Integration layer between Matplotlib and Tkinter for embedded chart rendering

### Infrastructure & Tools
- **Logging Module**: Python's built-in logging framework for application-level event tracking and error logging
- **Type Hints**: Python type annotations for improved code clarity and IDE support
- **OS Module**: Cross-platform file and directory management

### Project Structure
```
Expense-tracker/
├── src/
│   ├── main.py                 # Application entry point
│   ├── logger.py              # Logging configuration
│   ├── database/
│   │   └── db_manager.py      # SQLite database operations
│   ├── gui/
│   │   └── main_window.py     # GUI interface and components
│   └── logic/
│       └── analyzer.py        # Expense analysis and calculations
├── data/
│   └── expenses.db            # SQLite database file
└── README.md                  # Project documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Required Dependencies
```bash
pip install pandas ttkbootstrap matplotlib
```

### Running the Application
```bash
python src/main.py
```

---

## Features Overview

### 1. Expense Registration
Users can quickly add new expenses by providing:
- **Title**: Brief description of the expense
- **Price**: Amount spent (numeric value)
- **Category**: Classification for organization and analysis
- **Memo**: Optional additional notes

### 2. Database Management
- Automatic database initialization on first run
- Secure SQLite transactions with error handling
- Persistent storage with automatic schema creation

### 3. Expense Analysis
- Real-time category-wise expense aggregation
- Total balance calculation across all expenses
- Chronological expense listing with newest entries first

### 4. Visual Analytics
- **Donut/Pie Chart Visualization**: Interactive charts showing percentage breakdown by category
- **Dark Theme Interface**: Professional dark-mode UI for comfortable viewing
- **Responsive Design**: Dynamic graph rendering based on available data

### 5. Logging & Debugging
- Console output for INFO level messages
- File-based logging (app.log) for DEBUG level persistence
- Structured error messages with context information

---

## Architecture

### Modular Design
The application follows a clean architecture pattern with clear separation of concerns:

- **Presentation Layer** (gui/main_window.py): User interface and event handling
- **Business Logic Layer** (logic/analyzer.py): Data analysis and calculations
- **Data Access Layer** (database/db_manager.py): Database operations and queries
- **Core Layer** (main.py): Application initialization and orchestration

### Error Handling
- Comprehensive try-catch blocks for database operations
- User-friendly error messages for invalid inputs
- Detailed logging of all errors and exceptions

---

## Usage Example

1. **Launch Application**: Run `python src/main.py`
2. **Welcome Screen**: Start by clicking the "Start" button
3. **Add Expenses**: Navigate to "ADD EXPENSE" tab and fill in the form
4. **View Analysis**: Click "VIEW ANALYSIS" to see category breakdowns and pie charts
5. **Track Progress**: Monitor your spending patterns and category totals

---

## Future Enhancements

- Export expense data to CSV/PDF
- Monthly and yearly budget tracking
- Recurring expense templates
- Multi-user support with authentication
- Cloud synchronization
- Mobile app integration

---

## License

This project is open-source and available for personal and educational use.

---

## Author

Developed as a personal finance management tool.

---

**Last Updated**: February 2026