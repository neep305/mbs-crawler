import pandas as pd
import datetime

def convert_dataframe(type, json_result):
    df_result = pd.DataFrame(json_result)

    sheet_name = datetime.today()

    df_result.toExcel(type+'.csv', sheet_name=sheet_name)