import streamlit as st
import pandas as pd
import altair as alt

# Page configuration
st.set_page_config(
    page_title="Exec Dash",
    page_icon="⭐", layout="wide",
    initial_sidebar_state="expanded")

# Define the navigation items and their corresponding URLs
navigation_items = {
    "Homepage": "none",
    "Exec Dash": "https://sales-app-execdash1.streamlit.app/",
    "Products Dash": "https://sales-app-itemsdash1.streamlit.app/"

#######################
# Load data
order_details = pd.read_csv('order_details.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv', encoding='latin1')
categories = pd.read_csv('categories.csv', encoding='latin1')
employees = pd.read_csv('employees.csv', encoding='latin1')

# Prepare the data: Aggregate revenue by year and month
orders['orderDate'] = pd.to_datetime(orders['orderDate'])
orders['Year'] = orders['orderDate'].dt.year
orders['Month'] = orders['orderDate'].dt.month
order_details['Revenue'] = order_details['unitPrice'] * order_details['quantity'] * (1 - order_details['discount'])
revenue_data = order_details.merge(orders[['orderID', 'Year', 'Month']], on='orderID')
revenue_data = revenue_data.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()

# Convert 'Month' column to categorical with the defined order
revenue_data['Month'] = pd.Categorical(revenue_data['Month'])

#######################
# Sidebar
# Load your image
image = 'northwindlogo.png'
st.sidebar.image(image, use_column_width=True)

with st.sidebar:
    st.title('⭐ Exec Dash')
    st.sidebar.subheader('KPIs & Revenue Trending Analysis')
    year_list = sorted(orders['Year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox('Select a year', year_list)
    st.sidebar.subheader('Product Analysis')
    selected_category = st.sidebar.selectbox("Select a category", categories["categoryName"].unique())
    # Navigation
    st.write("## Navigation")
    for item, url in navigation_items.items():
        st.markdown(f"[ {item} ]({url})", unsafe_allow_html=True)
        
    st.sidebar.markdown('''Created with ❤️ by **Lin WANG & Shuhui TANG**''')

# Filter data based on selected year
revenue_year = revenue_data[revenue_data['Year'] == selected_year]

#######################
# 1. Revenue Trending Line chart
chart = alt.Chart(revenue_year).mark_line().encode(
x=alt.X('Month', axis=alt.Axis(labelAngle=0)), 
y=alt.Y('Revenue', axis=alt.Axis(title='Revenue')),
tooltip=['Year', 'Month', 'Revenue']
).properties(
title=f'Revenue Trending for {selected_year}',
width=700,
height=400
).interactive()

#######################
# 2. KPIs
# Calculate Total Revenue for selected year
order_details_selected_year = order_details[order_details['orderID'].isin(orders[orders['Year'] == selected_year]['orderID'])]
total_revenue_selected_year = order_details_selected_year['Revenue'].sum()

# Calculate Total Orders for selected year
total_orders_selected_year = orders[orders['Year'] == selected_year]['orderID'].nunique()

# Define layout with two columns
col1, col2 = st.columns([1,2])  

# First column: KPIs
with col1:
    st.header('KPIs')
    st.metric(label="Total Revenue", value=f"${total_revenue_selected_year:,.2f}")
    st.metric(label="Total Orders", value=total_orders_selected_year)

# Second column: Revenue Trending Line chart
with col2:
    st.altair_chart(chart, use_container_width=True)

#######################
# 3. Top-selling product & Highest-earning product
# 4. Top three performing employees

# Merge data
merged_data = order_details.merge(products[['productID', 'productName', 'categoryID']], on='productID')
merged_data = merged_data.merge(categories[['categoryID', 'categoryName']], on='categoryID')
merged_data = merged_data.merge(orders[['orderID', 'employeeID']], on='orderID')

# Calculate revenue for each product
merged_data['TotalRevenue'] = merged_data['unitPrice'] * merged_data['quantity'] * (1 - merged_data['discount'])

# Best-selling and highest-earning product by category
def get_best_selling_products(category):
    category_data = merged_data[merged_data['categoryName'] == category]
    best_selling_product = category_data.groupby('productName')['quantity'].sum().idxmax()
    highest_earning_product = category_data.groupby('productName')['TotalRevenue'].sum().idxmax()
    return best_selling_product, highest_earning_product

best_selling_product, highest_earning_product = get_best_selling_products(selected_category)

# Top 3 employees in sales revenue
top_employees = merged_data.groupby('employeeID')['TotalRevenue'].sum().nlargest(3).reset_index()
top_employees = top_employees.merge(employees[['employeeID', 'employeeName']], on='employeeID')

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader(f'Best-selling product in {selected_category}')
    st.write(best_selling_product)

    st.subheader(f'Highest-earning product in {selected_category}')
    st.write(highest_earning_product)

with col2:
    st.subheader('Top 3 employees in sales revenue')
    st.write(top_employees[['employeeName', 'TotalRevenue']])
    

