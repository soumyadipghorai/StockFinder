import streamlit as st
from models.database import get_db
from models.db_ops import StockTrendTable
import json

st.title("Top picks for the week")
st.write("Stocks that recently moved into an `upward` or `downward` trend based on 50 and 100 days EMA")

with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)   

db = get_db()
upwards = db.query(StockTrendTable).filter(StockTrendTable.trend == "Up").all()
downwards = db.query(StockTrendTable).filter(StockTrendTable.trend == "Down").all()

col1, _, col2 = st.columns([1, 0.1, 1])
with col1 : 
    st.subheader("Going Up")
    for stock in upwards :   
        st.success(all_company[stock.company_code]["name"])

with col2 : 
    st.subheader("Going Down")
    for stock in downwards : 
        st.error(all_company[stock.company_code]["name"])