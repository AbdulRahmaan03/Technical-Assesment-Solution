# Task 3
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Helper function for metrics display
def display_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-value">{value:,}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Page configuration
st.set_page_config(
    page_title="BGP Routing Analysis",
    page_icon="resources\favicon.jpeg",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #000;
        color: white;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #34495e;
    }
    .stMarkdown h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .stMarkdown h2 {
        color: #ecf0f1;
        font-size: 1.8rem;
        margin: 1.5rem 0;
    }
    .block-container {
        padding: 3rem 2rem;
    }
    .metric-container {
        background-color: #2c3e50;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }
    .metric-label {
        font-size: 1rem;
        color: #bdc3c7;
    }
    .element-container {
        width: 100% !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
    }
    
    .stDataFrame {
        width: 100% !important;
    }
    
    /* Make tabs stretch full width */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        width: 100%;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        white-space: nowrap;
    }
    
    /* Adjust metrics container for better spacing */
    .metrics-row {
        margin: 2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

def set_page(page_name):
    st.session_state.page = page_name

st.sidebar.title("Navigation")
if st.sidebar.button("**Home**"):
    set_page("Home")
if st.sidebar.button("**Exploratory Data Analysis**"):
    set_page("Exploratory Data Analysis")
if st.sidebar.button("**Anomaly Identification**"):
    set_page("Anomaly Identification")
if st.sidebar.button("**Advanced Analysis**"):
    set_page("Advanced Analysis")


# Home Page
if st.session_state.page == "Home":
    st.title("🌐 BGP Routing Analysis Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        display_metric("Total IP Prefixes", 1143496)
    with col2:
        display_metric("Transit IP Prefixes", 372366)
    with col3:
        display_metric("Non-Transit IP Prefixes", 771130)
    
    st.write(
        """
        ### About This Dashboard
        This analytical tool provides comprehensive insights into BGP routing data, focusing on:
        
        - **Network Distribution Analysis**: Understand the distribution of IPv4 vs IPv6 prefixes
        - **Transit vs Non-Transit Analysis**: Analyze routing patterns and dependencies
        - **Anomaly Detection**: Identify potential routing anomalies and patterns
        
        Use the sidebar navigation to explore different aspects of the analysis.
        """
    )

# EDA Page
elif st.session_state.page == "Exploratory Data Analysis":
    st.title("Exploratory Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "Visualizations"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Quick Statistics")
        col2.subheader('Insights')
        with col1:
            st.dataframe(
                data=pd.read_csv('resources/bgp_data_sample.csv'),
                use_container_width=False,
                hide_index=True,
                height=415
            )
            st.subheader("Proportion of IPV4 vs IPV6 Prefixes")
            st.image(r'resources\Count of IPv4 and IPv6 Prefixes.png')
        with col2:
            st.markdown('- A sample of the raw data parsed to **MySQL** Database')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.markdown('- More than **60 \%** of the data belongs to IPV4')
    
    with tab2:
        st.subheader("Hop Analysis")
        hops_table = pd.read_csv(r'resources\bgp_analysis_1.csv')
        st.dataframe(
            hops_table.style.background_gradient(cmap='Blues'),
            use_container_width=True,
            hide_index=True,
            height=1000
        )
        st.subheader('Insights')
        st.markdown('- Few Prefix do not have any associated ASN, indicating that the route has not passed any intermediate ASNs')
        st.markdown('- Majority of the Prefixes have number of hops in the range of **1-4**')
        st.markdown('- A few IP prefixes have very high number of hops, which might be anomalous')
    
    with tab3:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Further Analysis")
        col2.subheader('Insights')
        with col1:
            st.image(r'resources\Proportion of Transit and Non-Transit Prefixes.png')
            st.image(r'resources\Count of Prefix vs Number of Hops.png')
            st.markdown("")
            st.image('resources\Count of IP Prefixes by IP Class.png')

        with col2:
            st.markdown('- Proportion of Non-Transit Prefix compared to Transit Prefix varies a lot')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.markdown('- Majority of the Prefixes have No.of Hops in the range of **0-40**')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n')
            st.markdown('- The classes in IPV4 have varied counts in order of **A->B->C**.')
            st.markdown('- Count of IPV6 prefix doesn \'t even match the lowest class count of IPV4')


# Anomaly Detection Page
elif st.session_state.page == "Anomaly Identification":
    st.title("Anomaly Identification")

    tab1, tab2, tab3 = st.tabs(["Overview", "Detailed Analysis", "Further Analysis"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Quick Statistics")
        col2.subheader('Insights')
        with col1:
            st.dataframe(
                data=pd.read_csv(r'resources\bgp_comparative_analysis.csv'),
                use_container_width=False,
                hide_index=True,
                height=780
            )
        with col2:
            st.markdown('- A sample of the evaluated data by training **Isolation Forest ALgorithm**')
            st.markdown('- **Anomaly_Score** indicates the score of anomality predicted by the model (Close to 0 indicates normal Prefixes and Negative score suggest anomalies)')
            st.markdown('- **Anomaly** indicates if the Prefix has been predicted to be anomalous (1) or not anomalous (-1)')
    
    with tab2:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Anomaly Score Analysis")
        col2.subheader('Insights')
        with col1:
            st.image(r'resources\Anomaly Score vs. Number of Hops for Transit Prefixes.png')
            st.image(r'resources\Anomaly Score vs. Number of Hops for Non-Transit Prefixes.png')
        with col2:
            st.markdown('- Few Aanomalies in both yransit and non-transit have very high number of hops')
            st.markdown('- Both transit and non-transit scatter plots look **95%** similar indicating that the distribution of data across both type of prefixes is approximately the same')
            st.markdown('- The data points overlap due to similarity in anomaly score predicted by the model')
    
    with tab3:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Proportion of Anomalies")
        col2.subheader('Insights')
        with col1:
            st.image(r'resources\Number_of_Anomalies_Detected_in_Transit_vs_Non_Transit_Prefixes.png')
            st.subheader('Feature Importance of No.of Hops')
            st.dataframe(
                data=pd.read_csv('resources\high_hop_anomalies.csv'),
                use_container_width=False,
                hide_index=True,
                height=150
            )

        with col2:
            st.markdown('- The proportion of Anomalies in Transit is **14%** compared to Non-Transit with **38%**')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n');st.write('\n')
            st.markdown('- Extremely high values indicate possible routing anomalies, malicious behaviours, loops or path inflation')

# Advanced Feature Contribution Analysis Page
elif st.session_state.page == "Advanced Analysis":
    st.title("Advanced Feature Contribution Analysis")

    tab1, tab2= st.tabs(["Duplicates in ASN", "MED (Metric)"])
    
    with tab1:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Feature Visualisation")
        col2.subheader('Insights')
        with col1:
            st.image(r"resources\Prefixes_with_Duplicate_ASNs (Transit).png")
            st.image(r"resources\Prefixes_with_Duplicate_ASNs (Non-Transit).png")
        with col2:
            st.markdown('- It can be observed that around 13 \% of the Transit Prefix and 18 \% of the Non-Transit Prefix have duplicate ASNs in their paths, and its effect on identifying the anomalies can be subject to domain knowledge as these duplicates might be added by the hosts on purpose to influence the transmition of data by other networks or they can be a feature to identify anomalies.')
            
    
    with tab2:
        col1, col2 = st.columns([3, 1])
        col1.subheader("Feature Visualisation")
        col2.subheader('Insights')
        with col1:
            st.image(r"resources\Distribution of Metric Values (Transit).png")
            st.image(r"resources\Distribution of Metric Values (Non-Transit).png")
        with col2:
            st.markdown('- The distribution of Metric Values for Transit Prefixes varies a lot with a good amount having unexpectedly high value.')
            st.markdown('- In the case of Non-Transit, the metric values are mostly 0 with a few having high value.')
            st.markdown('- The red dashed line indicates the calculated threshold based on mean and standard deviation')
