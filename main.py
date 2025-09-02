import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
from faker import Faker

# Initialize Faker
fake = Faker()

# --- Load Static Data from Provided Content ---
roles_content = """id,name,guard_name,created_at,updated_at
1,Front Office Staff,web,20-06-2019 05:41,20-06-2019 05:41
2,Chef,web,20-06-2019 05:43,20-06-2019 05:43
3,Supervisor,web,20-06-2019 05:45,20-06-2019 05:45
5,Admin,admin,10/8/2019 18:18,10/8/2019 18:18"""

departments_content = """Department_id,department_name,department_code
1,Payroll,PRL
2,Human Resources,HRM
3,Accounting,ACC
4,Quality Assurance,QLA
5,Advertising,ADV
6,Finances,FIN
7,Sales and Marketing,SMG
8,Legal Department,LGD
9,Customer Service,CSR"""

countries_content = """lang,lan_name,country_alpha2_code,country_code,country_name
EN,ENGLISH,AD,AND,Andorra
EN,ENGLISH,AE,ARE,United Arab Emirates
EN,ENGLISH,AF,AFG,Afghanistan
EN,ENGLISH,AG,ATG,Antigua and Barbuda
EN,ENGLISH,AI,AIA,Anguilla
EN,ENGLISH,AL,ALB,Albania
EN,ENGLISH,AM,ARM,Armenia
EN,ENGLISH,AO,AGO,Angola
EN,ENGLISH,AQ,ATA,Antarctica
EN,ENGLISH,AR,ARG,Argentina
EN,ENGLISH,AS,ASM,American Samoa
EN,ENGLISH,AT,AUT,Austria
EN,ENGLISH,AU,AUS,Australia
EN,ENGLISH,AW,ABW,Aruba
EN,ENGLISH,AX,ALA,Aland Islands
EN,ENGLISH,AZ,AZE,Azerbaijan
EN,ENGLISH,BA,BIH,Bosnia and Herzegovina
EN,ENGLISH,BB,BRB,Barbados
EN,ENGLISH,BD,BGD,Bangladesh
EN,ENGLISH,BE,BEL,Belgium
EN,ENGLISH,BF,BFA,Burkina Faso
EN,ENGLISH,BG,BGR,Bulgaria
EN,ENGLISH,BH,BHR,Bahrain
EN,ENGLISH,BI,BDI,Burundi
EN,ENGLISH,BJ,BEN,Benin
EN,ENGLISH,BL,BLM,Saint Barthelemy
EN,ENGLISH,BM,BMU,Bermuda
EN,ENGLISH,BN,BRN,Brunei Darussalam
EN,ENGLISH,BO,BOL,"Bolivia, Plurinational State of"
EN,ENGLISH,BQ,BES,"Bonaire, Sint Eustatius and Saba"
EN,ENGLISH,BR,BRA,Brazil
EN,ENGLISH,BS,BHS,Bahamas
EN,ENGLISH,BT,BTN,Bhutan
EN,ENGLISH,BV,BVT,Bouvet Island
EN,ENGLISH,BW,BWA,Botswana
EN,ENGLISH,BY,BLR,Belarus
EN,ENGLISH,BZ,BLZ,Belize
EN,ENGLISH,CA,CAN,Canada
EN,ENGLISH,CC,CCK,Cocos (Keeling) Islands
EN,ENGLISH,CD,COD,"Congo, The Democratic Republic of The"
EN,ENGLISH,CF,CAF,Central African Republic
EN,ENGLISH,CG,COG,Congo
EN,ENGLISH,CH,CHE,Switzerland
EN,ENGLISH,CI,CIV,Cote D'ivoire
EN,ENGLISH,CK,COK,Cook Islands
EN,ENGLISH,CL,CHL,Chile
EN,ENGLISH,CM,CMR,Cameroon
EN,ENGLISH,CN,CHN,China
EN,ENGLISH,CO,COL,Colombia
EN,ENGLISH,CR,CRI,Costa Rica
EN,ENGLISH,CU,CUB,Cuba
EN,ENGLISH,CV,CPV,Cabo Verde
EN,ENGLISH,CW,CUW,Curacao
EN,ENGLISH,CX,CXR,Christmas Island
EN,ENGLISH,CY,CYP,Cyprus
EN,ENGLISH,CZ,CZE,Czech Republic
EN,ENGLISH,DE,DEU,Germany
EN,ENGLISH,DJ,DJI,Djibouti
EN,ENGLISH,DK,DNK,Denmark
EN,ENGLISH,DM,DMA,Dominica
EN,ENGLISH,DO,DOM,Dominican Republic
EN,ENGLISH,DZ,DZA,Algeria
EN,ENGLISH,EC,ECU,Ecuador
EN,ENGLISH,EE,EST,Estonia
EN,ENGLISH,EG,EGY,Egypt
EN,ENGLISH,EH,ESH,Western Sahara
EN,ENGLISH,ER,ERI,Eritrea
EN,ENGLISH,ES,ESP,Spain
EN,ENGLISH,ET,ETH,Ethiopia
EN,ENGLISH,FI,FIN,Finland
EN,ENGLISH,FJ,FJI,Fiji
EN,ENGLISH,FK,FLK,Falkland Islands (Malvinas)
EN,ENGLISH,FM,FSM,"Micronesia, Federated States of"
EN,ENGLISH,FO,FRO,Faroe Islands
EN,ENGLISH,FR,FRA,France
EN,ENGLISH,GA,GAB,Gabon
EN,ENGLISH,GD,GRD,Grenada
EN,ENGLISH,GE,GEO,Georgia
EN,ENGLISH,GF,GUF,French Guiana
EN,ENGLISH,GG,GGY,Guernsey
EN,ENGLISH,GH,GHA,Ghana
EN_ENGLISH,GI,GIB,Gibraltar
EN,ENGLISH,GL,GRL,Greenland
EN,ENGLISH,GM,GMB,Gambia
EN,ENGLISH,GN,GIN,Guinea
EN,ENGLISH,GP,GLP,Guadeloupe
EN,ENGLISH,GQ,GNQ,Equatorial Guinea
EN,ENGLISH,GR,GRC,Greece
EN,ENGLISH,GS,SGS,South Georgia and The South Sandwich Islands
EN,ENGLISH,GT,GTM,Guatemala
EN,ENGLISH,GU,GUM,Guam
EN,ENGLISH,GW,GNB,Guinea-Bissau
EN,ENGLISH,GY,GUY,Guyana
EN,ENGLISH,HK,HKG,Hong Kong
EN,ENGLISH,HM,HMD,Heard Island and Mcdonald Islands
EN,ENGLISH,HN,HND,Honduras
EN,ENGLISH,HR,HRV,Croatia
EN,ENGLISH,HT,HTI,Haiti
EN,ENGLISH,HU,HUN,Hungary
EN,ENGLISH,ID,IDN,Indonesia
EN,ENGLISH,IE,IRL,Ireland
EN,ENGLISH,IL,ISR,Israel
EN,ENGLISH,IM,IMN,Isle of Man
EN,ENGLISH,IN,IND,India
EN,ENGLISH,IO,IOT,British Indian Ocean Territory
EN,ENGLISH,IQ,IRQ,Iraq
EN,ENGLISH,IR,IRN,"Iran, Islamic Republic of"
EN,ENGLISH,IS,ISL,Iceland
EN,ENGLISH,IT,ITA,Italy
EN,ENGLISH,JE,JEY,Jersey
EN,ENGLISH,JM,JAM,Jamaica
EN,ENGLISH,JO,JOR,Jordan
EN,ENGLISH,JP,JPN,Japan
EN,ENGLISH,KE,KEN,Kenya
EN,ENGLISH,KG,KGZ,Kyrgyzstan
EN,ENGLISH,KH,KHM,Cambodia
EN,ENGLISH,KI,KIR,Kiribati
EN,ENGLISH,KM,COM,Comoros
EN,ENGLISH,KN,KNA,Saint Kitts and Nevis
EN,ENGLISH,KP,PRK,"Korea, Democratic People's Republic of"
EN,ENGLISH,KR,KOR,"Korea, Republic of"
EN,ENGLISH,KW,KWT,Kuwait
EN,ENGLISH,KY,CYM,Cayman Islands
EN,ENGLISH,KZ,KAZ,Kazakhstan
EN,ENGLISH,LA,LAO,Lao People's Democratic Republic
EN,ENGLISH,LB,LBN,Lebanon
EN,ENGLISH,LC,LCA,Saint Lucia
EN,ENGLISH,LI,LIE,Liechtenstein
EN,ENGLISH,LK,LKA,Sri Lanka
EN,ENGLISH,LR,LBR,Liberia
EN,ENGLISH,LS,LSO,Lesotho
EN,ENGLISH,LT,LTU,Lithuania
EN,ENGLISH,LU,LUX,Luxembourg
EN,ENGLISH,LV,LVA,Latvia
EN,ENGLISH,LY,LBY,Libya
EN,ENGLISH,MA,MAR,Morocco
EN,ENGLISH,MC,MCO,Monaco
EN,ENGLISH,MD,MDA,"Moldova, Republic of"
EN,ENGLISH,ME,MNE,Montenegro
EN,ENGLISH,MF,MAF,Saint Martin (French Part)
EN,ENGLISH,MG,MDG,Madagascar
EN,ENGLISH,MH,MHL,Marshall Islands
EN,ENGLISH,MK,MKD,North Macedonia
EN,ENGLISH,ML,MLI,Mali
EN,ENGLISH,MM,MMR,Myanmar
EN,ENGLISH,MN,MNG,Mongolia
EN,ENGLISH,MO,MAC,Macao
EN,ENGLISH,MP,MNP,Northern Mariana Islands
EN,ENGLISH,MQ,MTQ,Martinique
EN,ENGLISH,MR,MRT,Mauritania
EN,ENGLISH,MS,MSR,Montserrat
EN,ENGLISH,MT,MLT,Malta
EN,ENGLISH,MU,MUS,Mauritius
EN,ENGLISH,MV,MDV,Maldives
EN,ENGLISH,MW,MWI,Malawi
EN,ENGLISH,MX,MEX,Mexico
EN,ENGLISH,MY,MYS,Malaysia
EN,ENGLISH,MZ,MOZ,Mozambique
EN,ENGLISH,NA,NAM,Namibia
EN,ENGLISH,NC,NCL,New Caledonia
EN,ENGLISH,NE,NER,Niger
EN,ENGLISH,NF,NFK,Norfolk Island
EN,ENGLISH,NG,NGA,Nigeria
EN,ENGLISH,NI,NIC,Nicaragua
EN,ENGLISH,NL,NLD,Netherlands
EN,ENGLISH,NO,NOR,Norway
EN,ENGLISH,NP,NPL,Nepal
EN,ENGLISH,NR,NRU,Nauru
EN,ENGLISH,NU,NIU,Niue
EN,ENGLISH,NZ,NZL,New Zealand
EN,ENGLISH,OM,OMN,Oman
EN,ENGLISH,PA,PAN,Panama
EN,ENGLISH,PE,PER,Peru
EN,ENGLISH,PF,PYF,French Polynesia
EN,ENGLISH,PG,PNG,Papua New Guinea
EN,ENGLISH,PH,PHL,Philippines
EN,ENGLISH,PK,PAK,Pakistan
EN,ENGLISH,PL,POL,Poland
EN,ENGLISH,PM,SPM,Saint Pierre and Miquelon
EN,ENGLISH,PN,PCN,Pitcairn
EN,ENGLISH,PR,PRI,Puerto Rico
EN,ENGLISH,PS,PSE,"Palestine, State
of"
EN,ENGLISH,PT,PRT,Portugal
EN,ENGLISH,PW,PLW,Palau
EN,ENGLISH,PY,PRY,Paraguay
EN,ENGLISH,QA,QAT,Qatar
EN,ENGLISH,RE,REU,Reunion
EN,ENGLISH,RO,ROU,Romania
EN,ENGLISH,RS,SRB,Serbia
EN,ENGLISH,RU,RUS,Russian Federation
EN,ENGLISH,RW,RWA,Rwanda
EN,ENGLISH,SA,SAU,Saudi Arabia
EN,ENGLISH,SB,SLB,Solomon Islands
EN_ENGLISH,SC,SYC,Seychelles
EN,ENGLISH,SD,SDN,Sudan
EN_ENGLISH,SE,SWE,Sweden
EN,ENGLISH,SG,SGP,Singapore
EN,ENGLISH,SH,SHN,"Saint Helena, Ascension and Tristan Da Cunha"
EN,ENGLISH,SI,SVN,Slovenia
EN,ENGLISH,SJ,SJM,Svalbard and Jan Mayen
EN,ENGLISH,SK,SVK,Slovakia
EN,ENGLISH,SL,SLE,Sierra Leone
EN,ENGLISH,SM,SMR,San Marino
EN,ENGLISH,SN,SEN,Senegal
EN,ENGLISH,SO,SOM,Somalia
EN,ENGLISH,SR,SUR,Suriname
EN,ENGLISH,SS,SSD,South Sudan
EN,ENGLISH,ST,STP,Sao Tome and Principe
EN,ENGLISH,SV,SLV,El Salvador
EN,ENGLISH,SX,SXM,Sint Maarten (Dutch Part)
EN,ENGLISH,SY,SYR,Syrian Arab Republic
EN,ENGLISH,SZ,SWZ,Swaziland
EN,ENGLISH,TC,TCA,Turks and Caicos Islands
EN,ENGLISH,TD,TCD,Chad
EN,ENGLISH,TF,ATF,French Southern Territories
EN,ENGLISH,TG,TGO,Togo
EN,ENGLISH,TH,THA,Thailand
EN,ENGLISH,TJ,TJK,Tajikistan
EN,ENGLISH,TK,TKL,Tokelau
EN,ENGLISH,TL,TLS,Timor-Leste
EN,ENGLISH,TM,TKM,Turkmenistan
EN,ENGLISH,TN,TUN,Tunisia
EN,ENGLISH,TO,TON,Tonga
EN,ENGLISH,TR,TUR,Turkey
EN,ENGLISH,TT,TTO,Trinidad and Tobago
EN,ENGLISH,TV,TUV,Tuvalu
EN,ENGLISH,TW,TWN,"Taiwan, Province of China"
EN,ENGLISH,TZ,TZA,"Tanzania, United Republic of"
EN,ENGLISH,UA,UKR,Ukraine
EN,ENGLISH,UG,UGA,Uganda
EN,ENGLISH,UM,UMI,United States Minor Outlying Islands
EN,ENGLISH,US,USA,United States
EN,ENGLISH,UY,URY,Uruguay
EN,ENGLISH,UZ,UZB,Uzbekistan
EN,ENGLISH,VA,VAT,Holy See
EN,ENGLISH,VC,VCT,Saint Vincent and The Grenadines
EN,ENGLISH,VE,VEN,"Venezuela, Bolivarian Republic of"
EN,ENGLISH,VG,VGB,"Virgin Islands, British"
EN,ENGLISH,VI,VIR,"Virgin Islands, U.S."
EN,ENGLISH,VN,VNM,Viet Nam
EN,ENGLISH,VU,VUT,Vanuatu
EN,ENGLISH,WF,WLF,Wallis and Futuna
EN,ENGLISH,WS,WSM,Samoa
EN,ENGLISH,YE,YEM,Yemen
EN_ENGLISH,YT,MYT,Mayotte
EN,ENGLISH,ZA,ZAF,South Africa
EN,ENGLISH,ZM,ZMB,Zambia
EN,ENGLISH,ZW,ZWE,Zimbabwe"""

