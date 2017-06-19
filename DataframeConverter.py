import pandas as pd

def export_csv(type, current_time, json_result):
    df_result = pd.DataFrame(json_result)

    file_name = current_time  + '_' + type
    with open('./data/' + file_name+'.csv','a') as f:
        df_result.to_csv(f, header=False)