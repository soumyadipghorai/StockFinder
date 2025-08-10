import streamlit as st 
import logging
import os
import json
from _temp.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG) 
# from models.database import get_db, engine, Base
from utils.db_ops import FireBaseActions
from tqdm import tqdm
from dotenv import main
import time
from utils.download_historical_data import download_file
from utils.update_database import SMEStockFinder
_ = main.load_dotenv(main.find_dotenv())

db_url, cred_path = os.getenv("DB_URL"), os.getenv("CRED_PATH") 
collection_name = os.getenv("ALL_COMPANY_COLLECTION_NAME")
current_trend_collection_name = os.getenv("CURRENT_TREND_COLLECTION_NAME")
os.makedirs("data", exist_ok=True)
# ================================
# pull data from firebase 
# ================================ 
fb_obj = FireBaseActions(db_url = db_url, cred_path = cred_path)
if not os.path.exists('data/all_company.json'):
    fb_obj._pull(collection_name = collection_name)

if not os.path.exists('data/current_trend.json'): 
    fb_obj._pull(
        collection_name = current_trend_collection_name, 
        store_path='data/current_trend.json'
    )

# Base.metadata.create_all(bind=engine)
if 'company_name' not in st.session_state : 
    if not os.path.exists('data/current_company.json'):
        st.session_state.company_name = None 
    else :
        with open("data/current_company.json", "r") as json_file:
            current_company = json.load(json_file)   
            st.session_state.company_name = current_company['name']

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
top_picks_page = st.Page("pages/top_picks.py", title = "Top Picks", icon = ":material/local_fire_department:")

pg = st.navigation([
    select_stock_page, top_picks_page, screener_ratios_page, shareholding_pattern_page, cash_flow_page, 
    balance_sheet_page, quarters_page, pnl_page, readme_page
])


st.sidebar.markdown("### Update Data")  
st.sidebar.write("Click to scrape and refresh the latest data for accurate and up-to-date information.")
sb_button = st.sidebar.button('scrape') 
download_btn = st.sidebar.button('Download')

# if sb_button : 
    # from utils.update_database import SMEStockFinder
    # from utils.download_historical_data import download_file
    # from scrapper.scrapper import TableExtractor
#     all_url = {}
#     progress_bar = st.sidebar.progress(0, text="Scrapping Latest Data...")
#     for i in tqdm(range(201,301)) : #201 total number of pages
#         progress_bar.progress(i-200, text="Scrapping Latest Data...")
#         try :
#             url = f"https://www.screener.in/screens/357649/all-listed-companies/?page={i}"
#             obj = TableExtractor(url)
#             res = obj._update_company_list()   
#             all_url.update(res)  
#             logging.info(f"page {i} successful --> {res}")
#         except Exception as e: 
#             st.warning(url)
#             st.error(e)
#             logging.info(f'issue in page num {i} --> {e}')
#         time.sleep(30)

#     with open("data/all_company_201_300.json", "w") as json_file:
#         json.dump(all_url, json_file)
#     progress_bar.empty()

if download_btn :
    obj = SMEStockFinder()
    obj.generate_trend_reversal()
    # download_file(start_from = 'ZENSARTECH')

if __name__ == "__main__" : 
    pg.run()