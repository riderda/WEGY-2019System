import datetime
import json
def calendar_one():
    holidayName = ["正式开课","中秋节","计算机二级","国庆节","英语四六级","考研","元旦","考试周","放假"]
    holidayDate = ["2019-9-2","2019-9-13","2019-9-21","2019-10-1","2019-12-14","2019-12-21","2020-1-1","2020-1-4","2020-1-10"]
    gapDays = []
    holidayRestInfo = ["9月9日","9月13日","9月21日","10月1日~7日(放假7天)","12月14日","12月21日","1月1日","1月4日","1月10日"]
    holidayName.reverse()
    holidayDate.reverse()
    holidayRestInfo.reverse()
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    d1 = datetime.datetime.strptime(now, '%Y-%m-%d')
    for n in range(len(holidayName)):
        d2 = datetime.datetime.strptime(holidayDate[n], '%Y-%m-%d')
        delta = d2 - d1
        gapDays.append(str(delta.days))
    nextHoliday = ''
    for n in range(len(holidayName)):
        nextHoliday = '{'+ '"holidayName":"'+ holidayName[n] + '","holidayDate":"' + holidayDate[n] + '","gapDays":"' + gapDays[n] + '","holidayRestInfo":"' + holidayRestInfo[n] +'"},'+ nextHoliday
    nextHoliday = nextHoliday[:-1]
    day = datetime.date.today().isoweekday()
    nextHoliday = '['+ nextHoliday + ']'
    if(day == 1):
        day = '星期一'
    elif(day == 2):
        day = '星期二'
    elif(day == 3):
        day = '星期三'
    elif(day == 4):
        day = '星期四'
    elif(day == 5):
        day = '星期五'
    elif(day == 6):
        day = '星期六'
    else:
        day = '星期七'
    dayOfWeek = day
    day = datetime.datetime.now().strftime('%d')
    month = datetime.datetime.now().strftime('%m')
    d2 = datetime.datetime.strptime("2020-1-1", '%Y-%m-%d')
    examWeekDate = "2020-1-1"
    gap2ExamWeek = d2 - d1
    gap2ExamWeek = gap2ExamWeek.days
    data = '{"day":"'+ str(day) + '","dayOfWeek":"' + dayOfWeek + '","examWeekDate":"' + str(examWeekDate) + '","gap2ExamWeek":"' + str(gap2ExamWeek) + '","gap2StartClass":"' + gapDays[0] + '","month":"'+ month + '","nextHoliday":' + nextHoliday + '}'
    temp = json.loads(data)
    data = json.dumps(temp)
    return data

