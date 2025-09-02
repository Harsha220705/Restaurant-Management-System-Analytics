Restaurant Management System Analytics Dashboard 🍽️
Project Overview
This project provides a comprehensive analytics dashboard for a fictional restaurant management system. The solution consists of two main parts: a Python script for generating realistic data and a Streamlit application for data visualization and analysis.

The goal is to simulate a variety of daily restaurant operations, including sales, expenses, and workforce management, across multiple locations in the UK and India. This rich, multi-dimensional dataset is then used to power a business intelligence dashboard, offering key insights for restaurant owners and managers to make data-driven decisions.

Key Features
Realistic Data Generation: Uses the Faker library to create a plausible, year-long dataset for a multi-restaurant business.

Detailed Financials: Tracks financial metrics at a granular level, including daily sales, expenses, and cash flow, with support for country-specific taxes and currencies.

Operational Insights: The dashboard visualizes key performance indicators (KPIs) such as profit margins, revenue by order type, and peak hours to optimize staffing.

Interactive Dashboard: Built with Streamlit, the dashboard allows users to filter data by date and restaurant, providing dynamic and actionable insights.

Relational Database Schema: The generated data is structured across multiple tables (e.g., Clients, Restaurants, Orders, Expenses), simulating a real-world database.

Getting Started
Prerequisites
To run this project, you need to have Python installed. You can install the required libraries using pip:

Bash

pip install pandas numpy streamlit faker mysql-connector-python matplotlib seaborn plotly

1. Data Generation
The generate_data.py script creates the necessary Excel file with all the project data.

Open the generate_data.py file.

Ensure your MySQL connection details are correct in the script's connect_to_database() function, or comment out the database-related code if you're not using MySQL.

Run the script to generate the data file:

Bash

python generate_data.py
This will create a file named restaurant_data_new.xlsx in your project directory.

2. Running the Dashboard
The dashboard is built with Streamlit and visualizes the data from the generated file.

Make sure the restaurant_data_new.xlsx file is in the same directory as your Streamlit app file.

Open your terminal in the project directory.

Run the Streamlit application with the following command:

Bash

streamlit run your_app_file_name.py
A web browser tab will open automatically, displaying the interactive dashboard.

Dashboard Sections
The dashboard is organized into several sections for easy navigation:

Workforce Allocation: Analyzes order volume by hour to help with employee scheduling.

Restaurant Financial Health: Provides an overview of each restaurant's profitability and financial status.

Order Volume Trends: Breaks down revenue and order count by order type (e.g., Dine-in, Home Delivery).

Client & Restaurant Performance: Tracks net profit trends over time for a selected client's restaurants.

Daily Restaurant Performance Dashboard: A high-level overview of daily sales, expenses, and other key metrics.

Enjoy exploring the data and gaining insights!