currencies_content = """currency_id,currency_type,currency_symbol
1,GBP,£
2,EUR,€
3,USD,$
4,INR,₹"""

tax_info_content = """tax_type_id,country,Tax_Type,tax_percentage
1,UK,VAT,8%
2,India,GST,18%"""

# Read the content into DataFrames
roles_df = pd.read_csv(io.StringIO(roles_content))
departments_df = pd.read_csv(io.StringIO(departments_content))
countries_df = pd.read_csv(io.StringIO(countries_content))
currencies_df = pd.read_csv(io.StringIO(currencies_content))
tax_info_df = pd.read_csv(io.StringIO(tax_info_content))

# Prepare the tax info for calculations
tax_info_df['tax_percentage'] = tax_info_df['tax_percentage'].str.rstrip('%').astype(float) / 100
tax_map = tax_info_df.set_index('country')['tax_percentage'].to_dict()

# --- Generate Data for `Clients` table ---
num_clients = 30
clients_df = pd.DataFrame({
    'client_id': range(1, num_clients + 1),
    'legal_name': [fake.company() for _ in range(num_clients)],
    'business_name': [fake.company() for _ in range(num_clients)],
    'address': [fake.address() for _ in range(num_clients)],
    'contact_person': [fake.name() for _ in range(num_clients)],
})
uk_clients_count = 20
india_clients_count = 10
countries_list = ['UK'] * uk_clients_count + ['India'] * india_clients_count
np.random.shuffle(countries_list)
clients_df['country'] = countries_list
inactive_clients_count = 3
inactive_indices = np.random.choice(clients_df.index, size=inactive_clients_count, replace=False)
clients_df['is_active'] = True
clients_df.loc[inactive_indices, 'is_active'] = False
current_date = datetime.now().date()
clients_df['inactivated_date'] = clients_df['is_active'].apply(lambda x: None if x else current_date)
clients_df['activated_date'] = clients_df['is_active'].apply(lambda x: current_date if x else None)

