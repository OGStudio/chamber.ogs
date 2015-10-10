
import pymjin2

#CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS = "scripts/ControlButtons.py"
#CRANE_CONTROLS_DEPENDENCY_CRANE_LIFT      = "scripts/CraneLift.py"
#CRANE_PISTON_SIGNAL                       = "pistonControlSignal"
#CRANE_CONTROLS_SIGNAL_MATERIAL_ON         = "control_signal_on"
#CRANE_CONTROLS_SIGNAL_MATERIAL_OFF        = "control_signal_off"

class ButtonImpl(object):
    def __init__(self, scene, action):#, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        #self.listeners = listeners
        # State.
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        #self.listeners = None
    def onSelection(self, sceneName, nodeName):
        print "onSelection", sceneName, nodeName

class ButtonListenerSelection(pymjin2.ComponentListener):
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
#            nodeName = st.value(k)[0]
#            # Ignore other nodes.
#            if (nodeName != self.nodeName):
#                continue
#            v = k.split(".")
#            sceneName = v[1]
#            # Ignore other scenes.
#            if (sceneName != self.sceneName):
#                continue
#            self.impl.onSelection(sceneName, nodeName)

class ButtonExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self):
        pymjin2.Extension.__init__(self)
    def deinit(self):
        print "ButtonExt.deinit"
    def description(self):
        return "Turn any node into a simple button"
    def keys(self):
        return ["button...selectable",
                "button...selected"]
    def name(self):
        return "ButtonExtensionScriptEnvironment"
    def set(self, key, value):
        print "ButtonExt.set", key, value

class Button:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl              = ButtonImpl(scene, action)
        self.listenerSelection = ButtonListenerSelection(self.impl)
        self.extension         = ButtonExtensionScriptEnvironment()
        # Prepare.
        key = "selector..selectedNode"
        self.scene.addListener([key], self.listenerSelection)
        self.senv.addExtension(self.extension)
        print "{0} Button.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.scene.removeListener(self.listenerSelection)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.listenerSelection
        del self.impl
        del self.extension
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Button.__del__".format(id(self))

