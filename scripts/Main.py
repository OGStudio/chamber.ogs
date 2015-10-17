
import pymjin2

MAIN_DEPENDENCY_BUTTON = "scripts/Button.py"
MAIN_DEPENDENCY_CRANE  = "scripts/Crane.py"
MAIN_DEPENDENCY_LINE   = "scripts/Line.py"

class Main:
    def __init__(self,
                 sceneName,
                 nodeName,
                 scene,
                 action,
                 scriptEnvironment,
                 dependencies):
        # Refer.
        self.sceneName    = sceneName
        self.scene        = scene
        self.action       = action
        self.senv         = scriptEnvironment
        self.dependencies = dependencies
        # Create.
        module = self.dependencies[MAIN_DEPENDENCY_BUTTON]
        self.button = module.Button(scene, action, scriptEnvironment)
        module = self.dependencies[MAIN_DEPENDENCY_CRANE]
        self.crane = module.Crane(scene, action, scriptEnvironment)
        module = self.dependencies[MAIN_DEPENDENCY_LINE]
        self.line = module.Line(scene, action, scriptEnvironment)
        # Prepare.
        print "{0} Main.__init__({1}, {2})".format(id(self), sceneName, nodeName)
    def __del__(self):
        # Tear down.
        # Derefer.
        self.scene        = None
        self.action       = None
        self.senv         = None
        self.dependencies = None
        # Destroy
        del self.button
        del self.crane
        del self.line
        del self.listenerSEnv
        print "{0} Main.__del__".format(id(self))

def SCRIPT_CREATE(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies):
    return Main(sceneName,
                nodeName,
                scene,
                action,
                scriptEnvironment,
                dependencies)

def SCRIPT_DEPENDENCIES():
    return [MAIN_DEPENDENCY_BUTTON,
            MAIN_DEPENDENCY_CRANE,
            MAIN_DEPENDENCY_LINE]

def SCRIPT_DESTROY(instance):
    del instance