# --- Generate Data for `Restaurants` table ---
num_restaurants = 50
restaurants_df = pd.DataFrame({
    'restaurant_id': range(1, num_restaurants + 1),
    'name': [fake.company() for _ in range(num_restaurants)],
    'legal_name': [fake.company() for _ in range(num_restaurants)],
    'address': [fake.address() for _ in range(num_restaurants)],
    'phone': [fake.phone_number() for _ in range(num_restaurants)],
    'is_franchise': np.random.choice([True, False], size=num_restaurants, p=[0.2, 0.8]),
    'is_active': True
})
uk_restaurant_count = 40
india_restaurant_count = 10
restaurant_countries = ['UK'] * uk_restaurant_count + ['India'] * india_restaurant_count
np.random.shuffle(restaurant_countries)
restaurants_df['country'] = restaurant_countries
uk_client_ids = clients_df[clients_df['country'] == 'UK']['client_id'].tolist()
india_client_ids = clients_df[clients_df['country'] == 'India']['client_id'].tolist()
restaurants_df['client_id'] = restaurants_df['country'].apply(
    lambda x: np.random.choice(uk_client_ids) if x == 'UK' else np.random.choice(india_client_ids)
)
restaurants_df['currency_id'] = restaurants_df['country'].map({'UK': 1, 'India': 4})

