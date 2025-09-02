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

def clear_and_import_orders_data(connection):
    """Clear and import Orders and related tables with new distribution"""
    try:
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear tables that depend on Orders
        tables_to_clear = ['Delivery', 'Order_Financials', 'Orders']
        for table in tables_to_clear:
            cursor.execute(f"TRUNCATE TABLE {table}")
            print(f"Cleared table: {table}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        connection.commit()
        
        # Import Orders
        df_orders = pd.read_excel('database_data.xlsx', sheet_name='Orders')
        print(f"Read {len(df_orders)} rows from Orders")
        
        # Clean and convert data
        df_orders = df_orders.replace({np.nan: None})
        df_orders['order_date'] = pd.to_datetime(df_orders['order_date']).dt.strftime('%Y-%m-%d')
        df_orders['order_time'] = pd.to_datetime(df_orders['order_time']).dt.strftime('%H:%M:%S')
        
        # Insert Orders
        data_orders = [tuple(row) for row in df_orders.values]
        columns_orders = ', '.join(df_orders.columns)
        placeholders_orders = ', '.join(['%s'] * len(df_orders.columns))
        insert_query_orders = f"INSERT INTO Orders ({columns_orders}) VALUES ({placeholders_orders})"
        
        cursor.executemany(insert_query_orders, data_orders)
        print(f"Successfully imported {len(data_orders)} rows to Orders")
        
        # Import Order_Financials
        df_financials = pd.read_excel('database_data.xlsx', sheet_name='Order_Financials')
        print(f"Read {len(df_financials)} rows from Order_Financials")
        
        df_financials = df_financials.replace({np.nan: None})
        data_financials = [tuple(row) for row in df_financials.values]
        columns_financials = ', '.join(df_financials.columns)
        placeholders_financials = ', '.join(['%s'] * len(df_financials.columns))
        insert_query_financials = f"INSERT INTO Order_Financials ({columns_financials}) VALUES ({placeholders_financials})"
        
        cursor.executemany(insert_query_financials, data_financials)
        print(f"Successfully imported {len(data_financials)} rows to Order_Financials")
        
        # Import Delivery (only Home Delivery orders)
        df_delivery = pd.read_excel('database_data.xlsx', sheet_name='Delivery')
        print(f"Read {len(df_delivery)} rows from Delivery")
        
        df_delivery = df_delivery.replace({np.nan: None})
        data_delivery = [tuple(row) for row in df_delivery.values]
        columns_delivery = ', '.join([f'`{col}`' if col == 'match' else col for col in df_delivery.columns])
        placeholders_delivery = ', '.join(['%s'] * len(df_delivery.columns))
        insert_query_delivery = f"INSERT INTO Delivery ({columns_delivery}) VALUES ({placeholders_delivery})"
        
        cursor.executemany(insert_query_delivery, data_delivery)
        print(f"Successfully imported {len(data_delivery)} rows to Delivery")
        
        connection.commit()
        cursor.close()
        
        print("✅ Orders data updated successfully with new distribution!")
        
    except Error as e:
        print(f"Error updating Orders data: {e}")

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Update Orders and related tables
    print("Updating Orders table with new distribution (40% Delivery, 60% Dine-in)...")
    clear_and_import_orders_data(connection)
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")

if __name__ == "__main__":
    main() 