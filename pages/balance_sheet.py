import streamlit as st 
import pandas as pd 
from _temp.config import *
from md import MAPPER
import numpy as np 
from utils.find_drop import create_quarterly_growth

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
        remaining = st.multiselect(
            label= 'select another feature', 
            options=[rem for rem in all_options if rem != option]
        ) 
        mapper_key = option[:-1].replace('\xa0', '').strip() if option[-1] == '+' else option.replace('\xa0', '').strip()  
        with st.popover(label = f"Read More...", use_container_width= False) : 
            st.markdown(MAPPER[mapper_key] if mapper_key in MAPPER else MAPPER["others"])

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0] 
        remaining_index = [
            df[df[df.columns[0]] == rem].index[0] for rem in remaining
        ]
        st.subheader(f'{option} over the years') 
        st.line_chart(df.iloc[[row_index] + remaining_index].set_index(df.columns[0]).T)

        st.write("Median quarterly performance and latest growth percentage")
        col1, col2 = st.columns(2)

        with col1 : 
            kpi_row_index = df[df[df.columns[0]] == "Total Liabilities"].index[0] 
            raw_diff, perc_diff, q1_df = create_quarterly_growth(df, row_index=kpi_row_index, quarter="Mar")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Growth in Total Liabilities", 
                delta = f"{perc_diff[-1]} %", border= True
            )
        with col2 : 
            kpi_row_index = df[df[df.columns[0]] == "Total Assets"].index[0] 
            raw_diff, perc_diff, q2_df = create_quarterly_growth(df, row_index=kpi_row_index, quarter="Mar")
            st.metric(
                value=round(np.median(raw_diff)), label = f"Growth in Total Assets", 
                delta = f"{perc_diff[-1]} %", border= True
            )

else : 
    st.title("Balance Sheet")
    st.write("View company assets, liabilities, and equity snapshots for clear insights into financial health and stability.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")