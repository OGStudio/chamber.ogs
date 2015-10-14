
import pymjin2

#Control_ARMS_BASE_POSTFIX = "_arms_base"
#
#Control_MOVE_DOWN         = "moveBy.default.moveCraneDown"
#Control_MOVE_LEFT         = "moveBy.default.moveBeltLeft"
#Control_MOVE_RIGHT        = "moveBy.default.moveBeltRight"
#Control_MOVE_UP           = "moveBy.default.moveCraneUp"
#
#Control_DEFAULT_STEP_V    = 1
#Control_STEPS_H           = 3
#Control_STEPS_V           = 3

class ControlImpl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
    def onActionState(self, actionName, state):
        pass

class ControlListenerAction(pymjin2.ComponentListener):
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

class ControlExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self, impl):
        pymjin2.Extension.__init__(self)
        # Refer.
        self.impl = impl
    def deinit(self):
        # Derefer.
        self.impl = None
        print "ControlExt.deinit"
    def description(self):
        return "Turn any node into a simple Control"
    def keys(self):
        return ["control...enabled",
                "crane...moving",
                "crane...stepH",
                "crane...stepV",
                "crane...stepD"]
    def name(self):
        return "ControlExtensionScriptEnvironment"
    def set(self, key, value):
        print "Control.set({0}, {1})".format(key, value)
        v = key.split(".")
        sceneName = v[1]
        nodeName  = v[2]
        property  = v[3]
        if (property == "enabled"):
            self.impl.setEnabled(sceneName, nodeName, value == "1")
        elif (property == "stepV"):
            self.impl.setStepV(sceneName, nodeName, int(value))

class Control:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl              = ControlImpl(scene, action, scriptEnvironment)
        self.listenerAction    = ControlListenerAction(self.impl)
        self.extension         = ControlExtensionScriptEnvironment(self.impl)
        # Prepare.
#        key = "selector..selectedNode"
#        self.scene.addListener([key], self.listenerSelection)
        # Listen to Control down state.
#        key = "{0}..{1}.active".format(Control_ACTION_DOWN_TYPE,
#                                       Control_ACTION_DOWN_NAME)
#        self.action.addListener([key], self.listenerAction)
        self.senv.addExtension(self.extension)
        print "{0} Control.__init__".format(id(self))
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
        print "{0} Control.__del__".format(id(self))

