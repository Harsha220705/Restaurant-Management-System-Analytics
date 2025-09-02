import pandas as pd

excel_file = 'database_data.xlsx'

# Load sheets
clients = pd.read_excel(excel_file, sheet_name='Clients')
restaurants = pd.read_excel(excel_file, sheet_name='Restaurants')
users = pd.read_excel(excel_file, sheet_name='Users')

print('--- Clients Sheet ---')
print('Nulls per column:\n', clients.isnull().sum())
print('Unique client_ids:', clients['client_id'].nunique(), 'of', len(clients))
print('Sample legal names:', clients['legal_name'].head().tolist())

print('\n--- Restaurants Sheet ---')
print('Nulls per column:\n', restaurants.isnull().sum())
print('Unique restaurant_ids:', restaurants['restaurant_id'].nunique(), 'of', len(restaurants))
print('Sample names:', restaurants['name'].head().tolist())
# Check client_id foreign key
missing_clients = restaurants[~restaurants['client_id'].isin(clients['client_id'])]
print('Restaurants with missing client_id:', len(missing_clients))

print('\n--- Users Sheet ---')
print('Nulls per column:\n', users.isnull().sum())
print('Unique user_ids:', users['user_id'].nunique(), 'of', len(users))
print('Unique emails:', users['email'].nunique(), 'of', len(users))
print('Sample emails:', users['email'].head().tolist())
# Check restaurant_id foreign key
missing_restaurants = users[~users['restaurant_id'].isin(restaurants['restaurant_id'])]
print('Users with missing restaurant_id:', len(missing_restaurants))