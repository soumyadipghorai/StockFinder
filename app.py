import streamlit as st 
import logging
import os
import json
from _temp.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG) 

if 'company_name' not in st.session_state : 
    st.session_state.company_name = None

log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, 'app.log')
logging.basicConfig(
    filename = log_file, filemode = 'a', 
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

select_stock_page = st.Page("pages/enter_stock.py", title = "Select Stock", icon = ":material/check_circle:")
readme_page = st.Page("pages/readme.py", title = "README", icon = ":material/analytics:")
screener_ratios_page = st.Page("pages/screener_ratios.py", title = "Screener Ratios", icon = ":material/data_exploration:")
shareholding_pattern_page = st.Page("pages/shareholding.py", title = "shareholding pattern", icon = ":material/folder_shared:")
cash_flow_page = st.Page("pages/cashflow.py", title = "Cash flow", icon = ":material/payments:") 
balance_sheet_page = st.Page("pages/balance_sheet.py", title = "balance Sheet", icon = ":material/account_balance:")
quarters_page = st.Page("pages/quarters.py", title = "Quarterly results", icon = ":material/trending_up:")
pnl_page = st.Page("pages/pnl.py", title = "Profit & Loss", icon = ":material/currency_exchange:")

pg = st.navigation([
    select_stock_page, screener_ratios_page, shareholding_pattern_page, cash_flow_page, 
    balance_sheet_page, quarters_page, pnl_page, readme_page
])

# st.sidebar.markdown("### Update Data")  
# st.sidebar.write("Click to scrape and refresh the latest data for accurate and up-to-date information.")
# sb_button = st.sidebar.button('scrape') 

# if sb_button : 
#     all_url = {}
#     for i in range(1,193) :
#         try :
#             url = f"https://www.screener.in/screens/357649/all-listed-companies/?page={i}"
#             obj = TableExtractor(url)
#             res = obj._update_company_list()  
#             all_url.update(res) 
#             st.success("Dataset updated") 
#         except : 
#             logging.info(f'issue in page num {i}')


#     with open("data/all_company.json", "w") as json_file:
#         json.dump(all_url, json_file)

if __name__ == "__main__" : 
    pg.run()