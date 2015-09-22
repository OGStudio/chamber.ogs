
import pymjin2

class MainImpl(object):
    def __init__(self, scene, action, sceneName, nodeName):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.sceneName = sceneName
        self.nodeName  = nodeName
        #self.actionEnabled = False
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
    def selectNode(self, nodeName):
        print "Main: node selected. BEGIN", nodeName
        if (nodeName == self.nodeName):
            print "Main: PARENT node selected. Do nothing. END", nodeName
            return
#        st = pymjin2.State()
#        key = "node.{0}.{1}.script".format(self.sceneName, nodeName)
#        st.set(key, "scripts/TrackNodeLifeTime.py")
#        self.scene.setState(st)
        print "Main: launching 'fastMain' action"
        st = pymjin2.State()
        st.set("speed.default.fastMain.active", "1")
#        print "Main: changing 'script' property"
#        st.set("script.default.printAnything.script", "scripts/actions/PrintEverything.py")
#        self.action.setState(st)
        print "Main: node selected. END", nodeName

class MainListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        self.impl = impl
    def __del__(self):
        self.impl = None
    def onComponentStateChange(self, st):
        #print "MainListenerAction state change"
        for k in st.keys:
            value = st.value(k)[0]
            print "MainListenerAction", k, value
            #self.impl.selectNode(value)

class MainListenerScene(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        self.impl = impl
    def __del__(self):
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            value = st.value(k)[0]
            self.impl.selectNode(value)

class Main:
    def __init__(self, sceneName, nodeName, scene, action):
        print "Main script started"
        # Refer.
        self.scene  = scene
        self.action = action
        # Create.
        self.impl           = MainImpl(self.scene, action, sceneName, nodeName)
        self.listenerAction = MainListenerAction(None)
        self.listenerScene  = MainListenerScene(self.impl)
        # Prepare.
        key = "selector.{0}.selectedNode".format(sceneName)
        self.scene.addListener([key], self.listenerScene)
        key = "...active"
        self.action.addListener([key], self.listenerAction)
    def __del__(self):
        # Tear down.
        self.scene.removeListener(self.listenerScene)
        self.action.removeListener(self.listenerAction)
        # Destroy.
        del self.listenerScene
        del self.listenerAction
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        print "Main script finished"

def SCRIPT_CREATE(sceneName, nodeName, scene, action):
    return Main(sceneName, nodeName, scene, action)

def SCRIPT_DESTROY(instance):
    del instance

