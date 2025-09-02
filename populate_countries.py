import mysql.connector
from mysql.connector import Error
import pandas as pd
import io

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

def populate_countries():
    """Populate Countries table with static data"""
    # Import the static data from main.py
    from main import countries_content
    
    # Read the CSV data
    df = pd.read_csv(io.StringIO(countries_content))
    
    # Clean the data - replace NaN with None
    df = df.replace({pd.NA: None, 'nan': None, 'NaN': None})
    df = df.where(pd.notnull(df), None)
    
    # Ensure country_alpha2_code is max 2 characters
    df['country_alpha2_code'] = df['country_alpha2_code'].astype(str).str[:2]
    
    # Ensure country_code is max 3 characters
    df['country_code'] = df['country_code'].astype(str).str[:3]
    
    # Debug: Check row 82
    print(f"Row 82 data: {df.iloc[81]}")
    
    # Convert to list of tuples
    data = [tuple(row) for row in df.values]
    
    # Connect to database
    connection = connect_to_mysql()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM Countries")
        print("Cleared existing Countries data")
        
        # Insert new data
        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO Countries ({columns}) VALUES ({placeholders})"
        
        cursor.executemany(insert_query, data)
        connection.commit()
        
        print(f"Successfully inserted {len(data)} countries into the database")
        
        # Verify the insertion
        cursor.execute("SELECT COUNT(*) FROM Countries")
        count = cursor.fetchone()[0]
        print(f"Total countries in database: {count}")
        
        # Show sample data
        cursor.execute("SELECT * FROM Countries LIMIT 5")
        sample_data = cursor.fetchall()
        print("\nSample countries:")
        for row in sample_data:
            print(f"  {row}")
            
    except Error as e:
        print(f"Error: {e}")
        # Show the problematic data
        print(f"Problematic row data: {data[81] if len(data) > 81 else 'Row 82 not found'}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    populate_countries() 