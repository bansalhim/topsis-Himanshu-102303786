import streamlit as st
import pandas as pd
import os
from topsis import topsis  # Ensure this imports your package correctly

# 1. Configure the page
st.set_page_config(
    page_title="TOPSIS - Himanshu 102303786",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Black Theme & Visible Buttons
st.markdown("""
    <style>
    /* Force entire app background to black */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* Force all text headers and paragraphs to white */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff !important;
    }
    
    /* Fix input field text colors */
    .stTextInput > div > div > input {
        color: #ffffff;
        background-color: #1a1a1a; /* Dark Grey Input Background */
    }

    /* DataFrame styling */
    .stDataFrame {
        border: 1px solid #444;
    }

    /* --- BUTTON STYLING --- */
    
    /* 1. Calculate Button (Red) */
    .stButton > button {
        color: white !important;
        background-color: #FF4B4B !important;
        border: 1px solid #FF4B4B !important;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF2B2B !important;
        border-color: #FF2B2B !important;
    }

    /* 2. Download Button (Green) - Explicitly targeting the download button wrapper */
    .stDownloadButton > button {
        color: white !important;
        background-color: #28a745 !important; /* Green color */
        border: 1px solid #28a745 !important;
        font-weight: bold;
    }
    .stDownloadButton > button:hover {
        background-color: #218838 !important;
        border-color: #1e7e34 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# 3. Main Title
st.title("🚀 TOPSIS - Himanshu 102303786")
st.markdown("---")

# 4. File Uploader Section
st.write("### 1. Upload Data")
uploaded_file = st.file_uploader("Choose an Excel file (.xlsx)", type="xlsx")

if uploaded_file is not None:
    # Save uploaded file to temp file
    temp_input = "temp_input.xlsx"
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read and Display Original Data
    try:
        df = pd.read_excel(temp_input)
        st.write("#### 📄 Original Data Preview")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error reading file: {e}")

    st.markdown("---")

    # 5. Inputs Section
    st.write("### 2. Parameters")
    
    col1, col2 = st.columns(2)
    with col1:
        weights = st.text_input("Enter Weights (comma separated)", placeholder="e.g., 1,1,1,1,1")
        st.caption("Ensure the number of weights matches the number of numeric columns.")
        
    with col2:
        impacts = st.text_input("Enter Impacts (comma separated)", placeholder="e.g., +,+,+,+,+")
        st.caption("Use '+' for beneficial criteria and '-' for non-beneficial.")

    result_filename = "result.csv"

    # 6. Calculate Button
    if st.button("⚡ Calculate TOPSIS Score"):
        if not weights or not impacts:
            st.error("⚠️ Please enter both weights and impacts!")
        else:
            try:
                with st.spinner('Calculating scores...'):
                    # --- CALLING YOUR PACKAGE ---
                    topsis(temp_input, weights, impacts, result_filename)
                
                # Check if result file exists
                if os.path.exists(result_filename):
                    st.success("✅ TOPSIS calculation completed successfully!")
                    
                    # Read the result
                    result_df = pd.read_csv(result_filename)
                    
                    # Display Final Table
                    st.write("#### 🏆 Final Results (Ranked)")
                    st.dataframe(result_df, use_container_width=True)

                    # Highlight the winner (Rank 1)
                    if 'Rank' in result_df.columns:
                        winner = result_df[result_df['Rank'] == 1]
                        if not winner.empty:
                            st.info(f"🥇 Best Alternative: **{winner.iloc[0, 0]}**")

                    # Download Button
                    csv_data = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Result CSV",
                        data=csv_data,
                        file_name="TOPSIS_Himanshu_102303786.csv",
                        mime="text/csv"
                    )

                    # Cleanup temp files
                    os.remove(temp_input)
                    os.remove(result_filename)
                else:
                    st.error("Error: Result file was not generated.")
            
            except Exception as e:
                st.error(f"An error occurred during calculation: {e}")

else:
    st.info("👆 Please upload a file to get started.")