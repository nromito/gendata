import random
import sys
import os
import time
import datetime

class GeneratorFactory():
	def __init__(self, conf):
		self.filetype = 'log'
		if 'filetype' in conf:
			self.filetype = conf['filetype']
		self.conf = conf

	def createGenerator(self):
		generator = None
		conf = self.conf
		if self.filetype == 'csv':
			generator = CsvGenerator(conf)
		elif self.filetype == 'xml':
			generator = XmlGenerator(conf)
		else:
			generator = LogGenerator(conf)
		return generator
		
class Generator():
	def __init__(self, conf):
		self.filename = '/tmp/test.log'
		self.numfields = 10
		self.multiline = False
		self.fieldsPerLine = 1
		if 'filename' in conf:
			self.filename = conf['filename']
		if 'numfields' in conf:
			self.numfields = int(conf['numfields'])
		if 'multiline' in conf:
			self.multiline = bool(conf['multiline'])
			if 'fieldsPerLine' in conf:
				self.fieldsPerLine = int(conf['fieldsPerLine'])

	def createTimeStamp(self):
    		self.timestamp =  str(datetime.datetime.now())
		return self.timestamp

	def openLog(self, mode):
		self.logfile = open(self.filename, mode)

	def writeEvent(self, event):
		self.logfile.write(event)
		self.logfile.flush()
		os.fsync(self.logfile)

class LogGenerator(Generator):
	def __init__(self, conf):
		Generator.__init__(self, conf)
	def createEvent(self):
		self.clearEventData()
		self.createFieldNames()
		self.createValues()
		self.createTimeStamp()
		return self.mergeData()
			
	def createFieldNames(self):
		fieldName = 'field'
		self.fields = []
		for idx in range(self.numfields):
			self.fields.append(fieldName + str(idx))

	def createValues(self):
		self.values = []
		for idx in range(self.numfields):
			self.values.append(random.randint(100,999))

	def mergeData(self):
		event = self.timestamp + ' '
		count = 0
		if self.multiline:
			event += '\n'
		for idx in range(self.numfields):
			event += (str(self.fields[idx]) + '=' + str(self.values[idx]) + ' ')
			count += 1
			if self.multiline and count == self.fieldsPerLine:
				event += '\n'
				count = 0
		if not self.multiline:
			event += '\n'
		self.currentEvent = event
		return event

	def clearEventData(self):
		self.fields = []
		self.values = []
		self.timestamp = ''
		self.currentEvent = ''

class CsvGenerator(Generator):
	def __init__(self, conf):
		Generator.__init__(self, conf)

class XmlGenerator(Generator):
	def __init__(self, conf):
		Generator.__init__(self, conf)
