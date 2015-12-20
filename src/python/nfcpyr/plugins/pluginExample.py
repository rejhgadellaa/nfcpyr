#!/usr/bin/python
# -*- coding: utf-8 -*-

# Nfcpyr Plugin Example
# Requires five methods: init(), on_scan(), on_checkin(), on_checkout(), on_fail()
# It is encouraged to also include log()
# Important: all methods should use try/except to not crash nfcpyr!

# Config
cfg = {}
cfg["plugin_id"] = "pluginExample"
cfg["plugin_name"] = "Nfcpyr Plugin Example"

# Global variables
readerdict = None

# Plugin.log()
loglines = []
def log(line=""):
    loglines.append(str(line))

# Plugin.init()
# Called when nfcpyr is started
# Arguments: 'readerdict' reader config dictionary
def init(**kwargs):
    try:
        log(str(cfg["plugin_id"]) +".init()")
        readerdict = kwargs["readerdict"]
        log(" > Reader_id: "+ str(readerdict["id"]))
    except Exception as e:
        log(" > Exception: "+ str(e))
        return False
    return True

# Plugin.on_scan()
# Called when user scans tag (plugin_id needs to be in reader config -> on_scan -> plugins)
# Arguments: 'userdict' user dictionary
def on_scan(**kwargs):
    try:
        log(str(cfg["plugin_id"]) +".on_scan()")
        log(" > Username: "+ str(kwargs["userdict"]["username"]))
        # ...
    except Exception as e:
        log(" > Exception: "+ str(e))
        return False
    return True

# Plugin.on_checkin()
# Called when user checks in (plugin_id needs to be in reader config -> on_checkin -> plugins)
# Arguments: 'userdict' user dictionary
def on_checkin(**kwargs):
    try:
        log(str(cfg["plugin_id"]) +".on_checkin()")
        log(" > Username: "+ str(kwargs["userdict"]["username"]))
        # ...
    except Exception as e:
        log(" > Exception: "+ str(e))
        return False
    return True

# Plugin.on_checkout()
# Called when user scans tag (plugin_id needs to be in reader config -> on_checkout -> plugins)
# Arguments: 'userdict' user dictionary
def on_checkout(**kwargs):
    try:
        log(str(cfg["plugin_id"]) +".on_checkout()")
        log(" > Username: "+ str(kwargs["userdict"]["username"]))
        # ...
    except Exception as e:
        log(" > Exception: "+ str(e))
        return False
    return True

# Plugin.on_fail()
# Called when any of the on_.. methods returned False
# Arguments: 'method' name that failed or 'unknown'
def on_fail(**kwargs):
    try:
        log(str(cfg["plugin_id"]) +".on_fail()")
        if "method" in kwargs:
            log(str(kwargs["method"]))
    except Exception as e:
        log(" > Exception: "+ str(e))
        pass
