from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
import urllib
import httplib2
import sys
import JsonRangeInterestCh as cJson
import Const

# 대시보드 > Skylife 관심채널 시청가구 변화추이
# https://125.144.163.12:8080/chart/rangeInterestCh.do?lastTime=20170424172800&screenType=T&_=1493022523570
def request_for_range_interest_ch():

    request_common(Const.RANGE_INTEREST_CH)

# 실시간 시청형태 > 채널비교
def request_for_range_compare_ch():

    request_common(Const.RANGE_COMPARE_CH)

# request 공통
def request_common(type):
    try:
        date = datetime.today() - timedelta(seconds=90)

        str_today = date.strftime(req_date_format)

        req_url = make_req_url(type, date, str_today)

        print(req_url)

        response, content = http.request(req_url, 'GET', headers=headers)

        print(content.decode('utf-8'))

        # JSON 변경 후 저장
        cJson.convert_json(service_type, type, content.decode('utf-8'), date.strftime(Const.FILENAME_FORMAT))
    except BrokenPipeError as bpe:
        print(bpe)
    except RuntimeError as re:
        print(re)

# request url 생성
def make_req_url(type, date, str_today):
    # 대시보드 > Skylife 관심채널 시청가구 변화추이
    if type == Const.RANGE_INTEREST_CH:
        return domain + '/chart/rangeInterestCh.do?lastTime=' + str_today \
               + '&chGbnCd=&screenType=S&_=' + date.strftime("%s")
    # 실시간 시청형태 > 채널비교
    elif type == Const.RANGE_COMPARE_CH:
        return domain + '/chart/rangeCompareCh.do?lastTime=' + str_today \
               + '&screenType=S&_=' + date.strftime("%s")

if __name__ == "__main__":

    param_len = len(sys.argv)

    if param_len < 3:
        sys.exit("login info is empty")

    # loginId
    login_id = sys.argv[1]

    # loginPwd
    login_pwd = sys.argv[2]

    # live or tc
    service_type = sys.argv[3]

    http = httplib2.Http()

    domain = Const.DOMAIN
    url = domain + '/doLogin.do'
    body = {'loginId':login_id,'loginPw':login_pwd, 'channel': 'on'}

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(body))

    req_date_format = Const.REQ_DATE_FORMAT

    headers = {'Cookie': response['set-cookie']}

    sched = BlockingScheduler()
    # sched = BackgroundScheduler()

    # Schedules job_function to be run on the third Friday
    # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
    # sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

    # Schedule job_function to be called every minute 5 second
    sched.add_job(request_for_range_interest_ch, 'cron', second='5')
    sched.add_job(request_for_range_compare_ch, trigger='cron', second='9')

    try:
        sched.start()
    except:
        sched.shutdown()
