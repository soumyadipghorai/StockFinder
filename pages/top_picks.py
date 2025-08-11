import streamlit as st
from models.database import get_db
from models.db_ops import StockTrendTable
import json
from scrapper import TableExtractor
import os 
import logging
import pandas as pd 
import time 

with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)   

with open("data/current_trend.json", "r") as json_file:
    current_trend = json.load(json_file)   


def return_company_KPI(company_code, performance_metric: str = 'company_info') : 
    df = pd.read_csv(f'data/{company_code}/{performance_metric}.csv') 

    try : market_cap = float(df[df['name'] == 'Market Cap']['value'].iloc[0].replace('Cr.', '').replace(',', '')) 
    except : market_cap = None
    try  : curr_price = float(df[df['name'] == 'Current Price']['value'].iloc[0].replace(',', '')) 
    except : curr_price = None
    try : PE = float(df[df['name'] == 'Stock P/E']['value'].iloc[0]) 
    except: PE = None
    try : book_value = float(df[df['name'] == 'Book Value']['value'].iloc[0].replace(',', '')) 
    except: book_value = None
    try : ROCE = float(df[df['name'] == 'ROCE']['value'].iloc[0].replace('%', '')) 
    except : ROCE = None
    try : ROE = float(df[df['name'] == 'ROE']['value'].iloc[0].replace('%', '')) 
    except : ROE = None
    try : face_value = float(df[df['name'] == 'Face Value']['value'].iloc[0].replace(',', '')) 
    except : face_value = None

    return {
        "market_cap" : market_cap, "current_price": curr_price, "PE" : PE, 
        "book_value" : book_value, "face_value" : face_value, "ROCE" : ROCE, "ROE" : ROE, 
        "change_counter" : current_trend[company_code]["change_counter"], 
        "last_detected_change" : current_trend[company_code]["last_detected_change"]
    }

def extract_all_info(stock_trend, trend_type: str = 'up') : 
    total, counter, mapper = len(stock_trend), 1, {}
    progress_bar = st.progress(0, text=f"Gathering stocks that are going {trend_type}...")
    for stock in stock_trend : 
        progress_bar.progress(int((counter/total)*100), text=f"Gathering stocks that are going {trend_type}...") 
        if stock in all_company :  
            dir_path = f"data/{stock}"
            csv_path = os.path.join(dir_path, "company_info.csv")
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if not os.path.isfile(csv_path):
                obj = TableExtractor(all_company[stock]["url"], parent_directory=f'data/{stock}')
                if obj._extract_primary_table(obj._ceate_soup()) :
                    time.sleep(5) 
                else : 
                    logging.info(f"failed to access {stock}")
            mapper[stock] = return_company_KPI(
                company_code=stock, performance_metric='company_info'
            )
        counter += 1
    progress_bar.empty()
    st.toast(f'Successfully gathered stocks that are going {trend_type}!')
    return mapper 

def view_top_stock_list(company_trend, sort_value: str = "market_cap", trend_type="down") : 
    counter = 1 
    filter_company_with_kpi = [
        (
            tuple(
                upward_mapper[stock][val] if trend_type == "up" \
                else downward_mapper[stock][val] for val in sort_value
            ) + (stock,)
        ) for stock in company_trend
        if stock in all_company 
    ]  
    filter_company_with_kpi = sorted(filter_company_with_kpi, key=lambda x: tuple(x))
    for val in filter_company_with_kpi :  
        company_code = val[-1]
        if company_code in all_company :  
            with st.expander(f'{counter}.{all_company[company_code]["name"]}'):  
                st.write(f'Do you want to check performance of {all_company[company_code]["name"]}?')
                check_btn = st.button('Check', key = company_code) 
                total = len(upward_mapper[company_code].keys()) \
                    if trend_type == 'up' else len(downward_mapper[company_code].keys())
                counter = 1
                sub_col1, sub_col2 = st.columns(2)
                for key, val in (
                    upward_mapper[company_code].items() if trend_type == 'up' 
                    else downward_mapper[company_code].items()
                ) :
                    if counter <= total//2 : 
                        with sub_col2 : 
                            st.write(key, f" : `{val}`")  
                    else : 
                        with sub_col1 : 
                            st.write(key, f" : `{val}`")  
                    counter += 1 
                if check_btn :
                    company_name = f"{all_company[company_code]["name"]} [{company_code}]"
                    st.session_state.company_name = company_name 
                    with open('data/current_company.json', 'w') as f:
                        json.dump({"name" : company_name}, f, indent=4)

                    obj = TableExtractor(all_company[company_code]["url"])
                    if obj.extract_data() : 
                        st.toast('Successfully extracted all the tables...')
            counter += 1
        
upwards = [company for company in current_trend if current_trend[company]["trend"] == "Up"]
downwards = [company for company in current_trend if current_trend[company]["trend"] == "Down"]
upward_mapper = extract_all_info(upwards)
downward_mapper = extract_all_info(downwards, trend_type='down')

# ========================================
#               Page Layout              #
# ========================================
st.title("Top picks for the week")
st.write("Stocks that recently moved into an `upward` or `downward` trend based on 50 and 100 days EMA")

options = ["market_cap", "current_price", "PE", "book_value", "face_value", "ROCE", "ROE", "last_detected_change"]
sort_options = st.pills(
    "Sort companies based on the following : ", options=options, selection_mode="multi",
    default = options[0]
)

col1, _, col2 = st.columns([1, 0.1, 1])
with col1 : 
    st.subheader("Going Up")
    view_top_stock_list(upwards, trend_type = "up", sort_value=sort_options)

with col2 : 
    st.subheader("Going Down")
    view_top_stock_list(downwards, sort_value=sort_options)