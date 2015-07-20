import sys
import os
import random
import time
import datetime
from daemon import Daemon
from loggen import *

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



def genData(generator):
	generator.openLog('a')
	while 1:
		event = generator.createEvent()
		generator.writeEvent(event)
		time.sleep(random.uniform(0,3))


def loadConf():
    confFile = open('/tmp/gendata.conf', 'r')
    conf = {}
    for line in confFile:
        stripped = "".join(line.split())
        kv = stripped.split('=')
        conf[kv[0]] = kv[1]
    return conf

def createGenerator(conf):
	generator = None
	if 'filetype' in conf:
		if conf['filetype'] == 'csv':
			generator = CsvGenerator(conf)
		elif conf['filetype'] == 'xml':
			generator = XmlGenerator(conf)
	else:
		generator = LogGenerator(conf)
	return generator
			
class GenDataDaemon(Daemon):
    def run(self):
	conf = loadConf()
	generator = createGenerator(conf)
	generator = LogGenerator(conf)
	genData(generator)

	
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