# --- Generate Data for `Subscriptions` table ---
subscriptions_df = pd.DataFrame({
    'subscription_id': range(1, 5),
    'display_name': ['Free', 'Basic', 'Pro', 'Enterprise'],
    'subscription_name': ['Free Plan', 'Basic Plan', 'Pro Plan', 'Enterprise Plan'],
    'product_code': ['FREE', 'BASIC', 'PRO', 'ENT'],
    'subscription_active': True,
    'subscription_code': ['FREE_SUB', 'BASIC_SUB', 'PRO_SUB', 'ENT_SUB'],
    'description': ['Free plan', 'Basic plan', 'Pro plan', 'Enterprise plan'],
    'cost': [0.00, 19.99, 49.99, 199.99],
    'no_of_users': [3, 10, 50, 100]
})

# --- Generate Data for `Users` table ---
num_users = 300
users_df = pd.DataFrame({
    'user_id': range(1, num_users + 1),
    'first_name': [fake.first_name() for _ in range(num_users)],
    'last_name': [fake.last_name() for _ in range(num_users)],
    'email': [fake.email() for _ in range(num_users)],
    'phone': [fake.phone_number() for _ in range(num_users)],
    'address': [fake.address() for _ in range(num_users)],
    'date_of_birth': [fake.date_of_birth(minimum_age=18, maximum_age=65) for _ in range(num_users)],
    'is_active': True,
})
users_df['role_id'] = np.random.choice(roles_df['id'], size=num_users)
users_df['department_id'] = np.random.choice(departments_df['Department_id'], size=num_users)
users_df['restaurant_id'] = np.random.choice(restaurants_df['restaurant_id'], size=num_users, replace=True)
restaurant_client_map = dict(zip(restaurants_df['restaurant_id'], restaurants_df['client_id']))
users_df['client_id'] = users_df['restaurant_id'].map(restaurant_client_map)
subscription_limits = subscriptions_df.set_index('subscription_id')['no_of_users'].to_dict()
user_assignments = []
available_users_indices = list(users_df.index)
for sub_id, limit in subscription_limits.items():
    if len(available_users_indices) > 0:
        num_to_assign = min(limit, len(available_users_indices))
        assigned_indices = np.random.choice(available_users_indices, size=num_to_assign, replace=False)
        for idx in assigned_indices:
            user_assignments.append({'user_id': users_df.loc[idx, 'user_id'], 'subscription_id': sub_id})
        available_users_indices = [idx for idx in available_users_indices if idx not in assigned_indices]
