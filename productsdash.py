import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Page configuration

st.set_page_config(
    page_title="Products",
    page_icon="🥕", layout="wide",
    initial_sidebar_state="expanded")

# Define the navigation items and their corresponding URLs
navigation_items = {
    "Homepage": "none",
    "Exec Dash": "https://sales-app-execdash1.streamlit.app/",
    "Products Dash": "https://sales-app-itemsdash1.streamlit.app/"
}

#######################
# Load data
order_details = pd.read_csv('order_details.csv')
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv', encoding='latin1')
categories = pd.read_csv('categories.csv', encoding='latin1')

# Merge data
merged_df = pd.merge(order_details, products, on='productID')
merged_df = pd.merge(merged_df, categories, on='categoryID')
merged_df = pd.merge(orders, merged_df, on='orderID')

# Convert orderDate to datetime
merged_df['orderDate'] = pd.to_datetime(merged_df['orderDate'])
merged_df['year'] = merged_df['orderDate'].dt.year
merged_df['month'] = merged_df['orderDate'].dt.month

#######################
# Load your image
image = 'northwindlogo.png'
st.sidebar.image(image, use_column_width=True)

# Sidebar
with st.sidebar:
    st.title('🥕 Products')
    selected_year = st.selectbox('Select a year', options=sorted(merged_df['year'].unique(), reverse=True))
    st.write("## Navigation")
    for item, url in navigation_items.items():
        st.markdown(f"[ {item} ]({url})", unsafe_allow_html=True)
    
    st.sidebar.markdown('''Created with ❤️ by **Lin WANG & Shuhui TANG**''')

filtered_df = merged_df[merged_df['year'] == selected_year]

#######################
# Function to plot the chart
def plot_combo_chart(year):
    filtered_data = filtered_df[filtered_df['year'] == year]

    # Group by month and calculate quantities
    monthly_data = filtered_df.groupby('month').agg({'quantity': 'sum', 'discount': lambda x: (x > 0).sum()})

    # Plot the combo chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Line chart for total orders
    ax1.plot(monthly_data.index, monthly_data['quantity'], color='blue', label='Total Orders')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Total Orders', color='blue')
    ax1.tick_params('y', colors='blue')
    ax1.set_title(f'Total Orders vs Quantity of Discounted Products for the Year {year}')

    # Bar chart for quantity of discounted products
    ax2 = ax1.twinx()
    ax2.bar(monthly_data.index, monthly_data['discount'], color='grey', alpha=0.5, label='Discounted Products')
    ax2.set_ylabel('Quantity of Discounted Products', color='red')
    ax2.tick_params('y', colors='red')

    # Add legend
    fig.legend(loc="upper left", bbox_to_anchor=(0.15,0.85))

    return fig

#######################
# Function to plot the bar chart for orders by categories
def plot_orders_by_categories(year):
    filtered_data = filtered_df[filtered_df['year'] == year]

    # Group by category and calculate total volume of orders
    category_data = filtered_data.groupby('categoryName').agg({'quantity': 'sum'})

    # Plot the bar chart for orders by categories
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(category_data.index, category_data['quantity'], color='grey', alpha=0.5)
    ax.set_xlabel('Categories')
    ax.set_ylabel('Total Volume of Orders')
    ax.set_title(f'Orders by Category for the Year {year}')
    ax.tick_params(axis='x', rotation=45)

    return fig

st.subheader('Impact of Discount on Order Quantity')
combo_chart_fig = plot_combo_chart(selected_year)
st.pyplot(combo_chart_fig)

st.subheader('Orders by Category')
orders_by_categories_fig = plot_orders_by_categories(selected_year)
st.pyplot(orders_by_categories_fig)

#######################
# Calculate revenue for each product
filtered_df['revenue'] = filtered_df['quantity'] * filtered_df['unitPrice_x'] * (1 - filtered_df['discount'])

# Group by product and calculate total revenue
product_revenue = filtered_df.groupby('productName')['revenue'].sum().reset_index()

# Sort products by revenue and get top 10
top_10_products = product_revenue.sort_values(by='revenue', ascending=False).head(10)

# Display top 10 products in a table
st.subheader('Top 10 Products by Revenue')
st.table(top_10_products)
