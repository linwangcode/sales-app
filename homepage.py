import streamlit as st


# Page configuration
st.set_page_config(
page_title="Home",
page_icon="🏠", layout="wide",
initial_sidebar_state="expanded")

# Define the navigation items and their corresponding URLs
navigation_items = {
    "Homepage": "none",
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
    st.buttons(item)
    for item, url in navigation_items.items():
        st.markdown(f"[ {item} ]({url})", unsafe_allow_html=True)

# Create a hidden iframe element
st.markdown('<iframe id="frame" name="frame" style="display: none;"></iframe>', unsafe_allow_html=True)
            
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


