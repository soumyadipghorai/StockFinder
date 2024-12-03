import streamlit as st 
import pandas as pd 
from _temp.config import *
import plotly.express as px 
from md.shareholder import *

try : df = pd.read_csv('data/shareholding_pattern.csv')
except : df = None 

if df is not None :
    all_options = [df[df.columns[0]].iloc[i] for i in range(len(df))]

    col1, _, col2 = st.columns([1, 0.1, 2])
    with col1 :
        st.title("Company Shareholding Pattern")
        st.write("Overview of share distribution among Promoters, FIIs, DIIs, and Public stakeholders.")
        st.write(COMPANY_DATAILS.format(company_name = st.session_state.company_name))
        option = st.selectbox(label= 'select feature', options= all_options)
        with st.popover(label = f"Read More...", use_container_width= False) : 
            if option[:3] == "Pro" :
                st.markdown(promoter_md)
            elif option[:3] == "FII" :
                st.markdown(FII_md)
            elif option[:3] == 'DII' : 
                st.markdown(DII_md)
            elif option[:3] == "Pub" :
                st.markdown(public_md)
            elif option[:3] == "Gov" :
                st.markdown(gov_md)
            elif option[:3] == "No." :
                st.markdown(num_sh_md)

    with col2 :
        row_index = df[df[df.columns[0]] == option].index[0]
        fig = px.line(df.iloc[row_index][1:], title='Share holding pattern Over Time')
        fig.update_layout(
            yaxis=dict(
                title='Holding percentage' if option != all_options[-1] else option,  
                range=[0, max(df.iloc[row_index][1:]) * 1.3]  
            ), xaxis=dict(
                title='Period', tickangle=90  
            ), showlegend=False 
        )

        st.plotly_chart(fig)

else : 
    st.title("Company Shareholding Pattern")
    st.write("Overview of share distribution among Promoters, FIIs, DIIs, and Public stakeholders.")
    st.toast(DEFAULT_MSG_FU, icon=":material/info:")