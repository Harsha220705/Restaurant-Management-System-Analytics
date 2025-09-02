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

def fix_roles_table(connection):
    """Fix and import Roles table"""
    try:
        # Read Excel sheet
        df = pd.read_excel('database_data.xlsx', sheet_name='Roles')
        print(f"Read {len(df)} rows from Roles")
        
        # Clean the dataframe - handle NaN values properly
        df = df.replace({np.nan: None})
        
        # Convert date columns to proper format
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = pd.to_datetime(df['updated_at'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert DataFrame to list of tuples for insertion
        data = [tuple(row) for row in df.values]
        
        # Create INSERT statement
        insert_query = "INSERT INTO Roles (id, name, guard_name, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        
        # Execute INSERT
        cursor = connection.cursor()
        cursor.executemany(insert_query, data)
        connection.commit()
        
        print(f"Successfully imported {len(data)} rows to Roles")
        cursor.close()
        
    except Error as e:
        print(f"Error importing Roles: {e}")

def fix_countries_table(connection):
    """Fix and import Countries table"""
    try:
        # Read Excel sheet
        df = pd.read_excel('database_data.xlsx', sheet_name='Countries')
        print(f"Read {len(df)} rows from Countries")
        
        # Clean the dataframe - handle NaN values properly
        df = df.replace({np.nan: None})
        
        # Truncate country_alpha2_code to 2 characters
        df['country_alpha2_code'] = df['country_alpha2_code'].astype(str).str[:2]
        
        # Convert DataFrame to list of tuples for insertion
        data = [tuple(row) for row in df.values]
        
        # Create INSERT statement
        insert_query = "INSERT INTO Countries (lang, lan_name, country_alpha2_code, country_code, country_name) VALUES (%s, %s, %s, %s, %s)"
        
        # Execute INSERT
        cursor = connection.cursor()
        cursor.executemany(insert_query, data)
        connection.commit()
        
        print(f"Successfully imported {len(data)} rows to Countries")
        cursor.close()
        
    except Error as e:
        print(f"Error importing Countries: {e}")

def import_users_table(connection):
    """Import Users table after Roles is fixed"""
    try:
        # Read Excel sheet
        df = pd.read_excel('database_data.xlsx', sheet_name='Users')
        print(f"Read {len(df)} rows from Users")
        
        # Clean the dataframe
        df = df.replace({np.nan: None})
        
        # Convert date columns to proper format
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.strftime('%Y-%m-%d')
        
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
    
    # Fix and import Roles table
    print("\n--- Fixing and Importing Roles ---")
    fix_roles_table(connection)
    
    # Fix and import Countries table
    print("\n--- Fixing and Importing Countries ---")
    fix_countries_table(connection)
    
    # Import Users table
    print("\n--- Importing Users ---")
    import_users_table(connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 