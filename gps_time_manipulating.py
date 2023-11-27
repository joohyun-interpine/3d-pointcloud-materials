    
from datetime import datetime, timedelta
import math
import sys





def StandardTime2LocalTime(gpstime, utctimeoffset_hrs):
    GPSOrigin= datetime(1980, 1, 6,0,0,0)
    gpstime_days_part=math.floor(gpstime/60/60/24)
    gpstime_seconds_part=gpstime-(math.floor(gpstime/60/60/24)*60*60*24)
    
    return GPSOrigin+timedelta(11574,6399)+timedelta(0,utctimeoffset_hrs*60*60)+timedelta(gpstime_days_part,gpstime_seconds_part)
    
def SecondsOfWeek2StandardTime(secondsofweek,surveydate):
    date_format = "%d/%m/%Y"
    a = datetime.strptime('06/01/1980', date_format)
    b = datetime.strptime(surveydate, date_format)
    return secondsofweek+math.floor((b - a).days/7)*604800-1000000000

def SecondsOfWeek2StandardTimeGPSWeek(secondsofweek,gpsweek):
    date_format = "%d/%m/%Y"
    a = datetime.strptime('06/01/1980', date_format)
    b = a+timedelta(days=gpsweek*7)
    return secondsofweek+math.floor((b - a).days/7)*604800-1000000000
    
def StandardTime2SecondsOfWeek(standardtime):
    return standardtime-(math.floor((standardtime+1000000000)/604800)*604800-1000000000)

def GPSWeekFromDate(surveydate):
    date_format = "%d/%m/%Y"
    a = datetime.strptime('06/01/1980', date_format)
    b = datetime.strptime(surveydate, date_format)
    return math.floor((b-a).days/7)

def LocalTime2StandardTime(localtime):
    GPSOrigin= datetime(1980, 1, 6,0,0,0)
    deltatime = (localtime - GPSOrigin)
    return  float(deltatime.days*24*60*60 + deltatime.seconds -1000000000)

def main(argv):

    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('This tool helps converts gps times to and from standard time')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    try: 
        gpstimeformat=int(input('\tGPS time format (1=adjusted standard time 2=seconds of the week 3=show UTC time now):'))
    except:
        return

    if gpstimeformat==1:
        try:
            gpsstandardtime=float(input('\tGPS adjusted standard time:'))
            utctimeoffset_hrs=float(input('\tUTC time offset (hrs):'))
            if not gpsstandardtime=='' and not utctimeoffset_hrs=='':
                secondsofweek=StandardTime2SecondsOfWeek(gpsstandardtime)
                localtime=StandardTime2LocalTime(gpsstandardtime, utctimeoffset_hrs).strftime("%d/%m/%Y %H:%M:%S")  
                gpsweek=GPSWeekFromDate(StandardTime2LocalTime(gpsstandardtime, utctimeoffset_hrs).strftime("%d/%m/%Y"))
            else:
                return
        except:
            return

    elif gpstimeformat==2:
        try:
            secondsofweek=float(input('\tGPS seconds of the week time:'))
            utctimeoffset_hrs=float(input('\tUTC time offset (hrs):'))  
            if not secondsofweek=='' and not utctimeoffset_hrs=='':
                gpsweek=float(input('\tGPS week:'))
                if gpsweek=='':
                    gpsweek=currentgpsweek
                
                gpsstandardtime=SecondsOfWeek2StandardTimeGPSWeek(secondsofweek,gpsweek)
                localtime=StandardTime2LocalTime(gpsstandardtime, utctimeoffset_hrs).strftime("%d/%m/%Y %H:%M:%S") 




        except:
            return

    elif gpstimeformat==3:
        try:
            utctimeoffset_hrs=float(input('\tUTC time offset (hrs):'))
            if not utctimeoffset_hrs=='':
                timenow=datetime.now()-timedelta(0,utctimeoffset_hrs*60*60)
                currentgpsweek=GPSWeekFromDate(timenow.strftime("%d/%m/%Y"))
                gpsstandardtime=LocalTime2StandardTime(timenow)
                secondsofweek=StandardTime2SecondsOfWeek(gpsstandardtime)
                gpsweek=GPSWeekFromDate(StandardTime2LocalTime(gpsstandardtime, 0).strftime("%d/%m/%Y"))


                print('\n\tNote:')
                print('\t\tThe UTC time now is: {0}'.format(timenow.strftime("%d/%m/%Y %H:%M:%S")))
                print('\t\tGPS standard time: {0}'.format(gpsstandardtime))
                print('\t\tGPS seconds of week: {0}'.format(secondsofweek))
                print('\t\tGPS week: {0}'.format(gpsweek))
                print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                return
            else:
                return

        except:
            return

    else:
        return
    
           
    print('\n-------------------------------------------------------------------------------------')
    print('\t\tGPS standard time: {0}'.format(gpsstandardtime))
    print('\t\tGPS seconds of week: {0}'.format(secondsofweek))
    print('\t\tGPS week: {0}'.format(gpsweek))
    print('\t\tLocal time based on UTC offset {0}hrs: {1}'.format(utctimeoffset_hrs,localtime))
    print('-------------------------------------------------------------------------------------\n\n')



if __name__ == "__main__":
    main(sys.argv[1:])         
