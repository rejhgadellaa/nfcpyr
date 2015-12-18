
import sys
import os
import simplejson as json

import rgfileio

# ==============================
# JSON

def load(filepath, resDefault=None):
	try:
		datas = rgfileio.read(filepath)
		dataj = json.loads(datas)
		return dataj
	except ValueError as e:
		print(" -> rgjson.load().Error, return '"+ str(resDefault) +"'")
		print(" -> "+ str(e))
		return resDefault
		
def loads(jsons, resDefault=None):
	try:
		dataj = json.loads(jsons)
		return dataj
	except ValueError as e:
		print(" -> rgjson.loads().Error, return '"+ str(resDefault) +"'")
		print(" -> "+ str(e))
		return resDefault
		
def loadurl(url, resDefault=None):
	if sys.version_info < (3,0):
		import rghttp2 as rghttp
	else:
		import rghttp
	try:
		datas = rghttp.geturl(url)
		dataj = json.loads(datas)
		return dataj
	except ValueError as e:
		print(" -> rgjson.load().Error, return '"+ str(resDefault) +"'")
		print(" -> "+ str(e))
		return resDefault
	
def save(filepath,jsonobj):
	try:
		datas = json.dumps(jsonobj, sort_keys = False, indent = 4)
		rgfileio.write(filepath, datas)
		return True
	except ValueError as e:
		print(" -> rgjson.save().Error, return '"+ str(resDefault) +"'")
		print(" -> "+ str(e))
		return resDefault
		
def saves(filepath,jsons, resDefault=False):
	try:
		data = json.loads(jsons)
		datas = json.dumps(data, sort_keys = False, indent = 4)
		rgfileio.write(filepath, jsons)
		return True
	except ValueError as e:
		print(" -> rgjson.saves().Error, return '"+ str(resDefault) +"'")
		print(" -> "+ str(e))
		return resDefault