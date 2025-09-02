import pandas as pd
import mysql.connector
from mysql.connector import Error
import warnings
warnings.filterwarnings('ignore')

def connect_to_mysql():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='harsha@2207',  # Replace with your actual password
            database='restaurant_management'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def import_excel_to_mysql(excel_file, sheet_name, table_name, connection):
    """Import Excel sheet to MySQL table"""
    try:
        # Read Excel sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"Read {len(df)} rows from {sheet_name}")
        
        # Convert DataFrame to list of tuples for insertion
        data = [tuple(row) for row in df.values]
        
        # Create column names for INSERT statement
        columns = ', '.join(df.columns)
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

def import_countries_static(connection):
    """Import static countries_content from main.py into Countries table"""
    from main import countries_content
    import io
    df = pd.read_csv(io.StringIO(countries_content))
    
    # Replace NaN values with None (NULL in MySQL)
    df = df.replace({pd.NA: None, 'nan': None, 'NaN': None})
    df = df.where(pd.notnull(df), None)
    
    data = [tuple(row) for row in df.values]
    columns = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    insert_query = f"INSERT INTO Countries ({columns}) VALUES ({placeholders})"
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Countries")  # Clear table first
        cursor.executemany(insert_query, data)
        connection.commit()
        print(f"Inserted {len(data)} rows into Countries from static content.")
    except Error as e:
        print(f"Error importing static countries: {e}")
        print(f"Sample data: {data[:2]}")  # Debug info
    finally:
        cursor.close()

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Import static countries data
    import_countries_static(connection)
    
    # Excel file path
    excel_file = 'database_data.xlsx'
    
    # Define sheet to table mappings
    sheet_table_mapping = {
        'Roles': 'Roles',
        'Departments': 'Departments', 
        'Countries': 'Countries',
        'Currencies': 'Currencies',
        'TaxInfo': 'TaxInfo',
        'Clients': 'Clients',
        'Restaurants': 'Restaurants',
        'Subscriptions': 'Subscriptions',
        'Users': 'Users',
        'Orders': 'Orders',
        'Order_Financials': 'Order_Financials',
        'Sales': 'Sales',
        'Expenses': 'Expenses',
        'Banking': 'Banking',
        'Cashup': 'Cashup',
        'Delivery': 'Delivery'
    }
    
    # Import each sheet
    for sheet_name, table_name in sheet_table_mapping.items():
        print(f"\n--- Importing {sheet_name} ---")
        import_excel_to_mysql(excel_file, sheet_name, table_name, connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 