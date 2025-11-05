import streamlit as st
from web_functions import load_data
from auth.auth_manager import init_auth, check_session, show_auth_pages

from Tabs import diagnosis, home, result, kc, talk2doc, profile

# Configure the app
st.set_page_config(
    page_title = 'Diabetes Prediction System',
    page_icon = '🥯',
    layout = 'wide',
    initial_sidebar_state = 'auto'
)

# Initialize authentication
init_auth()

Tabs = {
    "Home":home,
    "Ask Queries":talk2doc,
    "Diagnosis":diagnosis,
    "Result":result,
    "Knowledge Center":kc,
    "Profile":profile
}

# Check authentication
if not check_session():
    # Show authentication pages
    show_auth_pages()
    st.stop()
else:
    # User is authenticated, show main app
    st.sidebar.title('Navigation')

    page = st.sidebar.radio("Page", list(Tabs.keys()))
    st.sidebar.info('Made with ❤️ by Gayatri Kasar')

    df, X, y = load_data()

    if page in ["Diagnosis"]:
        Tabs[page].app(df, X, y)
    else:
        Tabs[page].app()