users_with_subs_df = pd.DataFrame(user_assignments)
users_df = users_df.merge(users_with_subs_df, on='user_id', how='left')
users_df['subscription_id'] = users_df['subscription_id'].fillna(1).astype(int)
users_df = users_df.drop_duplicates(subset=['user_id'], keep='first')
user_ids = users_df['user_id'].tolist() # Get the list of all user_ids

# --- Generate Data for `Orders` and `Order_Financials` tables ---
num_restaurants = 50
days_in_year = 365
orders_per_day = 30
start_date = datetime(2024, 1, 1)
order_data = []
order_financials_data = []
order_id_counter = 1

for restaurant_id in range(1, num_restaurants + 1):
    restaurant_country = restaurants_df[restaurants_df['restaurant_id'] == restaurant_id]['country'].iloc[0]
    tax_rate = tax_map.get(restaurant_country, 0)

    for day in range(days_in_year):
        order_date = start_date + timedelta(days=day)

        for _ in range(orders_per_day):
            order_time = (start_date + timedelta(seconds=np.random.randint(0, 86400))).time()
            order_type = np.random.choice(['Home Delivery', 'Dine-in'], p=[0.4, 0.6])

            drinks_amount = round(np.random.uniform(5, 50), 2)
            food_amount = round(np.random.uniform(10, 100), 2)
            other_payment = round(np.random.uniform(0, 20), 2)

            service_charges = 0.0
            delivery_charges = 0.0

            if order_type == 'Dine-in':
                service_charges = round((drinks_amount + food_amount + other_payment) * 0.05, 2)
            elif order_type == 'Home Delivery':
                delivery_charges = round((drinks_amount + food_amount + other_payment) * 0.10, 2)

            order_amount = drinks_amount + food_amount + other_payment + service_charges + delivery_charges
            tax_amount = round(order_amount * tax_rate, 2)
            order_total = round(order_amount + tax_amount, 2)
            
            # Assign a random user_id to each order
            assigned_user_id = np.random.choice(user_ids)

            order_data.append({
                'order_id': order_id_counter,
                'restaurant_id': restaurant_id,
                'user_id': assigned_user_id, # Added the user_id column
                'order_date': order_date.date(),
                'order_time': order_time,
                'order_type': order_type
            })

            order_financials_data.append({
                'order_id': order_id_counter,
                'drinks_amount': drinks_amount,
                'food_amount': food_amount,
                'other_payment': other_payment,
                'service_charges': service_charges,
                'delivery_charges': delivery_charges,
                'order_amount': order_amount,
                'tax_amount': tax_amount,
                'order_total': order_total
            })

            order_id_counter += 1

