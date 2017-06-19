import json
import DataframeConverter as dc
import Const

def convert_json(type, result, strToday):
    try:

        data = json.loads(result)

        if type == 'range_interest_ch':
            convert_df_to_csv(type, data, strToday)
        elif type == 'range_compare_ch':
            convert_df_to_csv(type, data, strToday)
        else:
            print('Not Available Yet')
    except RuntimeError as re:
        print(re)

# Skylife 관심채널 시청가구 변화추이
def convert_df_to_csv(type, data, current_time):
    temp = []
    temp_tot = []

    type_value = 'I'

    if type == Const.RANGE_COMPARE_CH:
        type_value = 'Y'

    for item in data['chList']:
        for temprow in item['list']:
            list_item = {}
            list_item['time'] = item['time']
            list_item['prgm_id'] = temprow['prgm_id']
            list_item['ch_no'] = temprow['ch_no']
            list_item['ch_nm'] = temprow['ch_nm']
            list_item['disp_ch_nm'] = temprow['disp_ch_nm']
            list_item['view_cnt'] = temprow['view_cnt']
            list_item['api_type'] = type_value
            temp.append(list_item)

        # 전체 시청가구수
        list_item_tot = {}
        list_item_tot['time'] = item['time']
        list_item_tot['api_type'] = type_value
        
        # 실시간 채널 비교는 Skylife만
        if type == Const.RANGE_INTEREST_CH:
            list_item_tot['tot_view_cnt'] = item['viewCntOTS'] + item['viewCntOTV']
        elif type == Const.RANGE_COMPARE_CH:
            list_item_tot['tot_view_cnt'] = item['viewCntOTS']
        temp_tot.append(list_item_tot)

    # 상세 데이터 파일 저장
    dc.export_csv(type, current_time, temp)

    # 전체시청가구수 데이터 파일 저장
    dc.export_csv(type+'_tot', current_time, temp_tot)
