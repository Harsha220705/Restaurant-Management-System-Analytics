import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mysql.connector
from mysql.connector import Error
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Restaurant Management Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Currency conversion rates from USD to various currencies
CURRENCY_MAP = {
    'Europe': {'symbol': '€', 'conversion_rate': 0.93},
    'United Kingdom': {'symbol': '£', 'conversion_rate': 0.81},
    'India': {'symbol': '₹', 'conversion_rate': 83.33},
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='harsha@2207',
            database='restaurant_management'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None


@st.cache_data
def load_data(query):
    connection = connect_to_database()
    if connection:
        try:
            df = pd.read_sql(query, connection)
            connection.close()
            return df
        except Exception as e:
            connection.close()
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def get_currency_details(country_name):
    if country_name == 'India':
        return CURRENCY_MAP['India']
    elif country_name == 'United Kingdom':
        return CURRENCY_MAP['United Kingdom']
    else:
        return CURRENCY_MAP['Europe']


def show_workforce_allocation(currency_symbol, conversion_rate):
    st.header("⏳ Workforce Allocation")
    st.markdown("""
    **Insight:** Analyze order volume by hour to identify peak times for strategic employee scheduling for a specific restaurant.
    """)

    restaurants = load_data("SELECT DISTINCT name, country FROM Restaurants WHERE is_active = 1")
    if restaurants.empty:
        st.warning("No active restaurants found in the database. Cannot perform analysis.")
        return

    restaurant_names = ['All Restaurants'] + restaurants['name'].tolist()
    selected_restaurant = st.selectbox("Select a Restaurant", restaurant_names, key='workforce_restaurant_select')

    if selected_restaurant == 'All Restaurants':
        query = """
            SELECT HOUR(order_time) as order_hour, COUNT(*) as order_count
            FROM Orders
            GROUP BY order_hour
            ORDER BY order_hour ASC
        """
        title = 'Order Volume by Hour of Day (All Restaurants)'
    else:
        query = f"""
            SELECT HOUR(o.order_time) as order_hour, COUNT(*) as order_count
            FROM Orders o
            JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
            WHERE r.name = '{selected_restaurant}'
            GROUP BY order_hour
            ORDER BY order_hour ASC
        """
        title = f'Order Volume by Hour of Day for {selected_restaurant}'

    order_by_hour = load_data(query)
    if not order_by_hour.empty:
        fig = px.bar(order_by_hour, x='order_hour', y='order_count',
                     title=title,
                     labels={'order_hour': 'Hour of Day (24h)', 'order_count': 'Number of Orders'},
                     color='order_count', color_continuous_scale=px.colors.sequential.Viridis)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No order data available for {selected_restaurant} to show trends.")


def show_order_type_and_revenue_analysis(currency_symbol, conversion_rate):
    st.header("🛒 Order Type and Revenue Analysis")
    st.markdown("""
    **Insight:** Analyze the distribution of revenue and order volume by order type for a specific restaurant.
    """)
    
    restaurants = load_data("SELECT DISTINCT name, country FROM Restaurants WHERE is_active = 1")
    
    if restaurants.empty:
        st.warning("No active restaurants found in the database. Cannot perform analysis.")
        return
        
    selected_restaurant = st.selectbox("Select a Restaurant", restaurants['name'].tolist(), key='order_type_restaurant_select')
    selected_country = restaurants[restaurants['name'] == selected_restaurant]['country'].iloc[0]
    currency_details = get_currency_details(selected_country)
    
    order_metrics_query = f"""
        SELECT o.order_type,
               COUNT(o.order_id) as order_count,
               SUM(ofin.order_total) as total_revenue
        FROM Orders o
        JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
        LEFT JOIN Order_Financials ofin ON o.order_id = ofin.order_id
        WHERE r.name = '{selected_restaurant}'
        GROUP BY o.order_type
        ORDER BY order_count DESC
    """
    order_metrics_data = load_data(order_metrics_query)
    
    revenue_breakdown_query = f"""
        SELECT SUM(ofin.food_amount) as food_revenue,
               SUM(ofin.drinks_amount) as drinks_revenue,
               SUM(ofin.other_payment) as other_revenue
        FROM Orders o
        JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
        LEFT JOIN Order_Financials ofin ON o.order_id = ofin.order_id
        WHERE r.name = '{selected_restaurant}'
    """
    revenue_breakdown_data = load_data(revenue_breakdown_query)

    if not order_metrics_data.empty and not revenue_breakdown_data.empty:
        order_metrics_data['total_revenue'] *= currency_details['conversion_rate']
        revenue_breakdown_data['food_revenue'] *= currency_details['conversion_rate']
        revenue_breakdown_data['drinks_revenue'] *= currency_details['conversion_rate']
        revenue_breakdown_data['other_revenue'] *= currency_details['conversion_rate']

        col1, col2 = st.columns(2)
        with col1:
            fig_revenue = px.pie(order_metrics_data,
                                 values='total_revenue',
                                 names='order_type',
                                 title=f"Revenue by Order Type for {selected_restaurant} ({currency_details['symbol']})")
            st.plotly_chart(fig_revenue, use_container_width=True)

        with col2:
            fig_orders = px.pie(order_metrics_data,
                                values='order_count',
                                names='order_type',
                                title=f"Orders by Order Type for {selected_restaurant}")
            st.plotly_chart(fig_orders, use_container_width=True)
            
        st.subheader(f"Revenue Breakdown for {selected_restaurant}")

        breakdown_df = pd.DataFrame({
            'Revenue Type': ['Food', 'Drinks', 'Other'],
            'Amount': [revenue_breakdown_data['food_revenue'].iloc[0],
                       revenue_breakdown_data['drinks_revenue'].iloc[0],
                       revenue_breakdown_data['other_revenue'].iloc[0]]
        })

        fig_breakdown = px.bar(breakdown_df,
                               x='Revenue Type',
                               y='Amount',
                               title=f"Revenue Breakdown by Category ({currency_details['symbol']})",
                               labels={'Amount': f"Revenue ({currency_details['symbol']})"},
                               color='Revenue Type',
                               color_discrete_map={'Food': 'orange', 'Drinks': 'blue', 'Other': 'green'})
        st.plotly_chart(fig_breakdown, use_container_width=True)

    else:
        st.warning(f"No order data available for {selected_restaurant} to show trends.")

def show_client_restaurant_performance(currency_symbol, conversion_rate):
    st.header("🏢 Client & Restaurant Performance")
    st.markdown("""
    **Insight:** Analyze profit trends for a client's restaurants over time and identify which are growing.
    """)

    clients_df = load_data("SELECT client_id, legal_name, country FROM Clients WHERE is_active = 1")
    if clients_df.empty:
        st.warning("No active clients found in the database.")
        return
    
    client_names = clients_df['legal_name'].tolist()
    selected_client_name = st.selectbox("Select a Client", client_names, key='client_select')
    selected_client_id = clients_df[clients_df['legal_name'] == selected_client_name]['client_id'].iloc[0]
    
    restaurants_query = f"SELECT name FROM Restaurants WHERE is_active = 1 AND client_id = {selected_client_id}"
    restaurants_df = load_data(restaurants_query)
    
    if restaurants_df.empty:
        st.warning(f"No active restaurants found for client '{selected_client_name}'.")
        return
    
    restaurant_names_list = ['All Restaurants'] + sorted(restaurants_df['name'].tolist())
    selected_restaurant = st.selectbox("Select a Restaurant", restaurant_names_list, key='restaurant_select')
    
    period_options = ['Monthly', 'Yearly']
    selected_period = st.radio("Select Period", period_options)

    date_format = '%Y-%m' if selected_period == 'Monthly' else '%Y'
    date_col_name = 'month' if selected_period == 'Monthly' else 'year'

    if selected_restaurant == 'All Restaurants':
        where_clause = f"c.legal_name = '{selected_client_name}' AND r.is_active = 1"
    else:
        where_clause = f"r.name = '{selected_restaurant}' AND r.is_active = 1"

    query = f"""
        SELECT 
            r.name as restaurant_name,
            r.country as restaurant_country,
            DATE_FORMAT(o.order_date, '{date_format}') as period,
            SUM(ofin.order_total) as total_revenue,
            COALESCE(SUM(e.total_expense), 0) as total_expenses,
            (SUM(ofin.order_total) - COALESCE(SUM(e.total_expense), 0)) as net_profit
        FROM Clients c
        JOIN Restaurants r ON c.client_id = r.client_id
        LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id
        LEFT JOIN Order_Financials ofin ON o.order_id = ofin.order_id
        LEFT JOIN Expenses e ON r.restaurant_id = e.restaurant_id 
             AND DATE_FORMAT(e.exp_date, '{date_format}') = DATE_FORMAT(o.order_date, '{date_format}')
        WHERE {where_clause}
        GROUP BY r.name, restaurant_country, period
        ORDER BY r.name, period ASC
    """
    analysis_data = load_data(query)

    if not analysis_data.empty:
        if selected_restaurant == 'All Restaurants':
            client_country = clients_df[clients_df['legal_name'] == selected_client_name]['country'].iloc[0]
            currency_details = get_currency_details(client_country)
        else:
            selected_country = analysis_data['restaurant_country'].iloc[0]
            currency_details = get_currency_details(selected_country)

        conversion_rate = currency_details['conversion_rate']
        currency_symbol = currency_details['symbol']

        analysis_data['total_revenue'] *= conversion_rate
        analysis_data['total_expenses'] *= conversion_rate
        analysis_data['net_profit'] *= conversion_rate

        fig = px.line(analysis_data, x='period', y='net_profit', color='restaurant_name',
                      title=f'Net Profit Trend ({selected_period})',
                      labels={'period': selected_period, 'net_profit': f'Net Profit ({currency_symbol})'})
        st.plotly_chart(fig, use_container_width=True)




def show_restaurant_financial_health(currency_symbol, conversion_rate):
    st.header("💰 Restaurant Financial Health Tracker")
    st.markdown(f"**Insight:** Calculate each outlet's financial performance by comparing end-of-day sales to operating expenses, displayed in {currency_symbol}.")

    # Optimized SQL Query
    query = """
        SELECT
            r.name AS restaurant_name,
            COALESCE(sales_agg.total_sales, 0) AS total_sales,
            COALESCE(expenses_agg.total_expenses, 0) AS total_expenses,
            (COALESCE(sales_agg.total_sales, 0) - COALESCE(expenses_agg.total_expenses, 0)) AS net_profit,
            CASE
                WHEN COALESCE(sales_agg.total_sales, 0) > 0
                THEN ((COALESCE(sales_agg.total_sales, 0) - COALESCE(expenses_agg.total_expenses, 0)) / COALESCE(sales_agg.total_sales, 0)) * 100
                ELSE 0
            END AS profit_margin_pct
        FROM
            Restaurants r
        LEFT JOIN
            (SELECT restaurant_id, SUM(food_payment + drinks_payment + other_payment) AS total_sales FROM Sales GROUP BY restaurant_id) AS sales_agg
            ON r.restaurant_id = sales_agg.restaurant_id
        LEFT JOIN
            (SELECT restaurant_id, SUM(total_expense) AS total_expenses FROM Expenses GROUP BY restaurant_id) AS expenses_agg
            ON r.restaurant_id = expenses_agg.restaurant_id
        WHERE
            r.is_active = 1;
    """

    financial_health = load_data(query)

    if financial_health.empty:
        st.error("No financial data available. Please check that the Sales and Expenses tables exist and contain data.")
        return

    # Filter out rows with zero or negative sales to prevent division by zero in the chart
    financial_health = financial_health[financial_health['total_sales'] > 0].copy()

    # Convert to appropriate currency
    financial_health['total_sales'] *= conversion_rate
    financial_health['total_expenses'] *= conversion_rate
    financial_health['net_profit'] *= conversion_rate

    # Health status classification
    financial_health['health_status'] = financial_health['profit_margin_pct'].apply(
        lambda x: 'Excellent' if x > 20 else 'Good' if x > 10 else 'Average' if x > 0 else 'Needs Attention'
    )

    col1, col2 = st.columns(2)

    with col1:
        # Profit margin distribution
        fig = px.histogram(financial_health, x='profit_margin_pct',
                           title='Profit Margin Distribution',
                           labels={'profit_margin_pct': 'Profit Margin (%)', 'count': 'Number of Restaurants'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Health status pie chart
        status_counts = financial_health['health_status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                     title='Restaurant Financial Health Status')
        st.plotly_chart(fig, use_container_width=True)

    # Scatter plot for sales vs profit margin
    st.subheader(f"🔥 Financial Performance Scatter Plot ({currency_symbol})")
    fig = px.scatter(financial_health, x='total_sales', y='net_profit',
                     color='profit_margin_pct', size='total_sales',
                     hover_name='restaurant_name',
                     title=f'Sales vs. Net Profit with Profit Margin ({currency_symbol})',
                     labels={'total_sales': f'Total Sales ({currency_symbol})', 'net_profit': f'Net Profit ({currency_symbol})', 'profit_margin_pct': 'Profit Margin (%)'})
    st.plotly_chart(fig, use_container_width=True)

    # Alert system
    st.subheader("🚨 Financial Health Alerts")
    needs_attention = financial_health[financial_health['health_status'] == 'Needs Attention']
    if not needs_attention.empty:
        st.error(f"⚠️ {len(needs_attention)} restaurants need immediate attention!")
        for _, restaurant in needs_attention.iterrows():
            st.warning(f"🏪 **{restaurant['restaurant_name']}**: {restaurant['profit_margin_pct']:.1f}% margin")
    else:
        st.success("✅ All restaurants are financially healthy!")

def show_daily_performance_dashboard(currency_symbol, conversion_rate):
    st.header("📊 Daily Restaurant Performance Dashboard")
    st.markdown(f"**Insight:** Track daily sales figures, outgoing expenses, and cash flow metrics to evaluate overall restaurant health, displayed in {currency_symbol}.")
    
    # Date selector
    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Select Date for Analysis", value=pd.Timestamp.now().date())
    with col2:
        restaurant_filter = load_data("SELECT DISTINCT name FROM Restaurants WHERE is_active = 1")
        if not restaurant_filter.empty:
            selected_restaurant = st.selectbox("Select Restaurant", 
                                             options=['All'] + restaurant_filter['name'].tolist(), key='daily_performance_restaurant_select')
    
    # Daily performance metrics (Corrected column names and syntax)
    if selected_restaurant == 'All':
        restaurant_condition = ""
    else:
        restaurant_condition = f"AND r.name = '{selected_restaurant}'"
    
    daily_performance = load_data(f"""
        SELECT 
            r.name as restaurant_name,
            COALESCE(SUM(s.food_payment + s.drinks_payment + s.other_payment), 0) as daily_sales,
            COALESCE(SUM(e.total_expense), 0) as daily_expenses,
            COALESCE(SUM(c.eod_amount), 0) as end_of_day_cash,
            COUNT(o.order_id) as daily_orders,
            COALESCE(AVG(ofin.order_total), 0) as avg_order_value
        FROM Restaurants r
        LEFT JOIN Sales s ON r.restaurant_id = s.restaurant_id AND s.date = '{selected_date}'
        LEFT JOIN Expenses e ON r.restaurant_id = e.restaurant_id AND e.exp_date = '{selected_date}'
        LEFT JOIN Orders o ON r.restaurant_id = o.restaurant_id AND o.order_date = '{selected_date}'
        LEFT JOIN Order_Financials ofin ON o.order_id = ofin.order_id
        LEFT JOIN Cashup c ON r.restaurant_id = c.restaurant_id AND c.cash_up_date = '{selected_date}'
        WHERE r.is_active = 1 {restaurant_condition}
        GROUP BY r.restaurant_id, r.name
        HAVING daily_sales > 0 OR daily_expenses > 0
    """)
    
    if not daily_performance.empty:
        # Convert to appropriate currency
        daily_performance['daily_sales'] *= conversion_rate
        daily_performance['daily_expenses'] *= conversion_rate
        daily_performance['end_of_day_cash'] *= conversion_rate
        daily_performance['avg_order_value'] *= conversion_rate
        
        # Calculate derived metrics
        daily_performance['net_profit'] = daily_performance['daily_sales'] - daily_performance['daily_expenses']
        daily_performance['profit_margin'] = (daily_performance['net_profit'] / daily_performance['daily_sales'] * 100).fillna(0)
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_sales = daily_performance['daily_sales'].sum()
            st.metric("Total Daily Sales", f"{currency_symbol}{total_sales:,.2f}")
        with col2:
            total_expenses = daily_performance['daily_expenses'].sum()
            st.metric("Total Daily Expenses", f"{currency_symbol}{total_expenses:,.2f}")
        with col3:
            net_profit = total_sales - total_expenses
            st.metric("Net Profit", f"{currency_symbol}{net_profit:,.2f}", delta=f"{(net_profit/total_sales*100):.1f}%" if total_sales > 0 else None)
        with col4:
            total_orders = daily_performance['daily_orders'].sum()
            st.metric("Total Orders", f"{total_orders:,}")
        
        # Performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sales vs Expenses
            fig, ax = plt.subplots(figsize=(10, 6))
            x = range(len(daily_performance))
            width = 0.35
            ax.bar([i - width/2 for i in x], daily_performance['daily_sales'], 
                  width, label='Sales', alpha=0.8, color='green')
            ax.bar([i + width/2 for i in x], daily_performance['daily_expenses'], 
                  width, label='Expenses', alpha=0.8, color='red')
            ax.set_xlabel('Restaurants')
            ax.set_ylabel(f'Amount ({currency_symbol})')
            ax.set_title(f'Daily Sales vs Expenses by Restaurant ({currency_symbol})')
            ax.set_xticks(x)
            ax.set_xticklabels(daily_performance['restaurant_name'], rotation=45)
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            # Profit margin gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = daily_performance['profit_margin'].mean(),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Average Profit Margin (%)"},
                delta = {'reference': 15},
                gauge = {'axis': {'range': [None, 50]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 10], 'color': "lightgray"},
                            {'range': [10, 25], 'color': "gray"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 15}}))
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed performance table
        st.subheader("📋 Detailed Daily Performance")
        daily_performance['health_status'] = daily_performance['profit_margin'].apply(
            lambda x: '🟢 Excellent' if x > 20 else '🟡 Good' if x > 10 else '🔴 Needs Attention'
        )
        st.dataframe(daily_performance, use_container_width=True)
        
        # Alerts and recommendations
        st.subheader("🚨 Daily Alerts")
        poor_performers = daily_performance[daily_performance['profit_margin'] < 5]
        if not poor_performers.empty:
            st.error(f"⚠️ {len(poor_performers)} restaurants showing poor performance today!")
            for _, restaurant in poor_performers.iterrows():
                st.warning(f"🏪 {restaurant['restaurant_name']}: {restaurant['profit_margin']:.1f}% margin")
        else:
            st.success("✅ All restaurants performing well today!")


def main():
    st.markdown('<h1 class="main-header">🍽️ Restaurant Management Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        [
            "Workforce Allocation",
            "Restaurant Financial Health",
            "Order Volume Trends",
            "Client & Restaurant Performance",
            "Daily Restaurant Performance Dashboard"
        ]
    )

    def _get_selected_restaurant_name(key):
        return st.session_state.get(key, None)

    restaurants_df = load_data("SELECT DISTINCT name, country FROM Restaurants WHERE is_active = 1")
    currency_symbol, conversion_rate = '€', 0.93

    if 'workforce_restaurant_select' in st.session_state and st.session_state['workforce_restaurant_select'] != 'All Restaurants' and not restaurants_df.empty:
        selected_restaurant = st.session_state['workforce_restaurant_select']
        selected_country = restaurants_df[restaurants_df['name'] == selected_restaurant]['country'].iloc[0]
        currency_details = get_currency_details(selected_country)
        currency_symbol = currency_details['symbol']
        conversion_rate = currency_details['conversion_rate']

    elif 'restaurant_select' in st.session_state and st.session_state['restaurant_select'] != 'All Restaurants' and not restaurants_df.empty:
        selected_restaurant = st.session_state['restaurant_select']
        selected_country = restaurants_df[restaurants_df['name'] == selected_restaurant]['country'].iloc[0]
        currency_details = get_currency_details(selected_country)
        currency_symbol = currency_details['symbol']
        conversion_rate = currency_details['conversion_rate']
        
    elif 'daily_performance_restaurant_select' in st.session_state and st.session_state['daily_performance_restaurant_select'] != 'All' and not restaurants_df.empty:
        selected_restaurant = st.session_state['daily_performance_restaurant_select']
        selected_country = restaurants_df[restaurants_df['name'] == selected_restaurant]['country'].iloc[0]
        currency_details = get_currency_details(selected_country)
        currency_symbol = currency_details['symbol']
        conversion_rate = currency_details['conversion_rate']
    
    with st.spinner("Connecting to database..."):
        try:
            connection = connect_to_database()
            if connection:
                st.sidebar.success("✅ Database Connected")
                connection.close()
            else:
                st.sidebar.error("❌ Database Connection Failed")
                st.stop()
        except Exception as e:
            st.sidebar.error(f"❌ Database Connection Failed: {e}")
            st.stop()
    
    if page == "Workforce Allocation":
        show_workforce_allocation(currency_symbol, conversion_rate)
    elif page == "Restaurant Financial Health":
        show_restaurant_financial_health(currency_symbol, conversion_rate)
    elif page == "Order Volume Trends":
        show_order_type_and_revenue_analysis(currency_symbol, conversion_rate)
    elif page == "Client & Restaurant Performance":
        show_client_restaurant_performance(currency_symbol, conversion_rate)
    elif page == "Daily Restaurant Performance Dashboard":
        show_daily_performance_dashboard(currency_symbol, conversion_rate)


if __name__ == "__main__":
    main()

