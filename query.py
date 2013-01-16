import urllib2
import ast
import datetime as dt

uuid = '53cc00bb-1b69-5740-a88b-0c391578b15d'
def get_value(uuid, starttime, unit = 'A'):
    """
    Gets the value of the timeseries associated with uuid, at the time previous starttime

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


def epoch_time():
    """
    Return the current time in milliseconds since the UNIX epoch
    """
    now = dt.datetime.now()
    timestamp = float(now.strftime('%s.%f'))
    return int(timestamp*1000)
    
#print epoch_time()
print get_value(uuid,epoch_time())