orders_df = pd.DataFrame(order_data)
order_financials_df = pd.DataFrame(order_financials_data)

# --- Generate Data for `Sales` table ---
orders_with_fin = pd.merge(orders_df, order_financials_df, on='order_id')
sales_df = orders_with_fin.groupby(['restaurant_id', 'order_date']).agg(
    drinks_payment=('drinks_amount', 'sum'),
    food_payment=('food_amount', 'sum'),
    other_payment=('other_payment', 'sum'),
    service_charges=('service_charges', 'sum'),
    delivery_charges=('delivery_charges', 'sum'),
    tax_charges=('tax_amount', 'sum')
).reset_index()
sales_df['creditcard_tip'] = np.random.uniform(0, 10, size=len(sales_df)).round(2)
sales_df['sales_id'] = range(1, len(sales_df) + 1)
sales_df = sales_df.rename(columns={'order_date': 'date'})

# --- Generate Data for `Expenses` table ---
num_records = num_restaurants * days_in_year
expenses_data = {
    'expense_id': range(1, num_records + 1),
    'restaurant_id': np.repeat(range(1, num_restaurants + 1), days_in_year),
    'exp_date': pd.Series(np.tile(pd.date_range(start_date, periods=days_in_year), num_restaurants)).dt.date,
    'bills': np.random.uniform(0, 1000, size=num_records).round(2),
    'vendors': np.random.uniform(0, 200, size=num_records).round(2),
    'wage_advances': np.random.uniform(0, 1000, size=num_records).round(2),
    'repairs': np.random.uniform(0, 2000, size=num_records).round(2),
    'sundries': np.random.uniform(1, 100, size=num_records).round(2)
}
expenses_df = pd.DataFrame(expenses_data)
expenses_df['total_expense'] = expenses_df[['bills', 'vendors', 'wage_advances', 'repairs', 'sundries']].sum(
    axis=1).round(2)

