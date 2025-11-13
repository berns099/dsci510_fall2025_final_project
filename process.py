from load import *
import pandas as pd

def process_accident_data(url_input:str)-> pd.DataFrame:
    accident_df = get_accident_table_data(url_input, table_index=0)
    if accident_df is not NONE: