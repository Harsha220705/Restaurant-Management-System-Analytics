import pandas as pd
import mysql.connector
from mysql.connector import Error
import warnings
import numpy as np
warnings.filterwarnings('ignore')

def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='harsha@2207',
            database='restaurant_management'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def clean_dataframe(df):
    """Clean dataframe by handling NaN values and date formats"""
    # Replace NaN with None for MySQL
    df = df.replace({np.nan: None})
    
    # Convert date columns to proper format
    date_columns = ['created_at', 'updated_at', 'date_of_birth', 'order_date', 
                   'delivery_date', 'exp_date', 'banking_date', 'cash_up_date']
    
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df

def import_excel_to_mysql(excel_file, sheet_name, table_name, connection):
    """Import Excel sheet to MySQL table with proper handling"""
    try:
        # Read Excel sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"Read {len(df)} rows from {sheet_name}")
        
        # Clean the dataframe
        df = clean_dataframe(df)
        
        # Convert DataFrame to list of tuples for insertion
        data = [tuple(row) for row in df.values]
        
        # Create column names for INSERT statement
        columns = ', '.join([f'`{col}`' if col == 'match' else col for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        
        # Create INSERT statement
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute INSERT
        cursor = connection.cursor()
        cursor.executemany(insert_query, data)
        connection.commit()
        
        print(f"Successfully imported {len(data)} rows to {table_name}")
        cursor.close()
        
    except Error as e:
        print(f"Error importing {sheet_name} to {table_name}: {e}")

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Excel file path
    excel_file = 'database_data.xlsx'
    
    # Import tables in correct order (parent tables first)
    tables_to_import = [
        ('Roles', 'Roles'),
        ('Departments', 'Departments'), 
        ('Countries', 'Countries'),
        ('Currencies', 'Currencies'),
        ('TaxInfo', 'TaxInfo'),
        ('Clients', 'Clients'),
        ('Restaurants', 'Restaurants'),
        ('Subscriptions', 'Subscriptions'),
        ('Users', 'Users'),
        ('Orders', 'Orders'),
        ('Order_Financials', 'Order_Financials'),
        ('Sales', 'Sales'),
        ('Expenses', 'Expenses'),
        ('Banking', 'Banking'),
        ('Cashup', 'Cashup'),
        ('Delivery', 'Delivery')
    ]
    
    # Import each table
    for sheet_name, table_name in tables_to_import:
        print(f"\n--- Importing {sheet_name} ---")
        import_excel_to_mysql(excel_file, sheet_name, table_name, connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 