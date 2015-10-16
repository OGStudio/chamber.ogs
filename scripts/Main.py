
import pymjin2

MAIN_DEPENDENCY_BUTTON = "scripts/Button.py"
MAIN_DEPENDENCY_CRANE  = "scripts/Crane.py"
MAIN_DEPENDENCY_LINE   = "scripts/Line.py"

MAIN_CRANE             = "crane_base"
MAIN_LINES             = ["lineBelt1", "lineBelt2", "lineBelt3"]

class MainListenerScriptEnvironment(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            print "Main", k, st.value(k)

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
        self.listenerSEnv = MainListenerScriptEnvironment(None)
        module = self.dependencies[MAIN_DEPENDENCY_CRANE]
        self.crane = module.Crane(scene, action, scriptEnvironment)
        module = self.dependencies[MAIN_DEPENDENCY_LINE]
        self.line = module.Line(scene, action, scriptEnvironment)
        # Prepare.
        st = pymjin2.State()
        # Enable crane.
        key = "crane.{0}.{1}.enabled".format(sceneName, MAIN_CRANE)
        st.set(key, "1")
        # Enable lines.
        for l in MAIN_LINES:
            key = "line.{0}.{1}.enabled".format(sceneName, l)
            st.set(key, "1")
        self.senv.setState(st)
        # Listen to button selection.
        #self.senv.addListener(["button...selected"], self.listenerSEnv)
        print "{0} Main.__init__({1}, {2})".format(id(self), sceneName, nodeName)
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

