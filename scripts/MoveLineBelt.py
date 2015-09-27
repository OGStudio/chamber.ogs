
import pymjin2

class MoveBeltListenerScene(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        self.impl = impl
    def __del__(self):
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            value = st.value(k)[0]
            if (value == "moveBeltLeft"):
                print "MOVE BELT LEFT"
            elif (value == "moveBeltRight"):
                print "MOVE BELT RIGHT"

class MoveBelt:
    def __init__(self, sceneName, nodeName, scene, action):
        print "MoveBelt({0}). START. scene: {1} node: {2}".format(
            id(self),
            sceneName,
            nodeName)
        # Refer.
        self.sceneName = sceneName
        self.nodeName  = nodeName
        self.scene     = scene
        # Create.
        self.listenerScene = MoveBeltListenerScene(None)
        # Prepare.
        key = "selector.{0}.selectedNode".format(sceneName)
        self.scene.addListener([key], self.listenerScene)
    def __del__(self):
        # Tear down.
        self.scene.removeListener(self.listenerScene)
        # Destroy.
        del self.listenerScene
        # Derefer.
        self.scene = None
        print "MoveBelt({0}). FINISH. scene: {1} node: {2}".format(
            id(self),
            self.sceneName,
            self.nodeName)

def SCRIPT_CREATE(sceneName, nodeName, scene, action):
    return MoveBelt(sceneName, nodeName, scene, action)

def SCRIPT_DESTROY(instance):
    del instance

