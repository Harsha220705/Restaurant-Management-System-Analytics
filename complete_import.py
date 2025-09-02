import mysql.connector
from mysql.connector import Error

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

def import_roles_manual(connection):
    """Manually import Roles data"""
    try:
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE Roles")
        
        # Insert Roles data manually
        roles_data = [
            (1, 'Front Office Staff', 'web', '2019-06-20 05:41:00', '2019-06-20 05:41:00'),
            (2, 'Chef', 'web', '2019-06-20 05:43:00', '2019-06-20 05:43:00'),
            (3, 'Supervisor', 'web', '2019-06-20 05:45:00', '2019-06-20 05:45:00'),
            (5, 'Admin', 'admin', '2019-08-10 18:18:00', '2019-08-10 18:18:00')
        ]
        
        insert_query = "INSERT INTO Roles (id, name, guard_name, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(insert_query, roles_data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(roles_data)} rows to Roles")
        
    except Error as e:
        print(f"Error importing Roles: {e}")

def import_departments_manual(connection):
    """Manually import Departments data"""
    try:
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE Departments")
        
        # Insert Departments data manually
        departments_data = [
            (1, 'Payroll', 'PRL'),
            (2, 'Human Resources', 'HRM'),
            (3, 'Accounting', 'ACC'),
            (4, 'Quality Assurance', 'QLA'),
            (5, 'Advertising', 'ADV'),
            (6, 'Finances', 'FIN'),
            (7, 'Sales and Marketing', 'SMG'),
            (8, 'Legal Department', 'LGD'),
            (9, 'Customer Service', 'CSR')
        ]
        
        insert_query = "INSERT INTO Departments (Department_id, department_name, department_code) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, departments_data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(departments_data)} rows to Departments")
        
    except Error as e:
        print(f"Error importing Departments: {e}")

def import_currencies_manual(connection):
    """Manually import Currencies data"""
    try:
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear existing data
        cursor.execute("TRUNCATE TABLE Currencies")
        
        # Insert Currencies data manually
        currencies_data = [
            (1, 'GBP', '£'),
            (2, 'EUR', '€'),
            (3, 'USD', '$'),
            (4, 'INR', '₹')
        ]
        
        insert_query = "INSERT INTO Currencies (currency_id, currency_type, currency_symbol) VALUES (%s, %s, %s)"
        cursor.executemany(insert_query, currencies_data)
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(currencies_data)} rows to Currencies")
        
    except Error as e:
        print(f"Error importing Currencies: {e}")

def main():
    # Connect to MySQL
    connection = connect_to_mysql()
    if not connection:
        return
    
    # Import static data manually
    print("\n--- Importing Roles ---")
    import_roles_manual(connection)
    
    print("\n--- Importing Departments ---")
    import_departments_manual(connection)
    
    print("\n--- Importing Currencies ---")
    import_currencies_manual(connection)
    
    # Re-enable foreign key checks
    cursor = connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    connection.commit()
    cursor.close()
    
    # Close connection
    if connection.is_connected():
        connection.close()
        print("\nMySQL connection closed")
        print("\n✅ Static data imported successfully!")
        print("Now you can import the remaining data using the previous scripts.")

if __name__ == "__main__":
    main() 