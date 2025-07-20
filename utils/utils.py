import pandas as pd 

def check_if_exist(KPI: str, df: pd.DataFrame) -> bool: 
    for name in df[df.columns[0]] : 
        if KPI in name : return True 
    return False