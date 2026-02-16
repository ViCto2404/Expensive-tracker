"""Main GUI Window Module

This module implements the graphical user interface for the Expense Tracker.
It provides a tkinter-based interface with a sidebar menu and dynamic content
areas for adding expenses and viewing analytical reports.
"""

import ttkbootstrap as tb
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from ttkbootstrap.constants import *
from datetime import datetime
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from logger import logger


class MainWindow:
    """Main application window for the Expense Tracker GUI.
    
    Provides a user interface for:
    - Adding new expense records
    - Viewing expense analysis and category-based statistics
    - Displaying expenses in a table format
    - Visualizing data with pie charts
    """
    
    def __init__(self, db, analyzer):
        """Initialize the main window and GUI components.
        
        Args:
            db (DatabaseManager): Database manager instance for data operations
            analyzer (ExpenseAnalyzer): Expense analyzer instance for calculations
        """
        self.db = db
        self.analyzer = analyzer

        # Create the main window with dark theme
        self.root = tb.Window(themename="darkly")
        self.root.title("Expense Tracker")
        self.root.geometry("1100x700")

        # Create sidebar frame for navigation menu
        self.sidebar = tb.Frame(self.root, bootstyle="secondary", width=200)
        self.sidebar.pack(side=LEFT, fill=Y)

        # Create main content container
        self.container = tb.Frame(self.root, padding=10)
        self.container.pack(side=RIGHT, fill=BOTH, expand=True)

        # Initialize the sidebar menu and show welcome screen
        self._setup_sidebar()
        self.show_welcome()

    def _setup_sidebar(self):
        """Create and populate the navigation sidebar with menu buttons."""
        # Menu title
        tb.Label(self.sidebar, text="MENU", font=("Helvetica", 16, "bold")).pack(pady=20)
        # Button to show the expense entry form
        tb.Button(self.sidebar, text="ADD EXPENSE", bootstyle="info-outline", command=self.show_home).pack(fill=X, padx=10, pady=5)
        # Button to show the analysis and statistics view
        tb.Button(self.sidebar, text="VIEW ANALYSIS", bootstyle="info-outline", command=self.show_graph).pack(fill=X, padx=10, pady=5)

    def show_welcome(self):
        """Display the welcome screen with application title and start button."""
        # Clear the main container
        self._clear_container()
        frame = tb.Frame(self.container)
        frame.pack(fill=BOTH, expand=True)

        # Application title
        tb.Label(frame, text="Expense Tracker", font=("Helvetica", 24, "bold")).pack(pady=40)
        # Start button to navigate to the expense entry form
        tb.Button(frame, text="Start", bootstyle="success", padding=10, command=self.show_home).pack(pady=20)
    
    def show_home(self):
        """Display the expense entry form for adding new expenses."""
        # Clear the main container
        self._clear_container()
        # Section title
        tb.Label(self.container, text="Expense Record", font=("Helvetica", 18)).pack()

        # Create form frame for input fields
        form_frame = tb.Frame(self.container, padding=10)
        form_frame.pack(pady=10)

        # Title/Name input
        tb.Label(form_frame, text="Title:", font=("Helvetica", 12, "bold"), bootstyle="info").grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.title_entry = tb.Entry(form_frame, width=60)
        self.title_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky=W)

        # Amount/Price input
        tb.Label(form_frame, text="Price:", font=("Helvetica", 12, "bold"), bootstyle="info").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.price_entry = tb.Entry(form_frame, width=60)
        self.price_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10, sticky=W)

        # Category input
        tb.Label(form_frame, text="Category:", font=("Helvetica", 12, "bold"), bootstyle="info").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.category_entry = tb.Entry(form_frame, width=60)
        self.category_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=10, sticky=W)

        # Optional memo/notes input
        tb.Label(form_frame, text='Memo:', font=('Helvetica', 12, 'bold'), bootstyle='info').grid(row=3, column=0, padx=10, pady=10, sticky=W)
        self.memo_entry = tb.Entry(form_frame, width=60)
        self.memo_entry.grid(row=3, column=1, columnspan=3, padx=10, pady=10, sticky=W)
        # Helper text indicating memo is optional
        tb.Label(form_frame, text="Memo is optional:", font=('Helvetica', 9), bootstyle='success').grid(row=4, column=1, padx=10, sticky=W)
        
        # Submit button to save the expense
        self.btn_add = tb.Button(form_frame, text="Add Expense", bootstyle="Danger", width=15, command=self._save_record)
        self.btn_add.grid(row=0, column=4, rowspan=2, padx=20, pady=10)

        # Visual separator
        tb.Separator(self.container, bootstyle='info').pack(fill=X, pady=15)

        # Display the expenses table
        self._create_table_view()


    def show_graph(self):
        """Display expense analysis with a pie chart showing totals by category."""
        # Clear the main container
        self._clear_container()
        # Section title
        tb.Label(self.container, text="Expense Analysis", font=("Helvetica", 18)).pack()

        # Fetch category totals with error handling
        try:
            category_totals = self.analyzer.get_category_totals()
        except Exception as e:
            logger.error(f"Error fetching category totals: {e}")
            category_totals = None

        # Check if data is available
        if category_totals is None or category_totals.empty:
            tb.Label(self.container, text="No expenses recorded yet.", font=('Helvetica', 14), bootstyle='warning').pack(expand=YES)
            return
        
        # Create a matplotlib figure with dark background
        fig = Figure(figsize=(6,6), dpi=100, facecolor="#1a1a1a")
        ax = fig.add_subplot(111)
        ax.set_facecolor('#1a1a1a')

        # Define color palette for pie chart
        colors = ["#5a5cf4", '#ea4335', "#00c190", "#9c27b0", '#ff9800']

        # Create pie chart with category data
        wedges, texts, autotexts = ax.pie(
            category_totals.values,  # Expense amounts
            labels=category_totals.index,  # Category names
            autopct='%1.1f%%',  # Show percentages
            startangle=90,
            pctdistance=0.75,
            textprops={'color':'w', 'fontsize': 10, 'weight': 'bold'},
            colors=colors[:len(category_totals)]  # Use defined color palette
        )

        # Add a donut hole in the center (donut chart style)
        centre_circle = plt.Circle((0,0), 0.60, fc='#1a1a1a')
        ax.add_artist(centre_circle)

        # Set chart title and formatting
        ax.set_title('Total amount by category', fontsize=16, color='w', pad=20)
        ax.axis('equal')

        # Create frame for the graph
        graph_wrapper = tb.Frame(self.container)
        graph_wrapper.pack(expand=YES)

        # Embed matplotlib figure in tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=graph_wrapper)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def _clear_container(self):
        """Remove all widgets from the main content container."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def run(self):
        """Start the application and display the main window."""
        self.root.mainloop() 

    def _save_record(self):
        """Validate form input and save the expense record to the database.
        
        Performs the following validations:
        - All required fields are filled (title, price, category)
        - Price is a valid numeric value
        - Then saves to database and refreshes the display
        """
        # Retrieve form input values
        title = self.title_entry.get()
        price = self.price_entry.get()
        category = self.category_entry.get()
        memo = self.memo_entry.get()
        # Get current date and time in ISO format
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  

        # Validate that all required fields are completed
        if not title or not price or not category:
            messagebox.showerror("Error", "Please fill in all required fields (Title, price, category).")
            return 
        
        # Validate that price is a numeric value
        try:
            amount = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number.")
            return
        
        # Combine title and memo into description (memo is optional)
        description = f"{title} | {memo}" if memo else title

        # Attempt to save the expense to the database
        success = self.db.add_expense(amount, category, date_now, description)

        # Provide user feedback and refresh display if successful
        if success:
            messagebox.showinfo("Success", "Expense added successfully")
            self._clear_form()  # Clear input fields
            self._refresh_table()  # Update expense table
        else:
            messagebox.showerror("Error", "Failed to add expense. Please try again.")

    def _clear_form(self):
        # Clear input fields created in show_home
        try:
            self.title_entry.delete(0, 'end')
            self.price_entry.delete(0, 'end')
            self.category_entry.delete(0, 'end')
            self.memo_entry.delete(0, 'end')
        except AttributeError:
            # If entries are missing, ignore silently
            pass
    
    def _refresh_table(self):
        # Support either `tree` or `table` attribute if present
        tree = getattr(self, 'tree', None) or getattr(self, 'table', None)
        if not tree:
            return

        for item in tree.get_children():
            tree.delete(item)

        expenses = self.db.fetch_all_expenses()

        for exp in expenses:
            tree.insert('', END, values=exp)

    def _create_table_view(self):
        table_frame = tb.Frame(self.container)
        table_frame.pack(fill=BOTH, expand=True)

        columns = ('ID', 'Amount', 'Category', 'Date', 'Description', 'Memo')

        self.tree = tb.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            bootstyle='info',
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER, width=100)

        scroolbar = tb.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroolbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scroolbar.pack(side=RIGHT, fill=Y)

        self._refresh_table()


