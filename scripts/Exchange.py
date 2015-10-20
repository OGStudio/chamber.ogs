
import math
import pymjin2

EXCHANGE_ALLOWED_ERROR = 0.01

class ExchangeState(object):
    def __init__(self):
        self.owners  = []
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
    def exchange(self, sceneName, nodeName):
        node = sceneName + "." + nodeName
        if (node in self.enabled):
            es = self.enabled[node]
            print "exchange with owners", es.owners
            key = "node.{0}.{1}.parent".format(sceneName, es.subject)
            st = self.scene.state([key])
            parent = st.value(key)[0]
            print "current parent:", parent
            if (parent not in es.owners):
                print "Could not exchange, because subject is not part of the owners"
                return
            # Switch owners.
            st = pymjin2.State()
            for o in es.owners:
                if (o != parent):
                    st.set(key, o)
                    break
            self.scene.setState(st)
        else:
            print "Could not exchange, because exchange is disabled"
    def report(self, sceneName, exchange):
        st = pymjin2.State()
        key = "exchangeLocator.{0}.locatedExchange".format(sceneName)
        st.set(key, exchange)
        self.senv.reportStateChange(st)
        st.set(key, "")
        self.senv.reportStateChange(st)
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
        v = position.split(" ")
        x = float(v[0])
        y = float(v[1])
        # WARNING: We look into all scenes, not specific one.
        # Loop through exchanges to find one by matching positions.
        for k in self.enabled.keys():
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
                # We don't need scene name again. Don't use it.
                v = k.split(".")
                self.report(sceneName, v[1])
                return
    def setSubject(self, sceneName, nodeName, subject):
        node = sceneName + "." + nodeName
        if (node in self.enabled):
            es = self.enabled[node]
            es.subject = subject
        else:
            print "Could not set subject, because exchange is disabled"
    def setOwner(self, sceneName, nodeName, owners):
        node = sceneName + "." + nodeName
        if (node in self.enabled):
            es = self.enabled[node]
            es.owners = owners
        else:
            print "Could not set owner, because exchange is disabled"

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
                "exchange...exchange",
                "exchange...owner",
                "exchangeLocator..position",
                "exchangeLocator..selectedExchange"]
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
            elif ((property == "exchange") and
                  (value == "1")):
                    self.impl.exchange(sceneName, nodeName)
            elif (property == "subject"):
                self.impl.setSubject(sceneName, nodeName, value)
            elif (property == "owner"):
                self.impl.setOwner(sceneName, nodeName, value)
        elif (type == "exchangeLocator"):
            self.impl.setLocatorPosition(sceneName, value)

class Exchange:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl      = ExchangeImpl(scene, action, scriptEnvironment)
        self.extension = ExchangeExtensionScriptEnvironment(self.impl)
        # Prepare.
        self.senv.addExtension(self.extension)
        print "{0} Exchange.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        #self.scene.removeListener(self.listenerSelection)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.extension
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Exchange.__del__".format(id(self))

