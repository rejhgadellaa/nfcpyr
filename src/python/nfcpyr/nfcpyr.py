
import os
import sys
import time
import json
import traceback

import netifaces

import nfc

import rgaudio
import rgfileio
import rghttp2
import rgjson
import rglog

# -------------------------------------------------------------------------
# Nfcpyr

class Nfcpyr(object):

    # -----------------------------------
    # Members

    # -----------------------------------
    # Construct

    def __init__(self):

        # INIT LOG
        self.rglog = rglog.RgLog("logs/log.json")
        self.rglog.log("Nfcpyr.init()")

        # INIT OBJS
        self.rgaudio = rgaudio.RgAudio()

        # PREPARE VALUES
        self.timeConnected = -1

        # LOAD CONFIG
        self.rglog.log(" -> Load config..")
        self.config = rgjson.load("data/nfcpyr.config.json", {})

        # LOAD AUTHKEY
        self.rglog.log(" -> Load authkey..")
        self.authkey = rgfileio.read("data/nfcpyr.authkey")
        if (self.authkey == None or self.authkey == "None"):
            # Check if we can get (a new) auth..
            if "nfcpyr_id" not in self.config or "nfcpyr_user" not in self.config or "nfcpyr_pass" not in self.config:
                self.rglog.log("Could not authenticate, cannot request (new) authkey because nfcpyr_id, user and/or pass are missing")
                sys.exit(1)
            # get_authkey
            self.rglog.log(" --> Get authkey using credentials..")
            self.authkey = self.apiexec("a=get_authkey"
                +"&nfcpyr_id="+ self.config["nfcpyr_id"]
                +"&nfcpyr_user="+ self.config["nfcpyr_user"]
                +"&nfcpyr_pass="+ self.config["nfcpyr_pass"],
                "code"
                )
            if (self.authkey == 102):
                # get_new_authkey
                # self.authkey = self.apiexec("a=get_new_authkey&nfcpyr_id="+ str(self.config["nfcpyr_id"]),{})
                self.rglog.log(" --> Get new authkey using credentials..")
                self.authkey = self.apiexec("a=get_new_authkey"
                    +"&nfcpyr_id="+ self.config["nfcpyr_id"]
                    +"&nfcpyr_user="+ self.config["nfcpyr_user"]
                    +"&nfcpyr_pass="+ self.config["nfcpyr_pass"]
                    )
            else:
                self.rglog.log("Error: Unknown auth failure")
            if (self.authkey == None or self.authkey == "None"):
                self.rglog.log("Error: Could not create authkey")
                sys.exit(1)
            rgfileio.write("data/nfcpyr.authkey", self.authkey)
            self.rglog.log(" --> Authkey: "+ str(self.authkey))
            self.rglog.log(" --> OK")

        # LOAD READERS
        self.rglog.log(" -> Load readers..")
        self.readers = self.apiexec("a=get_readers", "code")
        if self.readers == 101:
            os.remove("data/nfcpyr.authkey")
            sys.exit(1)
        self.rglog.log(" --> OK: "+ str(len(self.readers)) +" reader(s)")

        # -> set up reader (self)
        self.reader = self.getReaderById(self.config["reader"]["id"])
        # if not exist: add
        if self.reader == None:
            # register self..
            self.rglog.log(" --> Register self as new reader..")
            self.reader = self.apiexec("a=add_reader&datas="+ rghttp2.encodeURIComponent(json.dumps(self.config["reader"])))
        else:
            # update reader data
            self.rglog.log(" --> Update reader data..")
            self.reader = self.apiexec("a=update_reader&reader_id="+ self.reader["id"] +"&datas="+ rghttp2.encodeURIComponent(json.dumps(self.config["reader"])))
        self.rglog.log(" --> Identified reader: "+ self.reader["name"])

        # -> register reader as online..
        # TODO: how to register offline..? timeout?
        self.rglog.log(" --> Register reader as online..")
        res = self.apiexec("a=register_reader_online"
            +"&reader_id="+ self.reader["id"]
            +"&reader_local_ips="+ rghttp2.encodeURIComponent(json.dumps(self.getIpAddresses())),
            None
            )
        if res == None:
            self.rglog.log(" ---> (E) Failed :(")
            sys.exit(1)
        else:
            self.rglog.log(" ---> "+ str(res))

        # LOAD USERS
        self.rglog.log(" -> Load users..")

        # -> add users from local..
        localusers = rgjson.load("data/nfcpyr.users.json",[])
        if len(localusers)>0:
            self.apiexec("a=add_users&datas="+ rghttp2.encodeURIComponent(json.dumps(localusers)))

        # -> get users from remote
        self.users = self.apiexec("a=get_users",[])
        self.rglog.log(" --> OK: "+ str(len(self.users)) +" user(s)")

        if self.config["sounds"]["enabled"] and "checkin" in self.config["sounds"]:
            self.rgaudio.playfile(self.config["sounds"]["checkin"])

        # INIT READER
        self.rglog.log(" -> Init reader..")
        try:
            self.clf = nfc.ContactlessFrontend('usb')
            self.rglog.log(" --> "+ str(self.clf))
        except IOError as e:
            self.rglog.log(" --> IOError occured")
            self.rglog.log(e)
            sys.exit(1)

        # READY
        self.rglog.log(" -> Ready..")

    # -----------------------------------
    # Run

    def run_once(self):
        self.clf.connect(rdwr={'on-connect':self.on_card_connect})
        return True

    def run(self):
        while self.run_once(): pass
        self.exit()

    def exit(self):
        self.rglog.log("Nfcpyr.Exit()")
        self.clf.close()
        sys.exit(1)

    # -----------------------------------
    # ON_CARD_CONNECT

    def on_card_connect(self,tag):

        # Check timeConnected
        if time.time() - self.timeConnected < 2:
            return True
        self.timeConnected = time.time()

        # Log on_card_connect
        self.rglog.log("Nfcpyr.on_card_connect()")
        self.rglog.log(" -> "+ str(tag))

        # Parse tag
        tagdict = self.nfcpyGetTagDict(tag)

        # Check tagdict..
        if "ID" not in tagdict:
            self.rglog.log(" -> No 'ID', ignore tag..")
            return

        # We're good, do stuff..
        self.rglog.log(" -> tag.ID: "+ str(tagdict["ID"]))

        # Get userdict
        userdict = self.getUserDictByTagID(tagdict["ID"])
        self.rglog.log(" -> User: "+ userdict["fullname"])

        # TODO: Update 'data'

        # FOR NOW: assume check in...
        checkedin = self.apiexec("a=checkinout&reader_id="+ str(self.reader["id"]) +"&username="+ userdict["username"])
        self.rglog.log(" -> Checkedin: "+ str(checkedin))

        # -> Figure event..
        if checkedin: event = "on_checkin"
        else: event = "on_checkout"

        # Run on_checkXXX event..
        self.runEvent(event, userdict)

        # Run on_scan event
        self.runEvent("on_scan", userdict)

    def runEvent(self, event, userdict, reader=None, skipReaderIds=[]):

        self.rglog.log("Nfcpyr.runEvent(): "+ str(event))

        # Check reader..
        if reader is None:
            reader = self.reader

        # Append reader to skipReaderIds
        skipReaderIds.append(reader["id"])

        # DO ACTIONS
        # TODO: actions are the same for checkin and checkout
        if event in reader:

            # -> Sound
            if self.config["sounds"]["enabled"] and event in self.config["sounds"]:
                self.rgaudio.playfile(self.config["sounds"][event])

            # -> Checkouts (checks out for other readers)
            if "checkout" in reader[event]:
                checkoutids = reader[event]["checkout"]
                self.rglog.log(" --> Checkout: "+ str(len(checkoutids)))
                for i in range(0, len(checkoutids)):
                    checkoutid = checkoutids[i]
                    if reader["id"] == checkoutid: continue # skip self
                    if reader["id"] in skipReaderIds: continue # skip
                    # Get reader
                    checkoutreader = self.getReaderById(checkoutid)
                    if checkoutreader == None:
                        self.rglog.log(" ---> (W) "+ checkoutid +" NOT FOUND")
                        continue
                    self.rglog.log(" ---> "+ checkoutid)
                    # Do checkout @ server
                    self.apiexec("a=checkout&reader_id="+ str(checkoutid) +"&username="+ userdict["username"])
                    # Perform checkout actions for reader..
                    self.runEvent("on_checkout", userdict, checkoutreader, skipReaderIds)

            # Checkins (checks in for other readers)
            if "checkin" in reader[event]:
                checkinids = reader[event]["checkin"]
                self.rglog.log(" --> Checkin: "+ str(len(checkinids)))
                for i in range(0, len(checkinids)):
                    checkinid = checkinids[i]
                    if reader["id"] == checkinid: continue # skip self
                    if reader["id"] in skipReaderIds: continue # skip
                    # Get reader
                    checkinreader = self.getReaderById(checkinid)
                    if checkinreader == None:
                        self.rglog.log(" ---> (W) "+ checkinid +" NOT FOUND")
                        continue
                    self.rglog.log(" ---> "+ checkinid)
                    # Do checkout @ server
                    self.apiexec("a=checkin&reader_id="+ str(checkinid) +"&username="+ userdict["username"])
                    # Perform checkout actions for reader..
                    self.runEvent("on_checkin", userdict, checkinreader, skipReaderIds)

            # -> Url_requests
            if "url_requests" in reader[event]:
                urlreqs = reader[event]["url_requests"]
                self.rglog.log(" --> Url requests: "+ str(len(urlreqs)))
                for i in range(0, len(urlreqs)):
                    urlreq = self.injectKeywords(urlreqs[i],userdict)
                    self.rglog.log(" ---> "+ urlreq)
                    urlreqres = rghttp2.geturl(urlreq)
                    self.rglog.log(" ----> "+ str(urlreqres))
                    # TODO: replace ##KEYWORDS##

        else:
            # Nothing..
            self.rglog.log(" -> Nothing to do...")

    # -----------------------------------
    # API

    def apiexec(self, query, resDefault=None):
        urlreq = self.config["url_nfcpyrapi"] + query + "&authkey="+ str(self.authkey)
        jsons = rghttp2.geturl(urlreq)
        if jsons == None:
            self.rglog.log("Error: rghttp2.geturl() returned None")
            self.rglog.log(" -> "+ urlreq)
            return resDefault
        jsondata = rgjson.loads(jsons)
        if "error" in jsondata:
            self.rglog.log("Error: "+ str(jsondata["error"]) +", "+ str(jsondata["errormsg"]))
            self.rglog.log(" -> "+ urlreq)
            if resDefault=="code":
                resDefault = jsondata["error"]
            return resDefault
        if "result" not in jsondata:
            self.rglog.log("Error: no 'result' in response")
            return resDefault
        return jsondata["result"]

    # -----------------------------------
    # HELPERS: DATA

    def injectKeywords(self,string,userdict,reader=None):
        # TODO: replacers in ext file?
        if reader is None:
            reader = self.reader
        string = str(string)
        replacers = {
            "##USER-USERNAME##": userdict["username"],
            "##USER-FULLNAME##": userdict["fullname"],
            # "##USER-EMAIL##": userdict["email"],
            "##READER-ID##": reader["id"],
            "##READER-NAME##": reader["name"],
            "##TIMESEC##": str(round(time.time())),
            "##TIMEMS##": str(round(time.time() * 1000))
        }
        for lookup in replacers:
            if string.find(lookup)>=0:
                string = string.replace(lookup, str(replacers[lookup]))
        return string

    def getReaderById(self,readerID):
        for readerdict in self.readers:
            if readerdict["id"] == readerID:
                return readerdict
        return None

    def getUserDictByTagID(self,tagID):
        for userdict in self.users:
            if tagID in userdict['nfctags']:
                return userdict
        return None

    # -----------------------------------
    # HELPERS: NFCPY

    def nfcpyGetTagDict(self,tag):
        tagdict = {}
        tagKeyValues= str(tag).split(" ")
        for i in range(0,len(tagKeyValues)):
            try:
                tagKeyValuePairs = tagKeyValues[i].split("=")
                tagdict[tagKeyValuePairs[0]] = tagKeyValuePairs[1]
            except Exception:
                pass
        return tagdict

    # -----------------------------------
    # HELPERS: OTHERS

    # NETIFACES
    def getIpAddresses(self):
        res = {}
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface != None:
                for j in iface:
                    # skip networks without broadcast and netmask (they are not the ips we're looking for)
                    if 'broadcast' not in j or 'netmask' not in j:
                        continue
                    # skip local ip (it's not the ip we're looking for)
                    if j['addr'] == "127.0.0.1":
                        continue
                    # okay this is an ip we're looking for..
                    # print(i +", "+ str(j))
                    res[i] = j['addr']
        return res

# -------------------------------------------------------------------------
# Run

if __name__ == '__main__':
    try:
        nfcpyr = Nfcpyr()
        nfcpyr.run()
    except KeyboardInterrupt:
        print("KeyboardInterrupt.Exit")
        try:
            nfcpyr.exit()
        except:
            print("Error: could not close nfcpyr correctly :(")
        sys.exit(1)
        raise
    except SystemExit:
        print("Sys.Exit")
        try:
            nfcpyr.exit()
        except:
            print("Error: could not close nfcpyr correctly :(")
            sys.exit(1)
        raise
    except Exception as e:
        type_, value_, traceback_ = sys.exc_info()
        traceback_ = traceback.format_tb(traceback_)
        print(type_)
        print(value_)
        trlines = ""
        for trline in traceback_:
            trlines += trline
        print(trlines)
        sys.exit(1)
