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

	def createFieldNames(self):
		fieldName = 'field'
		self.fields = []
		for idx in range(self.numfields):
			self.fields.append(fieldName + str(idx))

	def createValues(self):
		self.values = []
		for idx in range(self.numfields):
			self.values.append(random.randint(100,999))

	def createTimeStamp(self):
    		self.timestamp =  str(datetime.datetime.now())
		return self.timestamp

	def clearEventData(self):
		self.fields = []
		self.values = []
		self.timestamp = ''
		self.currentEvent = ''

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


class CsvGenerator(Generator):
	def __init__(self, conf):
		Generator.__init__(self, conf)
		self.firstEvent = True

	def createEvent(self):
		if self.firstEvent == True:
			self.firstEvent = False
			return self.createHeader()
		self.clearEventData()
		self.createValues()
		self.createTimeStamp()
		return self.mergeData()

	def createHeader(self):
		header = 'timestamp,'
		self.createFieldNames()
		for idx in range(self.numfields):
			delim = self.getDelim(idx)
			header += (str(self.fields[idx]) + delim)
		header += '\n'
		self.header = header
		return self.header

	def mergeData(self):
		event = self.timestamp + ','
		for idx in range(self.numfields):
			delim = self.getDelim(idx)
			event += (str(self.values[idx]) + delim)
		event += '\n'
		self.currentEvent = event
		return event

	def getDelim(self, idx):
		if idx == (self.numfields - 1):
			delim = ''
		else:
			delim = ','
		return delim

class XmlGenerator(Generator):
	def __init__(self, conf):
		Generator.__init__(self, conf)
