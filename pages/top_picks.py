import streamlit as st
import json
from scrapper import TableExtractor
import os 
import logging
import pandas as pd 
import time 
from md import MAPPER

with open("data/all_company.json", "r") as json_file:
    all_company = json.load(json_file)   

with open("data/current_trend.json", "r") as json_file:
    current_trend = json.load(json_file)   

with open("data/current_trend_info.json", "r") as json_file:
    current_trend_info = json.load(json_file)   

MAX_MAPPER = {
    "market_cap" : 0, "current_price": 0, "PE" : 0, 
    "book_value" : 0, "face_value" : 0, "ROCE" : 0, "ROE" : 0, 
    "change_counter" : 0, "last_detected_change" : 0
}
MIN_MAPPER = {
    "market_cap" : float('inf'), "current_price": float('inf'), "PE" : float('inf'), 
    "book_value" : float('inf'), "face_value" : float('inf'), "ROCE" : float('inf'), "ROE" : float('inf'), 
    "change_counter" : float('inf'), "last_detected_change" : float('inf')
}

def return_company_KPI(company_code) :  
    for val in current_trend_info[company_code] : 
        if val["name"] == "Market Cap" : 
            try : market_cap = val["value"]
            except : market_cap = None
        if val["name"] == "Current Price" :
            try : curr_price = val["value"]
            except : curr_price = None
        # if val["name"] == "High / Low" : 
        #     high_low = val["value"]
        if val["name"] == "Stock P/E" : 
            try : PE = val["value"]
            except : PE = None
        if val["name"] == "Book Value" : 
            try : book_value = val["value"]
            except : book_value = None
        # if val["name"] == "Dividend Yield" : 
        #     devidend_yield = val["value"]
        if val["name"] == "ROCE" : 
            try : ROCE = val["value"]
            except : ROCE = None
        if val["name"] == "ROE" : 
            try : ROE = val["value"]
            except : ROE = None
        if val["name"] == "Face Value" : 
            try : face_value = val["value"]
            except : face_value = None

    try : 
        market_cap = float(market_cap.replace('Cr.', '').replace(',', '')) 
        MAX_MAPPER['market_cap'] = max(MAX_MAPPER['market_cap'], market_cap)
        MIN_MAPPER['market_cap'] = min(MIN_MAPPER['market_cap'], market_cap)
    except : 
        market_cap = None
    try  : 
        curr_price = float(curr_price.replace(',', '')) 
        MAX_MAPPER['current_price'] = max(MAX_MAPPER['current_price'], curr_price)
        MIN_MAPPER['current_price'] = min(MIN_MAPPER['current_price'], curr_price)
    except : 
        curr_price = None
    try : 
        PE = float(PE) 
        MAX_MAPPER['PE'] = max(MAX_MAPPER['PE'], PE)
        MIN_MAPPER['PE'] = min(MIN_MAPPER['PE'], PE)
    except: 
        PE = None
    try : 
        book_value = float(book_value.replace(',', '')) 
        MAX_MAPPER['book_value'] = max(MAX_MAPPER['book_value'], book_value)
        MIN_MAPPER['book_value'] = min(MIN_MAPPER['book_value'], book_value)
    except: 
        book_value = None
    try : 
        ROCE = float(ROCE.replace('%', '')) 
        MAX_MAPPER['ROCE'] = max(MAX_MAPPER['ROCE'], ROCE)
        MIN_MAPPER['ROCE'] = min(MIN_MAPPER['ROCE'], ROCE)
    except : 
        ROCE = None
    try : 
        ROE = float(ROE.replace('%', '')) 
        MAX_MAPPER['ROE'] = max(MAX_MAPPER['ROE'], ROE)
        MIN_MAPPER['ROE'] = min(MIN_MAPPER['ROE'], ROE)
    except : 
        ROE = None
    try : 
        face_value = float(face_value.replace(',', '')) 
        MAX_MAPPER['face_value'] = max(MAX_MAPPER['face_value'], face_value)
        MIN_MAPPER['face_value'] = min(MIN_MAPPER['face_value'], face_value)
    except : 
        face_value = None

    MAX_MAPPER['last_detected_change'] = max(MAX_MAPPER['last_detected_change'], current_trend[company_code]["last_detected_change"])
    MIN_MAPPER['last_detected_change'] = min(MIN_MAPPER['last_detected_change'], current_trend[company_code]["last_detected_change"])
    
    MAX_MAPPER['change_counter'] = max(MAX_MAPPER['change_counter'], current_trend[company_code]["change_counter"])
    MIN_MAPPER['change_counter'] = min(MIN_MAPPER['change_counter'], current_trend[company_code]["change_counter"])


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
            mapper[stock] = return_company_KPI(company_code=stock)
        counter += 1
    progress_bar.empty()
    st.toast(f'Successfully gathered stocks that are going {trend_type}!', icon=":material/check_circle:")
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
    def remove_null(filter_company_with_kpi) : 
        return [
            val for val in filter_company_with_kpi if all([v is not None for v in val])
        ]
    filter_company_with_kpi = sorted(remove_null(filter_company_with_kpi), key=lambda x: tuple(x))
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

def filter_with_feature_map(trend_type, fetaure_map, trend = "Up") : 
    filtered_trend = []
    if trend == 'up' : mapper = upward_mapper
    else : mapper = downward_mapper
    for company in trend_type :
        if company in mapper :
            flag = True 
            for feature in feature_map : 
                if mapper[company][feature] : 
                    if (feature_map[feature][0] > mapper[company][feature]) \
                        or (mapper[company][feature] > feature_map[feature][1]) : 
                        flag = False
                        break 
            if flag :
                filtered_trend.append(company)
    return filtered_trend

# ========================================
#               Page Layout              #
# ========================================
st.title("Top picks for the week")
st.write("Stocks that recently moved into an `upward` or `downward` trend based on 50 and 100 days EMA")

options = ["market_cap", "current_price", "PE", "book_value", "ROCE", "ROE", "last_detected_change"]
input_col1, input_col2 = st.columns(2)


with input_col1 :
    sort_options = st.pills(
        "Sort companies based on the following : ", options=options, selection_mode="multi",
        default = options[0]
    )

    selected_columns = st.multiselect(label="Select features", options= options)
    with st.popover(label = f"Details", use_container_width= False, ) : 
        st.markdown(MAPPER["quick_summary"])

feature_map = {}
with input_col2 :
    if selected_columns :
        st.write('Adjust additional filters here : ')
        with st.expander('Additional Filters') : 
            for feature in selected_columns : 
                if feature != 'total_tax' :
                    min_val, max_val = MIN_MAPPER[feature], MAX_MAPPER[feature]
                    selected_range = st.slider(
                        f"Filter for {feature}", min_value= min_val, max_value= max_val, 
                        value = (min_val, max_val)
                    )
                    feature_map[feature] = selected_range

filtered_upwards = filter_with_feature_map(upwards, feature_map, trend='up')
filtered_downwards = filter_with_feature_map(downwards, feature_map, trend='down')

col1, _, col2 = st.columns([1, 0.1, 1]) 
with col1 : 
    st.subheader("Going Up")
    view_top_stock_list(filtered_upwards, trend_type = "up", sort_value=sort_options)

with col2 : 
    st.subheader("Going Down")
    view_top_stock_list(filtered_downwards, sort_value=sort_options)