# --- Generate Data for `Cashup` and `Banking` tables ---
cashup_data = []
banking_data = []
eod_per_restaurant = {rid: 0 for rid in range(1, num_restaurants + 1)}
banking_id_counter = 1
start_date_date = start_date.date()

for restaurant_id in range(1, num_restaurants + 1):
    restaurant_sales = sales_df[sales_df['restaurant_id'] == restaurant_id].sort_values('date')
    restaurant_expenses = expenses_df[expenses_df['restaurant_id'] == restaurant_id].sort_values('exp_date')

    for day in range(days_in_year):
        current_date = start_date_date + timedelta(days=day)
        sales_row = restaurant_sales[restaurant_sales['date'] == current_date]
        expenses_row = restaurant_expenses[restaurant_expenses['exp_date'] == current_date]

        if sales_row.empty or expenses_row.empty:
            continue

        sales_row = sales_row.iloc[0]
        expenses_row = expenses_row.iloc[0]

        bod_amount = eod_per_restaurant[restaurant_id] if day > 0 else 0.0
        sales_total = sales_row['drinks_payment'] + sales_row['food_payment'] + sales_row['other_payment']
        expenses_total = expenses_row['total_expense']
        delivery_charges = sales_row['delivery_charges']
        tax_charges = sales_row['tax_charges']

        eod_amount = bod_amount + sales_total - expenses_total - delivery_charges

        banking_total = eod_amount
        max_banked = max(10.0, eod_amount)
        banked_total = round(np.random.uniform(10, max_banked), 2)
        sealed_by_name = fake.name()

        cashup_data.append({
            'cashup_id': len(cashup_data) + 1,
            'restaurant_id': restaurant_id,
            'bod_amount': bod_amount,
            'sales': sales_total,
            'expenses': expenses_total,
            'tax': tax_charges,
            'delivery_charges': delivery_charges,
            'eod_amount': eod_amount,
            'match': True,
            'banking_id': banking_id_counter,
            'cash_up_date': current_date,
            'cashup_status': 'Completed'
        })

        banking_data.append({
            'banking_id': banking_id_counter,
            'banked_total': banked_total,
            'banking_total': banking_total,
            'banking_date': current_date,
            'banking_time_indicator': 'EOD',
            'reconcile_status': 'Reconciled',
            'restaurant_id': restaurant_id,
            'sealed_by': sealed_by_name
        })
        eod_per_restaurant[restaurant_id] = eod_amount - banked_total
        banking_id_counter += 1

