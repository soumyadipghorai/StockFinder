from utils.download_historical_data import download_file
from models.database import  get_db, Base
from models.db_ops import DBOps, StockTrendTable
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, MetaData, Table 
import os
from _temp.config import COLUMN_MAPPING
import pandas as pd 
import logging
import streamlit as st 
import json
from tqdm import tqdm

class SMEStockFinder : 
    def __init__(self, window_size: int = 30, dump_file_path: str = './dump', store_file_path: str = './data') : 
        self.dump = dump_file_path
        self.store = store_file_path
        self.window_size = window_size
        
    def __get_all_files(self) : 
        csv_files = [f for f in os.listdir(self.dump) if f.endswith('.csv')]
        return csv_files 
    
    def __find_trend_reversal(self, df: pd.DataFrame) : 
        change_arr, change_counter, last_change_detected = [], 0, 0 
        for i in range(1, len(df)) : 
            change_arr.append(True if df['diff'].iloc[i] > 0 else False)

        curr = change_arr[0]
        for i in range(1, len(change_arr)) : 
            if change_arr[i] != curr : 
                change_counter += 1 
                curr, last_change_detected = change_arr[i], i 

        return change_counter, len(df)-last_change_detected

    def __find_trend(self, df: pd.DataFrame, window_size: int = 30, long_ma: int = 100, short_ma: int = 50) : 
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df['close'] = df['close'].astype(str)
        df['close'] = df['close'].str.replace(",", "").astype(float)
        df['close'] = df['close'].fillna(0)
        try :
            df["EMA_short"] = df["close"].ewm(span=short_ma, adjust=False).mean()
            df["EMA_long"] = df["close"].ewm(span=long_ma, adjust=False).mean()

            df['diff'] = df["EMA_short"] - df["EMA_long"]
            window_df = df.tail(window_size) 
            change_counter, last_detected_change = self.__find_trend_reversal(window_df)

            if change_counter == 0 : 
                if window_df['diff'].iloc[-1] > 0 :
                    return 'Cont-Up', change_counter, last_detected_change
                else :
                    return 'Cont-Down', change_counter, last_detected_change
            else : 
                if window_df['diff'].iloc[-1] > 0 :  
                    return 'Up', change_counter, last_detected_change
                else : 
                    return 'Down', change_counter, last_detected_change
        
        except Exception as e: 
            df["EMA_short"] = df["close"].ewm(span=short_ma, adjust=True).mean()
            st.dataframe(df)
            logging.info(e)
            return False 
        
    def generate_trend_reversal(self) :  
        all_files, mapper = self.__get_all_files(), {}
        for i in range(len(all_files)) : 
            try :
                df = pd.read_csv('dump/'+all_files[i])
                table_name = df['Symbol  '].iloc[0]
                df = df[list(COLUMN_MAPPING.keys())].rename(columns=COLUMN_MAPPING)
                trend, change_counter, last_detected_change = self.__find_trend(df.copy(), window_size= self.window_size)

                print(table_name, trend, change_counter, last_detected_change, i)
                if change_counter != 0 :
                    mapper[table_name] = {
                        "change_counter" : change_counter, "last_detected_change" : last_detected_change,
                        "trend" : trend
                    } 
            except : 
                pass  
        
        with open('data/current_trend.json', 'w') as f:
            json.dump(mapper, f, indent=4)
        
    def update(self) : 
        all_files = self.__get_all_files()
        for file_path in all_files : 
            try :
                df = pd.read_csv('dump/'+file_path)
                table_name = df['Symbol  '].iloc[0]
                df = df[list(COLUMN_MAPPING.keys())].rename(columns=COLUMN_MAPPING)
                trend, trend_reversal = self.__find_trend(df.copy(), window_size= self.window_size)
                company_details = self.db.query(StockTrendTable).filter(StockTrendTable.company_code == table_name).first()

                if company_details : 
                    company_details.trend, company_details.reverse_started = trend, trend_reversal
                else : 
                    new_entry = StockTrendTable( 
                        company_code = table_name, trend = trend, reverse_started = trend_reversal
                    ) 
                    self.db.add(new_entry)
            
                self.db.commit()

                df = df[COLUMN_MAPPING.values()]
                _ = self.check_and_create_table(table_name=table_name) 
                df.to_sql(table_name, con=self.db.get_bind(), if_exists='append', index=False)
            except Exception as e : 
                logging.error(e)