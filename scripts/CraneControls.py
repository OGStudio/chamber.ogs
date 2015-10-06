
import pymjin2

CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS = "scripts/ControlButtons.py"

class CraneControls:
    def __init__(self, sceneName, nodeName, scene, action, dependencies):
        # Refer.
        self.sceneName    = sceneName
        self.scene        = scene
        self.action       = action
        self.dependencies = dependencies
        # Create.
        module = self.dependencies[CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS]
        self.controlButtons = module.ControlButtons(sceneName, nodeName, scene, action)
        # Prepare.
    def __del__(self):
        # Tear down.
        # Destroy.
        del self.controlButtons
        # Derefer.
        self.scene        = None
        self.action       = None
        self.dependencies = None

def SCRIPT_CREATE(sceneName, nodeName, scene, action, dependencies):
    return CraneControls(sceneName, nodeName, scene, action, dependencies)

def SCRIPT_DEPENDENCIES():
    return [CRANE_CONTROLS_DEPENDENCY_CONTROL_BUTTONS]

def SCRIPT_DESTROY(instance):
    del instance

