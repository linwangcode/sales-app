import streamlit as st


# Page configuration
st.set_page_config(
page_title="Home",
page_icon="🏠", layout="wide",
initial_sidebar_state="expanded")

# Define the navigation items and their corresponding URLs
navigation_items = {
    "Homepage": "https://sales-app-homepage1.streamlit.app/",
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
    st.sidebar.markdown('''Created with ❤️ by **Lin WANG & Shuhui TANG**''')
    # Redirect based on selected item using JavaScript
    redirect_script = f"""
    <script>
        function redirectToPage() {{
            var selectbox = document.getElementById('selectbox');
            var selectedOption = selectbox.options[selectbox.selectedIndex].value;
            window.location.href = selectedOption;
        }}
        document.getElementById('selectbox').addEventListener('change', redirectToPage);
    </script>
    """
    st.markdown(redirect_script, unsafe_allow_html=True)

    # Adding an empty line to create space
    st.sidebar.write("") 

# Display the selected dashboard
if selected_item in navigation_items:
    st.markdown(f"Redirecting to [{selected_item}]({navigation_items[selected_item]})...")

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


