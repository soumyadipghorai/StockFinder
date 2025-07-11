from models.database import  get_db, Base
from sqlalchemy import create_engine, inspect, Column, Integer, String, Float, Boolean, Table, Date
from sqlalchemy.exc import SQLAlchemyError
import logging 

class StockTrendTable(Base):
    __tablename__ = "stock_trend"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    company_code = Column(String, nullable=False)
    trend = Column(String, nullable=False)
    reverse_started = Column(Boolean, nullable= True)


class DBOps :
    def __init__(self) -> None : 
        self.db = get_db()

    def _get_all_db(self) -> set:   
        inspector = inspect(self.db.get_bind())
        table_names = inspector.get_table_names()
        return set(table_names)

    def _create_dynamic_table_class(self, table_name: str = "COMPANY_NAME"):
        return type(
            table_name, (Base,),
            {
                "__tablename__": table_name,
                "id": Column(Integer, primary_key=True, autoincrement=True),
                "date" : Column(Date, nullable= False), 
                "open" : Column(Float, nullable= False),
                "close" : Column(Float, nullable= False),
                "high" : Column(Float, nullable= False),
                "low" : Column(Float, nullable= False), 
                "traded_quantity" : Column(Integer, nullable= False),
                "num_trades" : Column(Integer, nullable= False)
            },
        )

    def check_and_create_table(self, table_name: str = "COMPANY_NAME"):
        try: 
            DynamicTable = self._create_dynamic_table_class(table_name)
            
            inspector = inspect(self.db.get_bind())
            if table_name not in inspector.get_table_names(): 
                Base.metadata.create_all(bind=self.db.get_bind(), tables=[DynamicTable.__table__])
                print(f"Table '{table_name}' created successfully.")
            else:
                print(f"Table '{table_name}' already exists.")

        except SQLAlchemyError as e:
            logging.info(e)
            self.db.rollback()
