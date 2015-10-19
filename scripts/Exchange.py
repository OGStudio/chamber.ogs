
import math
import pymjin2

EXCHANGE_ALLOWED_ERROR = 0.01

class ExchangeState(object):
    def __init__(self):
        self.subject = None

class ExchangeImpl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
        self.enabled = {}
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
#    def onSelection(self, sceneName, nodeName):
#        node = sceneName + "." + nodeName
#        if (node not in self.selectable):
#            return
#        bs = self.selectable[node]
#        st = pymjin2.State()
#        st.set("{0}.node".format(bs.press), node)
#        st.set("{0}.active".format(bs.press), "1")
#        self.action.setState(st)
    def setEnabled(self, sceneName, nodeName, state):
        node = sceneName + "." + nodeName
        if (state):
            es = ExchangeState()
            self.enabled[node] = es
        # Remove disabled.
        elif (node in self.enabled):
            #es = self.enabled[node]
            del self.enabled[node]
    def setLocatorPosition(self, sceneName, position):
        print "Exchange.setLocatorPosition", sceneName, position
        v = position.split(" ")
        x = float(v[0])
        y = float(v[1])
        # WARNING: We look into all scenes, not specific one.
        # Loop through exchanges to find one by matching positions.
        for k in self.enabled.keys():
            print "locate", k
            key = "node.{0}.positionAbs".format(k)
            st = self.scene.state([key])
            if (not len(st.keys)):
                continue
            pos = st.value(key)[0]
            v = pos.split(" ")
            ex = float(v[0])
            ey = float(v[1])
            if ((math.fabs(x - ex) <= EXCHANGE_ALLOWED_ERROR) and
                (math.fabs(y - ey) <= EXCHANGE_ALLOWED_ERROR)):
                print "matched exchange", k
            else:
                print "didn't match exchange", k
    def setSubject(self, sceneName, nodeName, subject):
        node = sceneName + "." + nodeName
        if (node in self.enabled):
            es = self.enabled[node]
            es.subject = subject
        else:
            print "Could not set subject, because exchange is disabled"

class ExchangeListenerLocation(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            print "Exchange location", k, st.value(k)
#            v = k.split(".")
#            sceneName = v[1]
#            nodeName = st.value(k)[0]
#            # Ignore deselection.
#            if (not len(nodeName)):
#                continue
#            self.impl.onSelection(sceneName, nodeName)

class ExchangeExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self, impl):
        pymjin2.Extension.__init__(self)
        # Refer.
        self.impl = impl
    def deinit(self):
        # Derefer.
        self.impl = None
        print "ExchangeExt.deinit"
    def description(self):
        return "Turn any node into an exchange point"
    def keys(self):
        return ["exchange...subject",
                "exchange...enabled",
                "exchangeLocator..position"]
    def name(self):
        return "ExchangeExtensionScriptEnvironment"
    def set(self, key, value):
        v = key.split(".")
        type      = v[0]
        sceneName = v[1]
        if (type == "exchange"):
            nodeName = v[2]
            property = v[3]
            if (property == "enabled"):
                self.impl.setEnabled(sceneName, nodeName, value == "1")
            elif (property == "subject"):
                self.impl.setSubject(sceneName, nodeName, value)
        elif (type == "exchangeLocator"):
            self.impl.setLocatorPosition(sceneName, value)

class Exchange:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl             = ExchangeImpl(scene, action, scriptEnvironment)
        self.listenerLocation = ExchangeListenerLocation(self.impl)
        self.extension        = ExchangeExtensionScriptEnvironment(self.impl)
        # Prepare.
#        key = "selector..selectedNode"
#        self.scene.addListener([key], self.listenerSelection)
        self.senv.addExtension(self.extension)
        print "{0} Exchange.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        #self.scene.removeListener(self.listenerSelection)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.listenerLocation
        del self.extension
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Exchange.__del__".format(id(self))

