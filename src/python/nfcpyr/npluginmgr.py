#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import imp
import rgfileio
import rglog

class NfcpyrPluginMgr(object):

    path_plugins = None
    readerdict = None
    pluginObjs = {}

    def __init__(self, _path_plugins, _readerdict):
        self.rglog = rglog.RgLog("logs/log-npluginmgr.json")
        self.rglog.log(" --> NfcpyrPluginMgr.init()")
        self.path_plugins = _path_plugins
        self.readerdict = _readerdict
        self.importPlugins()

    def importPlugins(self):
        # check dir
        if self.path_plugins is None:
            return False
        if not os.path.exists(self.path_plugins):
            return False
        # read dir
        files = rgfileio.listdirr(self.path_plugins)
        # walk files..
        for i in range(0, len(files)):
            # create import compatible name..
            fpath = files[i]
            fname = os.path.basename(files[i])
            pname = fname[0:len(fname)-3]
            # ignore pyc files..
            if fname == pname+"pyc":
                continue
            # store name in list
            self.pluginObjs[pname] = imp.load_source(pname,fpath)
        # call init methods
        for pname in self.pluginObjs:
            okay = self.call(pname,"init", readerdict=self.readerdict)
            if not okay:
                self.call(pname,"on_fail", method="init")
        return True

    def call(self, pluginName, methodName, **kwargs):
        res = False
        # clear loglines..
        try:
            self.pluginObjs[pluginName].loglines = []
        except:
            pass
        # call method..
        try:
            # check if pluginName exists..
            if pluginName in self.pluginObjs:
                # update readerdict if provided
                if "readerdict" in kwargs:
                    self.pluginObjs[pluginName].readerdict = kwargs["readerdict"]
                # call method
                res = getattr(self.pluginObjs[pluginName], methodName)(**kwargs)
        except:
            pass
        # print loglines..
        try:
            loglines = self.pluginObjs[pluginName].loglines
            for i in range(0, len(loglines)):
                self.rglog.log(" --> "+ str(loglines[i]))
        except:
            pass
        # return
        return res
