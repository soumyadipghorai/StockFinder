import requests 
from bs4 import BeautifulSoup
import pandas as pd
import random
import logging 
from tqdm import tqdm
import streamlit as st  
import json 

class TableExtractor : 
    def __init__(self, url: str, save_files: bool = True, debug: bool = False) -> None : 
        self.url = url
        self.save_files = save_files  
        self.debug = debug

    def __ceate_soup(self, url: str = None) :
        site_url = self.url if not url else url 
        headers = {
            'authority': 'scrapeme.live', 'dnt': '1', 'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none', 'sec-fetch-mode': 'navigate', 
            'sec-fetch-user': '?1', 'sec-fetch-dest': 'document', 
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

        site_page = requests.get(site_url, headers = headers)
        site_page_htmlcontent = site_page.content
        site_page_soup = BeautifulSoup(site_page_htmlcontent, 'html.parser')

        return site_page_soup
    
    def __extract_ratios(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'ratios'})
            ratio_table = str(ratio_section.find('table')) 
            ratio_df = pd.read_html(ratio_table)[0]
            ratio_df.iloc[-1, 1:] = ratio_df.iloc[-1, 1:].replace({'%': ''}, regex=True).apply(pd.to_numeric)
            ratio_df.iloc[:, 1:] = ratio_df.iloc[:, 1:].apply(pd.to_numeric)

            # ratio_df.set_index(ratio_df.columns[0], inplace=True)
            if self.save_files : 
                ratio_df.to_csv('data/ratio_table.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False 
    
    def __extract_shareholding_pattern(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'shareholding'})
            ratio_table = str(ratio_section.find('table'))
            ratio_df = pd.read_html(ratio_table)[0] 
            ratio_df.iloc[:, 1:] = ratio_df.iloc[:, 1:].replace({'%': ''}, regex=True).apply(pd.to_numeric)
            if self.save_files : 
                ratio_df.to_csv('data/shareholding_pattern.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False
        
    def __extract_cash_flow(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'cash-flow'})
            ratio_table = str(ratio_section.find('table'))
            ratio_df = pd.read_html(ratio_table)[0] 
            if self.save_files : 
                ratio_df.to_csv('data/cash_flow.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False
        
    def __extract_balance_sheet(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'balance-sheet'})
            ratio_table = str(ratio_section.find('table'))
            ratio_df = pd.read_html(ratio_table)[0] 
            ratio_df.iloc[:, 1:] = ratio_df.iloc[:, 1:].replace({'%': ''}, regex=True).apply(pd.to_numeric)
            if self.save_files : 
                ratio_df.to_csv('data/balance_sheet.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False
        
    def __extract_quarters(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'quarters'})
            ratio_table = str(ratio_section.find('table'))
            ratio_df = pd.read_html(ratio_table)[0] 
            ratio_df.iloc[:, 1:] = ratio_df.iloc[:, 1:].replace({'%': ''}, regex=True).apply(pd.to_numeric)
            if self.save_files : 
                ratio_df.to_csv('data/quarters.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False
        
    def __extract_pnl(self, soup: str) : 
        try :
            ratio_section = soup.find('section', {'id' : 'profit-loss'})
            ratio_table = str(ratio_section.find('table'))
            ratio_df = pd.read_html(ratio_table)[0] 
            ratio_df.iloc[:, 1:] = ratio_df.iloc[:, 1:].replace({'%': ''}, regex=True).apply(pd.to_numeric)
            if self.save_files : 
                ratio_df.to_csv('data/profit_loss.csv', index = False, encoding = 'utf-8')
            return True 
        except : 
            return False
        
    def _update_company_list(self) : 
        site_page_soup = self.__ceate_soup() 
        company_table = site_page_soup.find('table', {'class' : 'data-table'}) 
        all_row = company_table.find_all('tr')
        all_url = {}
        try :
            all_row = all_row[1:]
            for row in all_row : 
                try :
                    company_name = row.find_all('td')[1]
                    company_url = "https://www.screener.in"+company_name.find('a')['href'] 
                    company_soup = self.__ceate_soup(company_url)
                    try :
                        company_links = company_soup.find('div', {'class' : 'company-links show-from-tablet-landscape'})
                        for link in company_links.find_all('span', {'class' : 'ink-700 upper'}) : 
                            if link.text.strip()[:3] == 'NSE' :   
                                all_url[link.text.split(':')[1].strip()] = {
                                    "url" : company_url, "name" : company_name.text.strip()
                                } 
                                break
                    except :
                        logging.info(f"couldn't get the NSE code for {company_name.text.strip()} --> {company_links.find_all('span', {'class' : 'ink-700 upper'})}")
                except : 
                    logging.info(f'can not extract table data --> {row}')
        except Exception as e:
            st.error(e) 
            logging.info(f'can not extract table row --> {all_row}')

        return all_url 
        
    def extract_data(self) :
        site_page_soup = self.__ceate_soup()
        try :
            ratio_passed = self.__extract_ratios(site_page_soup)
            shareholding_passed = self.__extract_shareholding_pattern(site_page_soup)
            cashflow_passed = self.__extract_cash_flow(site_page_soup)
            balance_sheet_passed = self.__extract_balance_sheet(site_page_soup)
            quarters_passed = self.__extract_quarters(site_page_soup)
            pnl_passed = self.__extract_pnl(site_page_soup)
            return ratio_passed and shareholding_passed and cashflow_passed and pnl_passed and balance_sheet_passed and quarters_passed
        except : 
            return False 