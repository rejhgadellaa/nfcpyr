
import os
import rgfileio

class RgPluginMgr(object):

    path_plugins = None
    pluginNames = []
    pluginObjs = []

    def __init__(self, _path_plugins=None):
        self.path_plugins = _path_plugins

    def importPlugins(self):
        # check dir
        if not os.path.exists(self.path_plugins):
            return False
        # read dir
        files = rgfileio.listdirr(self.path_plugins)
        # walk files..
        for i in range(0, len(files)):
            # create import compatible name..
            fname = os.path.basename(files[i])
            fpath = os.path.join(self.path_plugins,fname)
            pname = fpath.replace("/",".") # fwd slash..
            pname = pname.replace("\\",".") # bwd slash..
            # store name in list
            self.pluginNames.append(pname)
        # import plugins
        self.pluginObjs = map(__import__,self.pluginNames)
        return True

    def call(self, pluginName, methodName, arguments={}):
        # find plugin index..
        pindex = self.pluginNames.find(pluginName)
        if pindex < 0:
            return False
        # Call method..
        res = False
        try:
            res = self.pluginObjs[0][methodName](arguments)
        except:
            pass
        return res