cashup_df = pd.DataFrame(cashup_data)
banking_df = pd.DataFrame(banking_data)

# --- Generate Data for `Delivery` table ---
delivery_orders = orders_with_fin[orders_with_fin['order_type'] == 'Home Delivery'].copy()
delivery_orders['delivery_id'] = range(1, len(delivery_orders) + 1)
delivery_orders['order_amount'] = delivery_orders['food_amount'] + delivery_orders['drinks_amount'] + delivery_orders[
    'other_payment']
delivery_orders['api_amount'] = delivery_orders['order_amount'] + (delivery_orders['delivery_charges'] * 0.4)
delivery_orders['name'] = [fake.company() for _ in range(len(delivery_orders))]
delivery_orders['match'] = True

delivery_df = delivery_orders.rename(columns={'order_date': 'delivery_date'})
delivery_df = delivery_df[
    ['delivery_id', 'restaurant_id', 'order_amount', 'api_amount', 'match', 'name', 'delivery_date']]

# --- Create and combine all dataframes into a single Excel file ---
output_file = 'restaurant_data_new.xlsx'
with pd.ExcelWriter(output_file) as writer:
    clients_df.to_excel(writer, sheet_name='Clients', index=False)
    restaurants_df.to_excel(writer, sheet_name='Restaurants', index=False)
    users_df.to_excel(writer, sheet_name='Users', index=False)
    subscriptions_df.to_excel(writer, sheet_name='Subscriptions', index=False)
    orders_df.to_excel(writer, sheet_name='Orders', index=False)
    order_financials_df.to_excel(writer, sheet_name='Order_Financials', index=False)
    sales_df.to_excel(writer, sheet_name='Sales', index=False)
    expenses_df.to_excel(writer, sheet_name='Expenses', index=False)
    cashup_df.to_excel(writer, sheet_name='Cashup', index=False)
    banking_df.to_excel(writer, sheet_name='Banking', index=False)
    delivery_df.to_excel(writer, sheet_name='Delivery', index=False)
    roles_df.to_excel(writer, sheet_name='Roles', index=False)
    departments_df.to_excel(writer, sheet_name='Departments', index=False)
    countries_df.to_excel(writer, sheet_name='Countries', index=False)
    currencies_df.to_excel(writer, sheet_name='Currencies', index=False)
    tax_info_df.to_excel(writer, sheet_name='TaxInfo', index=False)
