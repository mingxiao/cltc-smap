import urllib2
import ast
import datetime

uuid = '53cc00bb-1b69-5740-a88b-0c391578b15d'
def get_value(uuid, starttime, unit = 'A'):
    """
    Gets the value of the timeseries associated with uuid, at the time
    previous starttime

    uuid - uuid of the timeseries
    starttime - time in unix milliseconds since epoch
    unit - Unit of Measure
    """
    assert len(uuid) == 36
    assert len(str(starttime)) == 13
    URL = "http://new.openbms.org/backend/api/prev/uuid/%s/Properties__UnitofMeasure/%s?starttime=%s"%(uuid,
                                                                                                       unit,
                                                                                                       starttime) 
    reponse = urllib2.urlopen(URL)
    html = reponse.read()
    print html
    datalist = ast.literal_eval(html)
    assert len(datalist)>0
    data = datalist[0] #data is a dictionary
    assert 'Readings' in data
    assert len(data['Readings']) > 0
    value = data['Readings'][0][1]
    return value

def get_range_value(uuid,starttime,endtime,unit='A'):
    """
    Gets a range of values from the timeseries associated with uuid,from starttime to endtime

    OUTPUT
        values - list of floats
    INPUT
        uuid - the uuid of the timeseries, string
        starttime - start time in UNIX milliseconds since epoch, int
        endtime - end time in UNIX milliseconds since epoch, int
        unit - the unit of measure, string
    """
    URL = "http://new.openbms.org/backend/api/data/uuid/%s/Properties__UnitofMeasure/%s?starttime=%s&endtime=%s"%(uuid,
                                                                                                                  unit,
                                                                                                                  starttime,
                                                                                                                  endtime)
    response = urllib2.urlopen(URL)
    html=response.read()
    #print html
    datalist = ast.literal_eval(html)
    #print len(datalist)
    datadict = datalist[0]
    readings = datadict['Readings']
    #print readings
    values = [r[1] for r in readings]
    #print values
    return values

def unix_ms(month,day,hour,minute,second=0,year=2013):
    """
    Returns the milliseconds since UNIX epoch since the date and time inputed
    """
    try:
        some_date = datetime.datetime(year, month,day,hour,minute,second)
        timestamp = float(some_date.strftime('%s.%f'))
        return int(timestamp*1000)
    except ValueError:
        print '! Invalid date or time !'

def epoch_time():
    """
    Return the current time in milliseconds since the UNIX epoch
    """
    now = datetime.datetime.now()
    timestamp = float(now.strftime('%s.%f'))
    return int(timestamp*1000)

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0
    
#print epoch_time()
#print get_value(uuid,epoch_time())
if __name__ == '__main__':
    result =get_range_value(uuid,unix_ms(1,15,1,0), unix_ms(1,15,1,30))

