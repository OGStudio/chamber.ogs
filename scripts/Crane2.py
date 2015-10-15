
import pymjin2

CRANE2_ARMS_BASE_POSTFIX = "_arms_base"

CRANE2_MOVE_DOWN         = "moveBy.default.moveCraneDown"
CRANE2_MOVE_LEFT         = "moveBy.default.moveBeltLeft"
CRANE2_MOVE_RIGHT        = "moveBy.default.moveBeltRight"
CRANE2_MOVE_UP           = "moveBy.default.moveCraneUp"

CRANE2_DEFAULT_STEP_V    = 1
CRANE2_STEPS_H           = 3
CRANE2_STEPS_V           = 3

class Crane2State(object):
    def __init__(self):
        self.up       = CRANE2_MOVE_UP
        self.down     = CRANE2_MOVE_DOWN
        self.isMoving = False
        self.stepV    = CRANE2_DEFAULT_STEP_V
    def validateNewStepV(self, value):
        newStepV = self.stepV + value
        ok = (newStepV >= 0) and (newStepV < CRANE2_STEPS_V)
        if (ok):
            self.stepV = newStepV
        return ok

class Crane2Impl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
        self.actions = {}
        self.enabled = {}
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
    def onActionState(self, actionName, state):
        # Ignore activation.
        if (state):
            return
        # Ignore other actions.
        if (actionName not in self.actions):
            return
        node = self.actions[actionName]
        cs = self.enabled[node]
        cs.isMoving = False
        # Report !isMoving.
        st = pymjin2.State()
        key = "crane.{0}.moving".format(node)
        st.set(key, "0")
        self.senv.reportStateChange(st)
    def setEnabled(self, sceneName, nodeName, state):
        if (state):
            st = pymjin2.State()
            # Setup main node.
            node = sceneName + "." + nodeName
            st.set("{0}.node".format(CRANE2_MOVE_DOWN), node)
            st.set("{0}.node".format(CRANE2_MOVE_UP),   node)
            # Setup child node.
#            craneArmsBaseName = sceneName + "." + craneArmsBase
#            st.set("{0}.node".format(CRANE_MOVE_LEFT),  craneArmsBaseName)
#            st.set("{0}.node".format(CRANE_MOVE_RIGHT), craneArmsBaseName)
            self.action.setState(st)
            cs = Crane2State()
            self.enabled[node] = cs
            self.actions[cs.down] = node
            self.actions[cs.up]   = node
        # Remove disabled.
        elif (node in self.enabled):
            cs = self.enabled[node]
            del self.actions[cs.down]
            del self.actions[cs.up]
            del self.enabled[node]
    def setStepDV(self, sceneName, nodeName, value):
        node = sceneName + "." + nodeName
        cs = self.enabled[node]
        if (cs.isMoving):
            return
        if (not cs.validateNewStepV(value)):
            return
        cs.isMoving = True
        # Start the action.
        st = pymjin2.State()
        key = "{0}.active".format(cs.up if value < 0 else cs.down)
        st.set(key, "1")
        self.action.setState(st)
        # Report isMoving.
        st = pymjin2.State()
        key = "crane.{0}.moving".format(node)
        st.set(key, "1")
        self.senv.setState(st)

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
            actionName = k.replace(".active", "")
            state = (st.value(k)[0] == "1")
            self.impl.onActionState(actionName, state)

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
        #print "Crane2.set({0}, {1})".format(key, value)
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
        # Listen to Crane2.
        # TODO: update actions after cloning.
        keys = ["{0}.active".format(CRANE2_MOVE_UP),
                "{0}.active".format(CRANE2_MOVE_DOWN)]
        self.action.addListener(keys, self.listenerAction)
        self.senv.addExtension(self.extension)
        print "{0} Crane2.__init__".format(id(self))
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
        print "{0} Crane2.__del__".format(id(self))

