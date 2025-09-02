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

def import_users_table(connection):
    """Import Users table with proper data handling"""
    try:
        # Read Excel sheet
        df = pd.read_excel('database_data.xlsx', sheet_name='Users')
        print(f"Read {len(df)} rows from Users")
        
        # Clean the dataframe
        df = df.replace({np.nan: None})
        
        # Convert date columns to proper format
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        # Convert numeric columns to proper types
        df['role_id'] = df['role_id'].astype(int)
        df['department_id'] = df['department_id'].astype(int)
        df['restaurant_id'] = df['restaurant_id'].astype(int)
        df['client_id'] = df['client_id'].astype(int)
        df['subscription_id'] = df['subscription_id'].astype(int)
        
        # Convert DataFrame to list of tuples for insertion
        data = [tuple(row) for row in df.values]
        
        # Create column names for INSERT statement
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        
        # Create INSERT statement
        insert_query = f"INSERT INTO Users ({columns}) VALUES ({placeholders})"
        
        # Execute INSERT
        cursor = connection.cursor()
        cursor.executemany(insert_query, data)
        connection.commit()
        
        print(f"Successfully imported {len(data)} rows to Users")
        cursor.close()
        
    except Error as e:
        print(f"Error importing Users: {e}")

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Import Users table
    print("\n--- Importing Users ---")
    import_users_table(connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 