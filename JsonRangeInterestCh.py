import json
import DataframeConverter as dc
import Const

def convert_json(service_type, screen_type, type, result, strToday):
    try:

        data = json.loads(result)

        if type == 'range_interest_ch':
            convert_df_to_csv(service_type, screen_type, type, data, strToday)
        elif type == 'range_compare_ch':
            convert_df_to_csv(service_type, screen_type, type, data, strToday)
        else:
            print('Not Available Yet')
    except RuntimeError as re:
        print(re)

# Skylife 관심채널 시청가구 변화추이
def convert_df_to_csv(service_type, screen_type, type, data, current_time):
    temp = []
    temp_tot = []

    type_value = 'I'

    # print(service_type)

    if type == Const.RANGE_COMPARE_CH:
        type_value = 'C'

    for item in data['chList']:
        for temprow in item['list']:
            list_item = {}
            list_item['time'] = item['time']
            list_item['prgm_id'] = temprow['prgm_id']
            list_item['ch_no'] = temprow['ch_no']
            list_item['ch_nm'] = temprow['ch_nm']
            list_item['disp_ch_nm'] = temprow['disp_ch_nm']
            list_item['view_cnt'] = temprow['view_cnt']
            # 추가 20171019 by Jason
            list_item['api_type'] = type_value + screen_type
            list_item['service_type'] = service_type

            temp.append(list_item)

        # 전체 시청가구수
        list_item_tot = {}
        list_item_tot['time'] = item['time']
        list_item_tot['api_type'] = type_value
        list_item_tot['service_type'] = service_type

        # 실시간 채널 비교는 Skylife만 계산함. (MBS사이트에서도 Dashboard와 실시간 채널상의 값이 다르게 계산됨)
        if type == Const.RANGE_INTEREST_CH:
            list_item_tot['tot_view_cnt'] = item['viewCntOTS'] + item['viewCntOTV']
        elif type == Const.RANGE_COMPARE_CH:
            list_item_tot['tot_view_cnt'] = item['viewCntOTS']
        temp_tot.append(list_item_tot)

    # 상세 데이터 파일 저장
    if service_type == 'T':
        dc.export_csv(type+'_tc', current_time, temp)
    else:
        dc.export_csv(type, current_time, temp)

    # 전체시청가구수 데이터 파일 저장
    if service_type == 'T':
        dc.export_csv(type+'_tc_tot', current_time, temp_tot)
    else:
        dc.export_csv(type+'_tot', current_time, temp_tot)
