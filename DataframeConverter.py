import pandas as pd
from datetime import datetime

def export_csv(type, json_result):
    df_result = pd.DataFrame(json_result)

    date = datetime.today()

    strToday = date.strftime('%Y%m%d%H%M%S')

    df_result.to_csv(type+ '_' + strToday + '.csv')