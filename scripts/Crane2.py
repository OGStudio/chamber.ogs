
import pymjin2

CRANE2_ARMS_BASE_POSTFIX = "_arms_base"

CRANE2_MOVE_DOWN         = "moveBy.default.moveCraneDown"
CRANE2_MOVE_LEFT         = "moveBy.default.moveBeltLeft"
CRANE2_MOVE_RIGHT        = "moveBy.default.moveBeltRight"
CRANE2_MOVE_UP           = "moveBy.default.moveCraneUp"

CRANE2_DEFAULT_STEP_V    = 1
CRANE2_STEPS_H           = 3
CRANE2_STEPS_V           = 3

class Crane2Impl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
        self.enabled = {}
        # State.
        self.isMoving = False
        self.stepV    = CRANE2_DEFAULT_STEP_V
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
    def onActionState(self, actionName, state):
        pass
    def setEnabled(self, sceneName, nodeName, state):
        # Make sure scene exists.
        if (sceneName not in self.enabled):
            self.enabled[sceneName] = {}
        if (state):
            self.enabled[sceneName][nodeName] = True
            # TODO: clone actions.
            st = pymjin2.State()
            # Setup main node.
            craneName = sceneName + "." + nodeName
            st.set("{0}.node".format(CRANE2_MOVE_DOWN), craneName)
            st.set("{0}.node".format(CRANE2_MOVE_UP),   craneName)
            # Setup child node.
#            craneArmsBaseName = sceneName + "." + craneArmsBase
#            st.set("{0}.node".format(CRANE_MOVE_LEFT),  craneArmsBaseName)
#            st.set("{0}.node".format(CRANE_MOVE_RIGHT), craneArmsBaseName)
            self.action.setState(st)
        # Remove disabled.
#        elif (nodeName in self.selectable[sceneName]):
#            actionDownName = self.selectable[sceneName][nodeName]["down"]
#            del self.actions[actionDownName]
#            del self.selectable[sceneName][nodeName]
    def setStepDV(self, sceneName, nodeName, value):
        print "Crane2Impl.setStepDV", nodeName, value

class Crane2ListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            print k, st.value(k)
#            actionName = k.replace(".active", "")
#            state = (st.value(k)[0] == "1")
#            self.impl.onActionState(actionName, state)

class Crane2ExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self, impl):
        pymjin2.Extension.__init__(self)
        # Refer.
        self.impl = impl
    def deinit(self):
        # Derefer.
        self.impl = None
        print "Crane2Ext.deinit"
    def description(self):
        return "Turn any node into a simple Crane2"
    def get(self, st, key):
        print "Crane2.get({0})".format(key)
    def keys(self):
        return ["crane...enabled",
                "crane...moving",
                "crane...stepdh",
                "crane...stepdv",
                "crane...stepdd"]
    def name(self):
        return "Crane2ExtensionScriptEnvironment"
    def set(self, key, value):
        print "Crane2.set({0}, {1})".format(key, value)
        v = key.split(".")
        sceneName = v[1]
        nodeName  = v[2]
        property  = v[3]
        if (property == "enabled"):
            self.impl.setEnabled(sceneName, nodeName, value == "1")
        elif (property == "stepdv"):
            self.impl.setStepDV(sceneName, nodeName, int(value))

class Crane2:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl              = Crane2Impl(scene, action, scriptEnvironment)
        self.listenerAction    = Crane2ListenerAction(self.impl)
        self.extension         = Crane2ExtensionScriptEnvironment(self.impl)
        # Prepare.
#        key = "selector..selectedNode"
#        self.scene.addListener([key], self.listenerSelection)
        # Listen to Crane2 down state.
#        key = "{0}..{1}.active".format(Crane2_ACTION_DOWN_TYPE,
#                                       Crane2_ACTION_DOWN_NAME)
#        self.action.addListener([key], self.listenerAction)
        self.senv.addExtension(self.extension)
        print "{0} Crane2.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.action.removeListener(self.listenerAction)
        #self.scene.removeListener(self.listenerSelection)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.listenerAction
        del self.extension
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Crane2.__del__".format(id(self))

