
# Nfcpyr Plugin Example
# Requires five methods: init(), on_scan(), on_checkin(), on_checkout(), on_fail()
# Important: all methods should use try/except to not crash nfcpyr!

# Config
cfg = {}
cfg["plugin_id"] = "pluginExample"
cfg["plugin_name"] = "Nfcpyr Plugin Example"

# Global variables
readerdict = None

# Plugin.init()
# Called when nfcpyr is started
# Arguments: reader config dictionary
def init(arguments={}):
    try:
        print(str(cfg["plugin_id"]) +".init()")
        readerdict = arguments["readerdict"]
        print(" -> Reader_id: "+ str(readerdict["id"]))
    except:
        return False
    return True

# Plugin.on_scan()
# Called when user scans tag (plugin_id needs to be in reader config -> on_scan -> plugins)
# Arguments: user dictionary
def on_scan(arguments):
    try:
        print(str(cfg["plugin_id"]) +".on_scan()")
        print(" -> Username: "+ str(arguments["userdict"]["username"]))
        # ...
    except:
        return False
    return True

# Plugin.on_checkin()
# Called when user checks in (plugin_id needs to be in reader config -> on_checkin -> plugins)
# Arguments: user dictionary
def on_checkin(arguments):
    try:
        print(str(cfg["plugin_id"]) +".on_checkin()")
        print(" -> Username: "+ str(arguments["userdict"]["username"]))
        # ...
    except:
        return False
    return True

# Plugin.on_checkout()
# Called when user scans tag (plugin_id needs to be in reader config -> on_checkout -> plugins)
# Arguments: user dictionary
def on_checkout(arguments):
    try:
        print(str(cfg["plugin_id"]) +".on_checkout()")
        print(" -> Username: "+ str(arguments["userdict"]["username"]))
        # ...
    except:
        return False
    return True

# Plugin.on_fail()
# Called when any of the on_.. methods returned False
# Arguments: (str) method name that failed or 'unknown'
def on_fail(methodname="unknown"):
    try:
        print(str(cfg["plugin_id"]) +".on_fail()")
        print(" -> "+ str(methodname))
    except:
        pass
