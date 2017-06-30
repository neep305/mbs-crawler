from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import requests

loginId = 'mbsgs9'

loginPayload = {
    'loginId':loginId,
    'loginPw':'mbslive45@',
    'channel':'on'
}

s = requests.Session()

r = s.post('https://mbs.kt.com:8080/doLogin.do', data=loginPayload, verify=False, allow_redirects=False)

r = s.post('https://mbs.kt.com:8080/home/homeMain.do', verify=False, allow_redirects=False)

print(r.text)

uiCookie = r.request.headers['Cookie'] + ';loginId=' + loginId

def getRequestForCrawling():
    today = datetime.today()
    strToday = today.strftime('%Y%m%d%H%M%S')
    print(strToday)

    payload = {'lastTime':'20170523000000', 'chGbnCd':'', 'screenType':'S'}

    print(s.cookies)

    r = s.get('https://mbs.kt.com:8080/chart/rangeCompareCh.do', params=payload, verify=False)

    print(r.text)

sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(getRequestForCrawling, 'cron', second='*/10')

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
# sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')

sched.start()
