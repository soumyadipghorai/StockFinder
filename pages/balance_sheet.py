import streamlit as st 
import pandas as pd 
from _temp.config import *
from md import MAPPER

try : df = pd.read_csv('data/balance_sheet.csv')
except :  df = None

if not df is None :
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Balance Sheet")
        st.write("View company assets, liabilities, and equity snapshots for clear insights into financial health and stability.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)
        mapper_key = option[:-1].replace('\xa0', '').strip() if option[-1] == '+' else option.replace('\xa0', '').strip()  
        with st.popover(label = f"Read More...", use_container_width= False) : 
            st.markdown(MAPPER[mapper_key] if mapper_key in MAPPER else MAPPER["others"])

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        st.subheader(f'{option} over the years')
        st.line_chart(df.iloc[row_index][1:])
else : 
    st.title("Balance Sheet")
    st.write("View company assets, liabilities, and equity snapshots for clear insights into financial health and stability.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")