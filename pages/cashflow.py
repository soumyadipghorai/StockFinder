import streamlit as st 
import pandas as pd 
from md.cashflow import *
from _temp.config import *

try : df = pd.read_csv('data/cash_flow.csv')
except : df = None

if df is not None : 
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]
    total_operation = sum(df.iloc[0][1:])
    total_investing = sum(df.iloc[1][1:])
    total_finance = sum(df.iloc[2][1:])
    total_debt = total_operation + total_investing

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title('Cash flow')
        st.write("Cash flow statement gives exact cash position of a company")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)
        interest_rate = st.slider(label = 'select interest rate', min_value=4, max_value=50)
        with st.popover(label = f"Read More...", use_container_width= False) : 
            if option == all_options[0] :
                st.markdown(operating_cashflow)
            elif option == all_options[1] :
                st.markdown(investing_cashflow)
            elif option == all_options[2] : 
                st.markdown(financing_cashflow)
            elif option == all_options[3] :
                st.markdown("Total of the above 3 cashflow...")


    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        st.subheader(f'{option} over the years') 
        st.line_chart(df.iloc[row_index][1:])

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1 : st.metric(value=total_debt, label= 'Calculated Debt', delta=f'{round((total_debt - total_finance)/total_finance*100, 2)} %')
    with col2 :
        condition = round((interest_rate * max(total_debt, abs(total_finance))/100), 2) < df.iloc[0][-1] 
        st.metric(value="Yes" if condition else "No", label= 'Sustainable', delta= f"{'+ Can' if condition else "- Can't"} Sustain tax")
    with col3 : st.metric(value=total_operation, label= 'Total Operations') 
    with col4 : st.metric(value=total_investing, label= 'Total investing') 
    with col5 : st.metric(value=total_finance, label= 'Total Finance') 
    with col6 : st.metric(value= round((interest_rate * max(total_debt, total_finance)/100), 2), label= 'Calculated tax', delta = f"{round(((round((interest_rate * total_debt/100), 2) - df.iloc[0][-1])/df.iloc[0][-1]*100), 2)} %") 

else :
    st.title('Cash flow')
    st.write("Cash flow statement gives exact cash position of a company")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")