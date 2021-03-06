import json
from crawling_dataframe import convert_dataframe

def convert_json(type, result):
    try:

        data = json.loads(result)

        if type == 'range_interest_ch':
            convert_range_interest_ch(data)

        elif type == '':
            print("=========")
        else:
            print('==========')
    except RuntimeError as e:
        print(e)

# Skylife 관심채널 시청가구 변화추이
def convert_range_interest_ch(data):
    temp = []
    for item in data['chList']:
        row = []
        for temprow in item['list']:
            listitem = {}
            listitem['time'] = item['time']
            listitem['prgm_id'] = temprow['prgm_id']
            listitem['ch_no'] = temprow['ch_no']
            listitem['ch_nm'] = temprow['ch_nm']
            listitem['disp_ch_nm'] = temprow['disp_ch_nm']
            listitem['view_cnt'] = temprow['view_cnt']

            temp.append(listitem)
    return temp