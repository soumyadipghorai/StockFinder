import streamlit as st 
import logging
import os
import json
from _temp.config import PAGE_CONFIG
st.set_page_config(**PAGE_CONFIG)  
from utils.db_ops import FireBaseActions
from tqdm import tqdm
from dotenv import main
from components.footer import footer
import time
from utils.download_historical_data import download_file
from utils.update_database import SMEStockFinder
_ = main.load_dotenv(main.find_dotenv())

db_url, cred_path = os.getenv("DB_URL"), os.getenv("CRED_PATH") 
collection_name = os.getenv("ALL_COMPANY_COLLECTION_NAME")
current_trend_collection_name = os.getenv("CURRENT_TREND_COLLECTION_NAME")
current_trend_info_collection_name = os.getenv("CURRENT_TREND_INFO_COLLECTION_NAME")

cred_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),  # convert \n back to real newlines
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}


os.makedirs("data", exist_ok=True)
# ================================
# pull data from firebase 
# ================================ 
fb_obj = FireBaseActions(db_url = db_url, cred_path = cred_dict)
fb_obj._push(collection_name = current_trend_info_collection_name, data_path='data/current_trend_info.json')
if not os.path.exists('data/all_company.json'):
    fb_obj._pull(
        collection_name = collection_name, 
        store_path= 'data/all_company.json'
    )

if not os.path.exists('data/current_trend.json'): 
    fb_obj._pull(
        collection_name = current_trend_collection_name, 
        store_path='data/current_trend.json'
    )

if not os.path.exists('data/current_trend_info.json'): 
    fb_obj._pull(
        collection_name = current_trend_info_collection_name, 
        store_path='data/current_trend_info.json'
    )

if 'company_name' not in st.session_state : 
    if not os.path.exists('data/current_company.json'):
        st.session_state.company_name = None 
    else :
        with open("data/current_company.json", "r") as json_file:
            current_company = json.load(json_file)   
            st.session_state.company_name = current_company['name']

with open("data/current_trend_info.json", "r") as json_file:
    jf = json.load(json_file)
# st.write(jf)
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
# top_picks_page = st.Page("pages/top_picks.py", title = "Top Picks", icon = ":material/local_fire_department:")

pg = st.navigation([
    select_stock_page, 
    # top_picks_page, 
    screener_ratios_page, shareholding_pattern_page, cash_flow_page, 
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

# if download_btn :
#     obj = SMEStockFinder()
#     obj.generate_trend_reversal()
    # download_file(start_from = 'ZENSARTECH')
st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__" : 
    pg.run()