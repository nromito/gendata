import sys
import os
import random
import time
import datetime
from daemon import Daemon


def createFieldNames(numfields=10):
    fieldName = 'field'
    fields = []
    for idx in range(numfields):
        fields.append(fieldName + str(idx))
    return fields

def createValues(fields):
    numfields = len(fields)
    values = []
    for idx in range(numfields):
        values.append(random.randint(100,999))
    return values

def createTimeStamp():
    return str(datetime.datetime.now())


def mergeData(timestamp, fields, values, multiline, fieldsPerLine):
    event = timestamp + ' '
    count = 0
    if multiline:
        event += '\n'
    for idx in range(len(fields)):
        event += (str(fields[idx]) + '=' + str(values[idx]) + ' ')
        count += 1
        if multiline and count==fieldsPerLine:
            event += '\n'
            count = 0
    if not multiline:
        event += '\n'
    return event

def maxEvent():
    fieldName = 'field='
    ts = createTimeStamp()
    event = ts + ' ' + fieldName
    sizeNeeded = 10000 - (len(event))
    value = ''
    for idx in range(sizeNeeded):
        value += str(random.randint(1,9))
    event += '\n'
    for idx in range(255):
        event += (value + '\n')
    return event


def createEvent(numfields, multiline=False, fieldsPerLine=1, maxSize=False):
    if not maxSize:
        fields = createFieldNames(numfields)
        values = createValues(fields)
        timestamp = createTimeStamp()
        event = mergeData(timestamp, fields, values, multiline, fieldsPerLine)
    else:
        event = maxEvent()
    return event


def genData(conf):
    filename = 'test.log'
    numfields = 10
    multiline = False
    eventsPerLine = 1
    if 'filename' in conf:
        filename = conf['filename']
    if 'numfields' in conf:
        numfields = int(conf['numfields'])
    if 'multiline' in conf:
        multiline = bool(conf['multiline'])
        if 'fieldsPerLine' in conf:
            fieldsPerLine = int(conf['fieldsPerLine'])
    logfile = open(filename, 'a')
    while 1:
        event = createEvent(numfields, multiline, fieldsPerLine)
        logfile.write(event)
        logfile.flush()
        os.fsync(logfile)
        time.sleep(random.uniform(0,3))


def loadConf():
    confFile = open('/tmp/gendata.conf', 'r')
    conf = {}
    for line in confFile:
        stripped = "".join(line.split())
        kv = stripped.split('=')
        conf[kv[0]] = kv[1]
    return conf

class GenDataDaemon(Daemon):
    def run(self):
	conf = loadConf()
	genData(conf)

	
if __name__ == '__main__':
    daemon = GenDataDaemon('/tmp/gendata.pid', stdout='/tmp/gendata_stdout.log', stderr='/tmp/gendata_stderr.log')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
