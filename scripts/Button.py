
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
    def __init__(self, impl, sceneName, nodeName):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl      = impl
        self.sceneName = sceneName
        self.nodeName  = nodeName
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            nodeName = st.value(k)[0]
            # Ignore other nodes.
            if (nodeName != self.nodeName):
                continue
            v = k.split(".")
            sceneName = v[1]
            # Ignore other scenes.
            if (sceneName != self.sceneName):
                continue
            self.impl.onSelection(sceneName, nodeName)

class Button:
    def __init__(self,
                 sceneName,
                 nodeName,
                 scene,
                 action,
                 scriptEnvironment,
                 dependencies):
        # Refer.
        self.sceneName = sceneName
        self.scene     = scene
        self.action    = action
        self.senv      = scriptEnvironment
        #self.dependencies = dependencies
        # Create.
        self.impl              = ButtonImpl(scene, action)
        self.listenerSelection = ButtonListenerSelection(self.impl,
                                                         sceneName,
                                                         nodeName)
#        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CRANE_LIFT]
#        self.craneLift = module.CraneLift(sceneName, nodeName, scene, action)
#        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS]
#        self.controlButtons = module.ControlButtons(sceneName, nodeName, scene, action)
#        # Prepare.
#        self.controlButtons.addListener(self)
#        self.craneLift.addListener(self)
        key = "selector.{0}.selectedNode".format(sceneName)
        self.scene.addListener([key], self.listenerSelection)
#        # Postfixes.
#        self.buttonPostfixDown  = module.CONTROL_BUTTONS_POSTFIX_DOWN
#        self.buttonPostfixUp    = module.CONTROL_BUTTONS_POSTFIX_UP
        print "{0} Button.__init__({0}, {1})".format(id(self), sceneName, nodeName)
    def __del__(self):
        # Tear down.
        self.scene.removeListener(self.listenerSelection)
#        self.controlButtons.removeListener(self)
#        self.craneLift.removeListener(self)
        # Destroy.
#        del self.controlButtons
#        del self.craneLift
        del self.listenerSelection
        del self.impl
        # Derefer.
        self.scene        = None
        self.action       = None
        self.senv         = None
        #self.dependencies = None
        print "{0} Button.__del__".format(id(self))

def SCRIPT_CREATE(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies):
    return Button(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies)

def SCRIPT_DEPENDENCIES():
    return []

def SCRIPT_DESTROY(instance):
    del instance

