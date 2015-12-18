
from datetime import datetime, date, time
import rgjson

class RgLog(object):
	
	logfile = "log.json"
	maxlen = 1024
	
	logjson = []
	
	def __init__(self, _logfile="log.jon", _maxlen=1024):
			
			self.logfile = _logfile
			self.maxlen = _maxlen
			self.readLogfile()
			
	def setLogfile(self, _logfile):
		self.logfile = _logfile
		self.readLogfile()
		
	def readLogfile(self):
		self.logjson = rgjson.load(self.logfile,[])
		
	def writeLogfile(self):
		rgjson.save(self.logfile,self.logjson)
			
	def log(self, line, doprint=True):
		line = datetime.now().strftime("%m-%d %H:%M:%S")  +"    "+ str(line)
		self.logjson.append(line)
		while len(self.logjson)>self.maxlen:
			self.logjson.pop(0)
		if doprint:
			print(line)
		self.writeLogfile()
		
	