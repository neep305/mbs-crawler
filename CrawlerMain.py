from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib
import httplib2
import sys
import JsonRangeInterestCh as cJson

if __name__ == "__main__":
    print(sys.argv)

http = httplib2.Http()

domain = 'https://mbs.kt.com:8080'
url = domain + '/doLogin.do'
body = {'loginId':'mbsgs10','loginPw':'mbslive45@', 'channel': 'on'}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
response, content = http.request(url, 'POST', headers = headers, body = urllib.parse.urlencode(body))

headers = {'Cookie': response['set-cookie']}

def request_for_crawling():
    date = datetime.today() - timedelta(seconds = 90)
    strToday = date.strftime('%Y%m%d%H%M%S')

    # https://125.144.163.12:8080/chart/rangePrgm.do?lastTime=20170424172800&yesterdayLastTime=20170423173300&prevWeekLastTime=20170417173300&chGbnCd=&screenType=T&_=1493022523570
    # 실시간 시청형태 > 채널비교
    url = domain + '/chart/rangeInterestCh.do?lastTime=' + strToday \
          + '&screenType=S&_=' + date.strftime("%s")

    print(url)

    response, content = http.request(url, 'GET', headers=headers)

    print(content.decode('utf-8'))

    # JSON 변경 후 저장
    cJson.convert_json('range_interest_ch', content.decode('utf-8'))

sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(request_for_crawling, 'cron', minute='*/60')

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
# sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

sched.start()
