
import pymjin2

MAIN2_DEPENDENCY_BUTTON = "scripts/Button.py"
MAIN2_DEPENDENCY_CRANE  = "scripts/Crane2.py"

MAIN2_BUTTON_CRANE_STEP_V_DEC = "seControlDown"
MAIN2_BUTTON_CRANE_STEP_V_INC = "seControlUp"
MAIN2_BUTTON_CRANE_STEP_H_DEC = "seControlLeft"
MAIN2_BUTTON_CRANE_STEP_H_INC = "seControlRight"
MAIN2_CRANE                   = "crane_base"

class Main2ListenerScriptEnvironment(pymjin2.ComponentListener):
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
        self.listenerSEnv = Main2ListenerScriptEnvironment(None)
        module = self.dependencies[MAIN2_DEPENDENCY_CRANE]
        self.crane = module.Crane2(scene, action, scriptEnvironment)
        # Prepare.
        # Mark crane buttons selectable.
        buttons = [MAIN2_BUTTON_CRANE_STEP_V_DEC,
                   MAIN2_BUTTON_CRANE_STEP_V_INC,
                   MAIN2_BUTTON_CRANE_STEP_H_DEC,
                   MAIN2_BUTTON_CRANE_STEP_H_INC]
        st = pymjin2.State()
        for b in buttons:
            key = "button.{0}.{1}.selectable".format(sceneName, b)
            st.set(key, "1")
        # Enable crane.
        key = "crane.{0}.{1}.enabled".format(sceneName, MAIN2_CRANE)
        st.set(key, "1")
        self.senv.setState(st)
        # Listen to button selection.
        self.senv.addListener(["button...selected"], self.listenerSEnv)
        print "{0} Main2.__init__({1}, {2})".format(id(self), sceneName, nodeName)
    def __del__(self):
        # Tear down.
        self.senv.removeListener(self.listenerSEnv)
        # Derefer.
        self.scene        = None
        self.action       = None
        self.senv         = None
        self.dependencies = None
        # Destroy
        del self.button
        del self.crane
        del self.listenerSEnv
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
    return [MAIN2_DEPENDENCY_BUTTON,
            MAIN2_DEPENDENCY_CRANE]

def SCRIPT_DESTROY(instance):
    del instance

