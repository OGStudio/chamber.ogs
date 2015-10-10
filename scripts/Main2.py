
import pymjin2

MAIN2_DEPENDENCY_BUTTON = "scripts/Button.py"

class Main2:
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
        module = self.dependencies[MAIN2_DEPENDENCY_BUTTON]
        self.button = module.Button(scene, action, scriptEnvironment)
        # Prepare.
        print "{0} Main2.__init__({1}, {2})".format(id(self), sceneName, nodeName)
    def __del__(self):
        # Derefer.
        self.scene        = None
        self.action       = None
        self.senv         = None
        self.dependencies = None
        # Destroy
        del self.button
        print "{0} Main2.__del__".format(id(self))

def SCRIPT_CREATE(sceneName,
                  nodeName,
                  scene,
                  action,
                  scriptEnvironment,
                  dependencies):
    return Main2(sceneName,
                 nodeName,
                 scene,
                 action,
                 scriptEnvironment,
                 dependencies)

def SCRIPT_DEPENDENCIES():
    return [MAIN2_DEPENDENCY_BUTTON]

def SCRIPT_DESTROY(instance):
    del instance

