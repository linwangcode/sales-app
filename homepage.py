import streamlit as st


# Page configuration
st.set_page_config(
page_title="Home",
page_icon="🏠", layout="wide",
initial_sidebar_state="expanded")

# Define the navigation items and their corresponding URLs
navigation_items = {
    "Exec Dash": "https://sales-app-execdash1.streamlit.app/",
    "Products Dash": "https://sales-app-itemsdash1.streamlit.app/"
}

st.write("# 📊 Northwind Trader Sales Report")

# Load your image
image = 'northwindlogo.png'
st.sidebar.image(image, use_column_width=True)

# Sidebar
with st.sidebar:
    st.title('🏠 Home')
    st.write("## Navigation")
    selected_item = st.selectbox("Select a dashboard", list(navigation_items.keys()))
    if selected_item in navigation_items:
        st.markdown(f"[{selected_item}]({navigation_items[selected_item]})")
    st.sidebar.markdown('''Created with ❤️ by **Lin WANG & Shuhui TANG**''')

st.markdown(
    """
    Northwind Traders, a fictitious gourmet food supplier. This app aims to report to **a sales manager**
    about the analysis of the sales, revenue, products, and customers.

    **👈 Select a dashboard from the sidebar** to navigate.
    ### 🎯 The Objectives
    - Discover sales and order volume trends over time
    - Find out best-selling product categories and names
    - Analyze whether discounts have a positive impact on total orders
    - Identify the key customers and the customer distribution
    - Find the top 3 employees by sales revenue
    """
    )

st.write('---')  # Add a horizontal line to separate the navigation bar from the content

st.write("## Navigation")

# Iterate through the navigation items and create links
for item, url in navigation_items.items():
    st.markdown(f"[{item}]({url})")
