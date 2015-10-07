
import pymjin2

CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS = "scripts/ControlButtons.py"
CRANE_CONTROLS_DEPENDENCY_CRANE           = "scripts/Crane.py"
CRANE_CONTROLS_SIGNAL                     = "craneControlSignal"
CRANE_CONTROLS_SIGNAL_MATERIAL_ON         = "control_signal_on"
CRANE_CONTROLS_SIGNAL_MATERIAL_OFF        = "control_signal_off"

class CraneControls:
    def __init__(self, sceneName, nodeName, scene, action, dependencies):
        # Refer.
        self.sceneName    = sceneName
        self.scene        = scene
        self.action       = action
        self.dependencies = dependencies
        # Create.
        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CRANE]
        self.crane = module.Crane(sceneName, nodeName, scene, action)
        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS]
        self.controlButtons = module.ControlButtons(sceneName, nodeName, scene, action)
        # Prepare.
        self.controlButtons.addListener(self)
        self.crane.addListener(self)
        # Postfixes.
        self.buttonPostfixDown  = module.CONTROL_BUTTONS_POSTFIX_DOWN
        self.buttonPostfixLeft  = module.CONTROL_BUTTONS_POSTFIX_LEFT
        self.buttonPostfixRight = module.CONTROL_BUTTONS_POSTFIX_RIGHT
        self.buttonPostfixUp    = module.CONTROL_BUTTONS_POSTFIX_UP
    def __del__(self):
        # Tear down.
        self.controlButtons.removeListener(self)
        self.crane.removeListener(self)
        # Destroy.
        del self.controlButtons
        del self.crane
        # Derefer.
        self.scene        = None
        self.action       = None
        self.dependencies = None
    def onControlButtonsExecute(self, sceneName, nodeName):
        print "onControlButtonsExecute", sceneName, nodeName
        if (nodeName.endswith(self.buttonPostfixUp)):
            self.crane.moveUp(True)
        elif (nodeName.endswith(self.buttonPostfixDown)):
            self.crane.moveUp(False)
        elif (nodeName.endswith(self.buttonPostfixLeft)):
            self.crane.moveRight(False)
        elif (nodeName.endswith(self.buttonPostfixRight)):
            self.crane.moveRight(True)
    def onCraneMove(self, state):
        self.setSignalState(state)
    def setSignalState(self, state):
        mat = CRANE_CONTROLS_SIGNAL_MATERIAL_OFF
        if (state):
            mat = CRANE_CONTROLS_SIGNAL_MATERIAL_ON
        st = pymjin2.State()
        key = "node.{0}.{1}.material".format(self.sceneName,
                                             CRANE_CONTROLS_SIGNAL)
        st.set(key, mat)
        self.scene.setState(st)

def SCRIPT_CREATE(sceneName, nodeName, scene, action, dependencies):
    return CraneControls(sceneName, nodeName, scene, action, dependencies)

def SCRIPT_DEPENDENCIES():
    return [CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS,
            CRANE_CONTROLS_DEPENDENCY_CRANE]

def SCRIPT_DESTROY(instance):
    del instance

