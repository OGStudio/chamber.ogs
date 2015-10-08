
import pymjin2

CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS = "scripts/ControlButtons.py"
CRANE_CONTROLS_DEPENDENCY_CRANE_LIFT      = "scripts/CraneLift.py"
CRANE_PISTON_SIGNAL                       = "pistonControlSignal"
CRANE_CONTROLS_SIGNAL_MATERIAL_ON         = "control_signal_on"
CRANE_CONTROLS_SIGNAL_MATERIAL_OFF        = "control_signal_off"

class CraneControlsLift:
    def __init__(self, sceneName, nodeName, scene, action, dependencies):
        # Refer.
        self.sceneName    = sceneName
        self.scene        = scene
        self.action       = action
        self.dependencies = dependencies
        # Create.
        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CRANE_LIFT]
        self.craneLift = module.CraneLift(sceneName, nodeName, scene, action)
        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS]
        self.controlButtons = module.ControlButtons(sceneName, nodeName, scene, action)
        # Prepare.
        self.controlButtons.addListener(self)
        self.craneLift.addListener(self)
        # Postfixes.
        self.buttonPostfixDown  = module.CONTROL_BUTTONS_POSTFIX_DOWN
        self.buttonPostfixUp    = module.CONTROL_BUTTONS_POSTFIX_UP
    def __del__(self):
        # Tear down.
        self.controlButtons.removeListener(self)
        self.craneLift.removeListener(self)
        # Destroy.
        del self.controlButtons
        del self.craneLift
        # Derefer.
        self.scene        = None
        self.action       = None
        self.dependencies = None
    def onControlButtonsExecute(self, sceneName, nodeName):
        if (nodeName.endswith(self.buttonPostfixUp)):
            self.craneLift.lift(True)
        elif (nodeName.endswith(self.buttonPostfixDown)):
            self.craneLift.lift(False)
    def onCraneLift(self, state):
        self.setSignalState(state)
    def setSignalState(self, state):
        mat = CRANE_CONTROLS_SIGNAL_MATERIAL_OFF
        if (state):
            mat = CRANE_CONTROLS_SIGNAL_MATERIAL_ON
        st = pymjin2.State()
        key = "node.{0}.{1}.material".format(self.sceneName,
                                             CRANE_PISTON_SIGNAL)
        st.set(key, mat)
        self.scene.setState(st)

def SCRIPT_CREATE(sceneName, nodeName, scene, action, scriptEnvironment, dependencies):
    return CraneControlsLift(sceneName, nodeName, scene, action, dependencies)

def SCRIPT_DEPENDENCIES():
    return [CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS,
            CRANE_CONTROLS_DEPENDENCY_CRANE_LIFT]

def SCRIPT_DESTROY(instance):
    del instance

