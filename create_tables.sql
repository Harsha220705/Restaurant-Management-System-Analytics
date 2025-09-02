-- Create database
CREATE DATABASE IF NOT EXISTS restaurant_management;
USE restaurant_management;

-- Create Roles table
CREATE TABLE Roles (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    guard_name VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME
);

-- Create Departments table
CREATE TABLE Departments (
    Department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(10)
);

-- Create Countries table
CREATE TABLE Countries (
    lang VARCHAR(10),
    lan_name VARCHAR(50),
    country_alpha2_code VARCHAR(2),
    country_code VARCHAR(3),
    country_name VARCHAR(100)
);

-- Create Currencies table
CREATE TABLE Currencies (
    currency_id INT PRIMARY KEY,
    currency_type VARCHAR(10),
    currency_symbol VARCHAR(5)
);

-- Create TaxInfo table
CREATE TABLE TaxInfo (
    tax_type_id INT PRIMARY KEY,
    country VARCHAR(50),
    Tax_Type VARCHAR(50),
    tax_percentage VARCHAR(10)
);

-- Create Clients table
CREATE TABLE Clients (
    client_id INT PRIMARY KEY,
    legal_name VARCHAR(255),
    business_name VARCHAR(255),
    address TEXT,
    contact_person VARCHAR(255),
    country VARCHAR(50),
    is_active BOOLEAN,
    inactivated_date DATE NULL,
    activated_date DATE NULL
);

-- Create Restaurants table
CREATE TABLE Restaurants (
    restaurant_id INT PRIMARY KEY,
    name VARCHAR(255),
    legal_name VARCHAR(255),
    address TEXT,
    phone VARCHAR(50),
    is_franchise BOOLEAN,
    is_active BOOLEAN,
    country VARCHAR(50),
    client_id INT,
    currency_id INT,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (currency_id) REFERENCES Currencies(currency_id)
);

-- Create Subscriptions table
CREATE TABLE Subscriptions (
    subscription_id INT PRIMARY KEY,
    display_name VARCHAR(100),
    subscription_name VARCHAR(100),
    product_code VARCHAR(20),
    subscription_active BOOLEAN,
    subscription_code VARCHAR(20),
    description TEXT,
    cost DECIMAL(10,2),
    no_of_users INT
);

-- Create Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    address TEXT,
    date_of_birth DATE,
    is_active BOOLEAN,
    role_id INT,
    department_id INT,
    restaurant_id INT,
    client_id INT,
    subscription_id INT,
    FOREIGN KEY (role_id) REFERENCES Roles(id),
    FOREIGN KEY (department_id) REFERENCES Departments(Department_id),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions(subscription_id)
);

-- Create Orders table
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    restaurant_id INT,
    order_date DATE,
    order_time TIME,
    order_type VARCHAR(50),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Create Order_Financials table
CREATE TABLE Order_Financials (
    order_id INT PRIMARY KEY,
    drinks_amount DECIMAL(10,2),
    food_amount DECIMAL(10,2),
    other_payment DECIMAL(10,2),
    service_charges DECIMAL(10,2),
    delivery_charges DECIMAL(10,2),
    order_amount DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    order_total DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Create Sales table
CREATE TABLE Sales (
    sales_id INT PRIMARY KEY,
    restaurant_id INT,
    date DATE,
    drinks_payment DECIMAL(10,2),
    food_payment DECIMAL(10,2),
    other_payment DECIMAL(10,2),
    service_charges DECIMAL(10,2),
    delivery_charges DECIMAL(10,2),
    tax_charges DECIMAL(10,2),
    creditcard_tip DECIMAL(10,2),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Create Expenses table
CREATE TABLE Expenses (
    expense_id INT PRIMARY KEY,
    restaurant_id INT,
    exp_date DATE,
    bills DECIMAL(10,2),
    vendors DECIMAL(10,2),
    wage_advances DECIMAL(10,2),
    repairs DECIMAL(10,2),
    sundries DECIMAL(10,2),
    total_expense DECIMAL(10,2),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Create Banking table
CREATE TABLE Banking (
    banking_id INT PRIMARY KEY,
    banked_total DECIMAL(10,2),
    banking_total DECIMAL(10,2),
    banking_date DATE,
    banking_time_indicator VARCHAR(10),
    reconcile_status VARCHAR(20),
    restaurant_id INT,
    sealed_by VARCHAR(255),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);

-- Create Cashup table
CREATE TABLE Cashup (
    cashup_id INT PRIMARY KEY,
    restaurant_id INT,
    bod_amount DECIMAL(10,2),
    sales DECIMAL(10,2),
    expenses DECIMAL(10,2),
    tax DECIMAL(10,2),
    delivery_charges DECIMAL(10,2),
    eod_amount DECIMAL(10,2),
    match BOOLEAN,
    banking_id INT,
    cash_up_date DATE,
    cashup_status VARCHAR(20),
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id),
    FOREIGN KEY (banking_id) REFERENCES Banking(banking_id)
);

-- Create Delivery table
CREATE TABLE Delivery (
    delivery_id INT PRIMARY KEY,
    restaurant_id INT,
    order_amount DECIMAL(10,2),    st.warning("Customer retention analysis is not available because the Orders table does not contain user information.")
    api_amount DECIMAL(10,2),
    match BOOLEAN,
    name VARCHAR(255),
    delivery_date DATE,
    FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
);