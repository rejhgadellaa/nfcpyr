#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import imp
import rgfileio

class NfcpyrPluginMgr(object):

    path_plugins = None
    readerdict = None
    pluginObjs = {}

    def __init__(self, _path_plugins=None, _readerdict=None):
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
            self.call(pname,"init", readerdict=self.readerdict)
        return True

    def call(self, pluginName, methodName, **kwargs):
        res = False
        try:
            # check if pluginName exists..
            if pluginName in self.pluginObjs:
                # update readerdict if provided
                if "readerdict" in kwargs:
                    self.pluginObjs[0].readerdict = kwargs["readerdict"]
                # call method
                res = self.pluginObjs[0][methodName](**kwargs)
        except:
            pass
        return res
