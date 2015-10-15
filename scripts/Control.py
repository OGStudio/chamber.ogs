
import pymjin2

CONTROL_BUTTON_POSTFIX_DOWN  = "Down"
CONTROL_BUTTON_POSTFIX_LEFT  = "Left"
CONTROL_BUTTON_POSTFIX_RIGHT = "Right"
CONTROL_BUTTON_POSTFIX_UP    = "Up"

CONTROL_CRANE_NAME           = "crane_base"

CONTROL_SIGNAL_MATERIAL_OFF  = "control_signal_off"
CONTROL_SIGNAL_MATERIAL_ON   = "control_signal_on"
CONTROL_SIGNAL_POSTFIX       = "Signal"

class ControlImpl(object):
    def __init__(self, sceneName, scene, senv):
        # Refer.
        self.scene     = scene
        self.senv      = senv
        self.sceneName = sceneName
        # Create.
        self.buttons = { "down" : None,
                         "left" : None,
                        "right" : None,
                           "up" : None }
        self.signal = None
    def __del__(self):
        # Derefer.
        self.scene = None
        self.senv  = None
    def enableButtons(self):
        st = pymjin2.State()
        for type, value in self.buttons.items():
            key = "button..{0}.selectable".format(value)
            st.set(key, "1")
        self.senv.setState(st)
    def onButtonPress(self, nodeName):
        print "onButtonPress", nodeName
        craneStepVDiff = 0
        if (nodeName == self.buttons["down"]):
            craneStepVDiff = 1
        elif (nodeName == self.buttons["up"]):
            craneStepVDiff = -1
#        elif (nodeName == self.buttons["left"]):
#            print "left"
#        elif (nodeName == self.buttons["right"]):
#            print "right"
        if (craneStepVDiff):
            print "crane step V diff:", craneStepVDiff
            st = pymjin2.State()
            key = "crane.{0}.{1}.stepdv".format(self.sceneName, CONTROL_CRANE_NAME)
            st.set(key, str(craneStepVDiff))
            self.senv.setState(st)
    def onCraneMotion(self, sceneName, state):
        print "onCraneMotion", state
        mat = CONTROL_SIGNAL_MATERIAL_OFF
        if (state):
            mat = CONTROL_SIGNAL_MATERIAL_ON
        key = "node.{0}.{1}.material".format(sceneName, self.signal)
        st = pymjin2.State()
        st.set(key, mat)
        self.scene.setState(st)
    def resolveButtons(self, sceneName, nodeName):
        key = "node.{0}.{1}.children".format(sceneName, nodeName)
        st = self.scene.state([key])
        if (not len(st.keys)):
            print "Could not resolve buttons"
            return
        children = st.value(key)
        for c in children:
            if (c.endswith(CONTROL_BUTTON_POSTFIX_DOWN)):
                self.buttons["down"] = c
            elif (c.endswith(CONTROL_BUTTON_POSTFIX_LEFT)):
                self.buttons["left"] = c
            elif (c.endswith(CONTROL_BUTTON_POSTFIX_RIGHT)):
                self.buttons["right"] = c
            elif (c.endswith(CONTROL_BUTTON_POSTFIX_UP)):
                self.buttons["up"] = c
            elif (c.endswith(CONTROL_SIGNAL_POSTFIX)):
                self.signal = c

class ControlListenerScriptEnvironment(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            v = k.split(".")
            type      = v[0]
            sceneName = v[1]
            nodeName  = v[2]
            #property = v[3]
            value     = st.value(k)[0]
            if (type == "button"):
                if (value == "1"):
                    self.impl.onButtonPress(nodeName)
            elif (type == "crane"):
                self.impl.onCraneMotion(sceneName, value == "1")

class Control:
    def __init__(self,
                 sceneName,
                 nodeName,
                 scene,
                 action,
                 scriptEnvironment,
                 dependencies):
        # Refer.
        self.senv = scriptEnvironment
        # Create.
        self.impl         = ControlImpl(sceneName, scene, scriptEnvironment)
        self.listenerSEnv = ControlListenerScriptEnvironment(self.impl)
        # Prepare.
        self.impl.resolveButtons(sceneName, nodeName)
        self.impl.enableButtons()
        # Listen to buttons' down state.
        keys = []
        for type, value in self.impl.buttons.items():
            key = "button.{0}.{1}.selected".format(sceneName, value)
            keys.append(key)
        # Listen to crane motion.
        key = "crane.{0}.{1}.moving".format(sceneName, CONTROL_CRANE_NAME)
        keys.append(key)
        self.senv.addListener(keys, self.listenerSEnv)
        print "{0} Control.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.senv.removeListener(self.listenerSEnv)
        # Destroy.
        del self.listenerSEnv
        del self.impl
        # Derefer.
        self.senv = None
        print "{0} Control.__del__".format(id(self))

def SCRIPT_CREATE(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies):
    return Control(sceneName,
                   nodeName,
                   scene,
                   action,
                   scriptEnvironment,
                   dependencies)

def SCRIPT_DEPENDENCIES():
    return []

def SCRIPT_DESTROY(instance):
    del instance
