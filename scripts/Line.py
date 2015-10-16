
import pymjin2

#Line_ACTION_GROUP      = "default"
#Line_ACTION_DOWN_TYPE  = "moveBy"
#Line_ACTION_DOWN_NAME  = "moveLineDown"
#Line_ACTION_PRESS_TYPE = "sequence"
#Line_ACTION_PRESS_NAME = "pressLine"

class LineState(object):
    def __init__(self):
        self.down  = None
        self.press = None
#    def setActionGroup(self, groupName):
#        self.down = "{0}.{1}.{2}".format(Line_ACTION_DOWN_TYPE,
#                                         groupName,
#                                         Line_ACTION_DOWN_NAME)
#        self.press = "{0}.{1}.{2}".format(Line_ACTION_PRESS_TYPE,
#                                          groupName,
#                                          Line_ACTION_PRESS_NAME)

class LineImpl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
#        self.selectable = {}
#        self.actions    = {}
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
#    def onActionState(self, actionName, state):
#        # Ignore activation.
#        if (state):
#            return
#        # Ignore other actions.
#        if (actionName not in self.actions):
#            return
#        # Report.
#        st = pymjin2.State()
#        key = "Line.{0}.selected".format(self.actions[actionName])
#        st.set(key, "1")
#        self.senv.reportStateChange(st)
#        st.set(key, "0")
#        self.senv.reportStateChange(st)
#    def onSelection(self, sceneName, nodeName):
#        node = sceneName + "." + nodeName
#        if (node not in self.selectable):
#            return
#        bs = self.selectable[node]
#        st = pymjin2.State()
#        st.set("{0}.node".format(bs.press), node)
#        st.set("{0}.active".format(bs.press), "1")
#        self.action.setState(st)
#    def setSelectable(self, sceneName, nodeName, state):
#        node = sceneName + "." + nodeName
#        if (state):
#            key = "{0}.{1}.{2}.clone".format(Line_ACTION_PRESS_TYPE,
#                                             Line_ACTION_GROUP,
#                                             Line_ACTION_PRESS_NAME)
#            st = self.action.state([key])
#            newGroupName = st.value(key)[0]
#            bs = LineState()
#            self.selectable[node] = bs
#            bs.setActionGroup(newGroupName)
#            self.actions[bs.down] = node
#        # Remove disabled.
#        elif (node in self.selectable):
#            bs = self.selectable[node]
#            del self.actions[bs.down]
#            del self.selectable[node]

class LineListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            print "Line", k, st.value(k)
#            actionName = k.replace(".active", "")
#            state = (st.value(k)[0] == "1")
#            self.impl.onActionState(actionName, state)

class LineExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self, impl):
        pymjin2.Extension.__init__(self)
        # Refer.
        self.impl = impl
    def deinit(self):
        # Derefer.
        self.impl = None
        print "LineExt.deinit"
    def description(self):
        return "Turn any node into a simple line"
    def keys(self):
        return ["line...enabled",
                "line...moving",
                "line...stepd"]
    def name(self):
        return "LineExtensionScriptEnvironment"
    def set(self, key, value):
        print "Line.set({0}, {1})".format(key, value)
#        v = key.split(".")
#        sceneName = v[1]
#        nodeName  = v[2]
#        self.impl.setSelectable(sceneName, nodeName, value == "1")

class Line:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl              = LineImpl(scene, action, scriptEnvironment)
        self.listenerAction    = LineListenerAction(self.impl)
        self.extension         = LineExtensionScriptEnvironment(self.impl)
        # Prepare.
        # Listen to Line down state.
#        key = "{0}..{1}.active".format(Line_ACTION_DOWN_TYPE,
#                                       Line_ACTION_DOWN_NAME)
#        self.action.addListener([key], self.listenerAction)
        self.senv.addExtension(self.extension)
        print "{0} Line.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.action.removeListener(self.listenerAction)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.listenerAction
        del self.extension
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Line.__del__".format(id(self))

