from utils.download_historical_data import download_file
from models.database import  get_db, Base
from models.db_ops import DBOps, StockTrendTable
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, MetaData, Table 
import os
from _temp.config import COLUMN_MAPPING
import pandas as pd 
import logging
import streamlit as st 

class SMEStockFinder(DBOps) : 
    def __init__(self, window_size: int = 20) :
        super().__init__() 
        self.dump = './dump'
        self.window_size = window_size
        
    def __get_all_files(self) : 
        csv_files = [f for f in os.listdir(self.dump) if f.endswith('.csv')]
        return csv_files 
    
    def __find_trend_reversal(self, df: pd.DataFrame, time_frame: int = 3) : 
        curr, trend, i, flag = df['EMA_50'].iloc[0], [], 1, False
        while i < len(df) : 
            if df['EMA_50'].iloc[0] > curr : 
                flag = False 
            elif df['EMA_50'].iloc[0] < curr : 
                flag = True 

            i += 1
            trend.append(flag)

        for i in range(len(trend)) :
            if all(trend[i:i+time_frame]) : 
                return True 
        return False 


    def __find_trend(self, df: pd.DataFrame, window_size: int = 20) : 
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        df['close'] = df['close'].astype(str)
        df['close'] = df['close'].str.replace(",", "").astype(float)
        df['close'] = df['close'].fillna(0)
        try :
            df["EMA_50"] = df["close"].ewm(span=50, adjust=False).mean()
            df["EMA_100"] = df["close"].ewm(span=100, adjust=False).mean()

            df['diff'] = df["EMA_50"] - df["EMA_100"]
            window_df = df.tail(window_size) 
            trend_reversal = self.__find_trend_reversal(window_df)
            # trend_reversal = None
            if window_df['diff'].iloc[-1] > 0 : 
                if window_df['diff'].iloc[0] <= 0 : 
                    return "Up", trend_reversal
                else : 
                    return "Upwards", trend_reversal
            elif window_df['diff'].iloc[-1] <= 0  : 
                if window_df['diff'].iloc[0] > 0 : 
                    return "Down", trend_reversal
                else : 
                    return "Downwards", trend_reversal
            
            return False, trend_reversal
        
        except Exception as e: 
            df["EMA_50"] = df["close"].ewm(span=50, adjust=True).mean()
            st.dataframe(df)
            logging.info(e)
            return False 
        
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