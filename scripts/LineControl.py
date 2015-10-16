
import pymjin2

LINE_CONTROL_BUTTON_POSTFIX_DOWN  = "Down"
LINE_CONTROL_BUTTON_POSTFIX_LEFT  = "Left"
LINE_CONTROL_BUTTON_POSTFIX_RIGHT = "Right"
LINE_CONTROL_BUTTON_POSTFIX_UP    = "Up"

#LINE_CONTROLLineControl_CRANE_NAME           = "crane_base"

#LineControl_SIGNAL_MATERIAL_OFF  = "LineControl_signal_off"
#LineControl_SIGNAL_MATERIAL_ON   = "LineControl_signal_on"
#LineControl_SIGNAL_POSTFIX       = "Signal"

class LineControlState(object):
    def __init__(self):
        self.up     = None
        self.down   = None
        self.right  = None
        self.left   = None
        #self.signal = None

class LineControlImpl(object):
    def __init__(self, scene, senv):
        # Refer.
        self.scene = scene
        self.senv  = senv
        # Create.
        #self.cs = LineControlState()
    def __del__(self):
        # Derefer.
        self.scene = None
        self.senv  = None
#    def enableButtons(self, sceneName):
#        st = pymjin2.State()
#        buttons = [self.cs.up, self.cs.down, self.cs.right, self.cs.left]
#        for b in buttons:
#            key = "button.{0}.{1}.selectable".format(sceneName, b)
#            st.set(key, "1")
#        self.senv.setState(st)
#    def onButtonPress(self, sceneName, nodeName):
#        craneStepV = 0
#        if (nodeName == self.cs.down):
#            craneStepV = 1
#        elif (nodeName == self.cs.up):
#            craneStepV = -1
#        elif (nodeName == self.cs.left):
#            craneStepH = -1
#        elif (nodeName == self.cs.right):
#            craneStepH = 1
#        if (craneStepV):
#            st = pymjin2.State()
#            key = "crane.{0}.{1}.stepdv".format(sceneName, LineControl_CRANE_NAME)
#            st.set(key, str(craneStepV))
#            self.senv.setState(st)
#        elif (craneStepH):
#            st = pymjin2.State()
#            key = "crane.{0}.{1}.stepdh".format(sceneName, LineControl_CRANE_NAME)
#            st.set(key, str(craneStepH))
#            self.senv.setState(st)
#    def onCraneMotion(self, sceneName, state):
#        mat = LineControl_SIGNAL_MATERIAL_OFF
#        if (state):
#            mat = LineControl_SIGNAL_MATERIAL_ON
#        key = "node.{0}.{1}.material".format(sceneName, self.cs.signal)
#        st = pymjin2.State()
#        st.set(key, mat)
#        self.scene.setState(st)
#    def resolveButtons(self, sceneName, nodeName):
#        key = "node.{0}.{1}.children".format(sceneName, nodeName)
#        st = self.scene.state([key])
#        if (not len(st.keys)):
#            print "Could not resolve buttons"
#            return
#        children = st.value(key)
#        for c in children:
#            if (c.endswith(LineControl_BUTTON_POSTFIX_DOWN)):
#                self.cs.down = c
#            elif (c.endswith(LineControl_BUTTON_POSTFIX_LEFT)):
#                self.cs.left = c
#            elif (c.endswith(LineControl_BUTTON_POSTFIX_RIGHT)):
#                self.cs.right = c
#            elif (c.endswith(LineControl_BUTTON_POSTFIX_UP)):
#                self.cs.up = c
#            elif (c.endswith(LineControl_SIGNAL_POSTFIX)):
#                self.cs.signal = c

class LineControlListenerScriptEnvironment(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            print "LineControl", k, st.value(k)
#            v = k.split(".")
#            type      = v[0]
#            sceneName = v[1]
#            nodeName  = v[2]
#            #property = v[3]
#            value     = st.value(k)[0]
#            if (type == "button"):
#                if (value == "1"):
#                    self.impl.onButtonPress(sceneName, nodeName)
#            elif (type == "crane"):
#                self.impl.onCraneMotion(sceneName, value == "1")

class LineControl:
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
        self.impl         = LineControlImpl(scene, scriptEnvironment)
        self.listenerSEnv = LineControlListenerScriptEnvironment(self.impl)
        # Prepare.
#        self.impl.resolveButtons(sceneName, nodeName)
#        self.impl.enableButtons(sceneName)
#        # Listen to buttons' down state.
#        keys = []
#        buttons = [self.impl.cs.up,
#                   self.impl.cs.down,
#                   self.impl.cs.right,
#                   self.impl.cs.left]
#        for b in buttons:
#            key = "button.{0}.{1}.selected".format(sceneName, b)
#            keys.append(key)
#        # Listen to crane motion.
#        key = "crane.{0}.{1}.moving".format(sceneName, LineControl_CRANE_NAME)
#        keys.append(key)
#        self.senv.addListener(keys, self.listenerSEnv)
        print "{0} LineControl.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.senv.removeListener(self.listenerSEnv)
        # Destroy.
        del self.listenerSEnv
        del self.impl
        # Derefer.
        self.senv = None
        print "{0} LineControl.__del__".format(id(self))

def SCRIPT_CREATE(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies):
    return LineControl(sceneName,
                   nodeName,
                   scene,
                   action,
                   scriptEnvironment,
                   dependencies)

def SCRIPT_DEPENDENCIES():
    return []

def SCRIPT_DESTROY(instance):
    del instance
