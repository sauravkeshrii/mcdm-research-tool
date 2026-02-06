
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from mcdm_calculator.service import calculate_mcdm

st.set_page_config(
    page_title="MCDM Research Tool",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Multi-Criteria Decision Making (MCDM) Research Tool")
st.markdown("A research-ready tool for comprehensive decision analysis.")

# --- Helper Functions ---
@st.cache_data
def load_data(file):
    """Load data from CSV or Excel file."""
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file, index_col=0)
        elif file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file, index_col=0, engine='openpyxl')
        else:
            return None
    except Exception as e:
        return str(e)

@st.cache_data
def convert_df(df):
    """Convert dataframe to CSV for download."""
    return df.to_csv(index=False).encode('utf-8')

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Configuration")

# Weights Method
weights_method = st.sidebar.selectbox(
    "Weighting Method",
    options=['merec', 'entropy', 'critic', 'equal', 'manual'],
    index=0,
    help="Select the method to calculate criteria weights."
)

manual_weights_str = ""
if weights_method == 'manual':
    manual_weights_str = st.sidebar.text_input(
        "Enter Weights (comma separated)",
        placeholder="0.2, 0.3, 0.5"
    )

# Ranking Method
ranking_method = st.sidebar.selectbox(
    "Ranking Method",
    options=['topsis', 'vikor', 'mairca'],
    index=0,
    help="Select the method to rank alternatives."
)

st.sidebar.info(f"**Selected Logic:**\n\nWeights: `{weights_method.upper()}`\nRanking: `{ranking_method.upper()}`")

# --- Main Area: Data Input ---
st.header("Input Data")
st.info("Upload a CSV/Excel file or edit the table below. First column must be Alternative Names.")

# File Uploader
uploaded_file = st.file_uploader("Upload Data File", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    loaded_data = load_data(uploaded_file)
    if isinstance(loaded_data, str): # Error message
        st.error(f"Error reading file: {loaded_data}")
        st.stop()
    elif loaded_data is None:
        st.error("Unsupported file format.")
        st.stop()
    else:
        df = loaded_data
else:
    # Default example data
    data = {
        'Price': [250, 200, 300, 275],
        'Storage': [16, 16, 32, 32],
        'Camera': [12, 8, 16, 8],
        'Looks': [5, 3, 4, 2]
    }
    df = pd.DataFrame(data, index=['Phone A', 'Phone B', 'Phone C', 'Phone D'])

# Interactive Data Editor
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Decision Matrix")
    edited_df = st.data_editor(df, num_rows="dynamic")

with col2:
    st.subheader("Criteria Types")
    st.caption("Select optimization direction for each criterion.")
    
    criteria_types = []
    cols = edited_df.columns
    
    for col in cols:
        c_type = st.radio(
            f"**{col}**",
            options=[1, -1],
            format_func=lambda x: "Benefit (Maximize)" if x == 1 else "Cost (Minimize)",
            key=f"type_{col}",
            horizontal=True
        )
        criteria_types.append(c_type)

# --- Calculation Trigger ---
st.divider()
if st.button("🚀 Calculate Results", type="primary"):
    
    # Manual Weights Parsing
    manual_weights = None
    if weights_method == 'manual':
        try:
            manual_weights = [float(x.strip()) for x in manual_weights_str.split(',')]
            if len(manual_weights) != len(edited_df.columns):
                st.error(f"Number of weights ({len(manual_weights)}) does not match number of criteria ({len(edited_df.columns)})")
                st.stop()
        except ValueError:
            st.error("Invalid format for manual weights. Use comma-separated numbers.")
            st.stop()

    try:
        # Call Backend Service
        results = calculate_mcdm(
            edited_df, 
            weights_method, 
            ranking_method, 
            criteria_types, 
            manual_weights
        )
        
        # --- Display Results ---
        st.header("Results Analysis")
        
        # Rankings Table
        st.subheader("🏆 Final Ranking")
        st.dataframe(
            results['results'].style.background_gradient(cmap='Blues', subset=[results['results'].columns[1]]),
            use_container_width=True
        )
        
        # Weights Table
        st.subheader("⚖️ Calculated Weights")
        
        # Create a visually appealing weights chart
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            st.dataframe(results['weights'], use_container_width=True)
            
        with col_w2:
            st.bar_chart(results['weights'].set_index('Criterion'))
            
        # Download Button
        csv_data = convert_df(results['results'])
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv_data,
            file_name=f'results_{weights_method}_{ranking_method}.csv',
            mime='text/csv',
        )
        
        st.success("Analysis Complete! ✅")
        
    except Exception as e:
        st.error(f"Calculation Error: {e}")

# Run instructions
st.sidebar.divider()
st.sidebar.markdown("""
**How to use:**
1. Upload data or edit example.
2. Set criteria types (Benefit/Cost).
3. Choose methods.
4. Click Calculate!
""")
st.sidebar.divider()
st.sidebar.markdown("Maintainer: [sauravkeshrii](https://github.com/sauravkeshrii)")
st.sidebar.caption("#Research #Opensource")
st.sidebar.caption("v1.0.0 | ॐ")
