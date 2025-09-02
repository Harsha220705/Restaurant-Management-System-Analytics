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

def clear_tables(connection, tables):
    """Clear specific tables"""
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    for table in tables:
        try:
            cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"Cleared table: {table}")
        except Error as e:
            print(f"Error clearing {table}: {e}")
    
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    connection.commit()
    cursor.close()

def import_roles(connection):
    """Import Roles table with proper data handling"""
    try:
        df = pd.read_excel('database_data.xlsx', sheet_name='Roles')
        print(f"Read {len(df)} rows from Roles")
        
        # Convert date strings to proper format
        df['created_at'] = pd.to_datetime(df['created_at'], format='%d-%m-%Y %H:%M', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        df['updated_at'] = pd.to_datetime(df['updated_at'], format='%d-%m-%Y %H:%M', errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Convert to list of tuples
        data = [tuple(row) for row in df.values]
        
        # Insert data
        cursor = connection.cursor()
        insert_query = "INSERT INTO Roles (id, name, guard_name, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(data)} rows to Roles")
        
    except Error as e:
        print(f"Error importing Roles: {e}")

def import_countries(connection):
    """Import Countries table with proper data handling"""
    try:
        df = pd.read_excel('database_data.xlsx', sheet_name='Countries')
        print(f"Read {len(df)} rows from Countries")
        
        # Clean data - truncate long codes
        df['country_alpha2_code'] = df['country_alpha2_code'].astype(str).str[:2]
        df['country_code'] = df['country_code'].astype(str).str[:3]
        
        # Convert to list of tuples
        data = [tuple(row) for row in df.values]
        
        # Insert data
        cursor = connection.cursor()
        insert_query = "INSERT INTO Countries (lang, lan_name, country_alpha2_code, country_code, country_name) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(data)} rows to Countries")
        
    except Error as e:
        print(f"Error importing Countries: {e}")

def import_users(connection):
    """Import Users table"""
    try:
        df = pd.read_excel('database_data.xlsx', sheet_name='Users')
        print(f"Read {len(df)} rows from Users")
        
        # Clean data
        df = df.replace({np.nan: None})
        
        # Convert date columns
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        # Convert to list of tuples
        data = [tuple(row) for row in df.values]
        
        # Insert data
        cursor = connection.cursor()
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO Users ({columns}) VALUES ({placeholders})"
        cursor.executemany(insert_query, data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(data)} rows to Users")
        
    except Error as e:
        print(f"Error importing Users: {e}")

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Clear the problematic tables
    print("Clearing problematic tables...")
    clear_tables(connection, ['Users', 'Countries', 'Roles'])
    
    # Import in correct order
    print("\n--- Importing Roles ---")
    import_roles(connection)
    
    print("\n--- Importing Countries ---")
    import_countries(connection)
    
    print("\n--- Importing Users ---")
    import_users(connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 