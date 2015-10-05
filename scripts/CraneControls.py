
import pymjin2

class CraneControlsImpl(object):
    def __init__(self, scene, action):
        # Refer.
        self.scene  = scene
        self.action = action
        # Setup.
        self.moveButtonUp   = "moveBy.default.moveButtonUp"
        self.moveButtonDown = "moveBy.default.moveButtonDown"
        self.pressButtonSeq = "sequence.default.pressButton"
        # State.
        self.buttons = []
        self.canPressButton = True
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
    def onActionState(self, sceneName, actionName, state):
        print "impl.onActionState", actionName, state
        if (not state):
            if (actionName == self.pressButtonSeq):
                self.canPressButton = True
    def onSelection(self, sceneName, nodeName):
        if (nodeName in self.buttons):
            self.pressButton(sceneName, nodeName)
    def pressButton(self, sceneName, nodeName):
        if (not self.canPressButton):
            return
        self.canPressButton = False
        node = sceneName + "." + nodeName
        print "pressButton", node
        st = pymjin2.State()
        key = "{0}.node".format(self.moveButtonUp)
        st.set(key, node)
        key = "{0}.node".format(self.moveButtonDown)
        st.set(key, node)
        key = "{0}.active".format(self.pressButtonSeq)
        st.set(key, "1")
        self.action.setState(st)
    def setupButtons(self, sceneName, nodeName):
        key = "node.{0}.{1}.children".format(sceneName, nodeName)
        st = self.scene.state([key])
        for k in st.keys:
            children = st.value(k)
            for c in children:
                if (c.endswith("Up")   or
                    c.endswith("Down") or
                    c.endswith("Left") or
                    c.endswith("Right")):
                    self.buttons.append(c)

class CraneControlsListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl, sceneName):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
        self.sceneName = sceneName
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            actionName = k.replace(".active", "")
            state = (st.value(k)[0] == "1")
            self.impl.onActionState(self.sceneName, actionName, state)

class CraneControlsListenerScene(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            v = k.split(".")
            sceneName = v[1]
            nodeName = st.value(k)[0]
            self.impl.onSelection(sceneName, nodeName)

class CraneControls:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.nodeName  = nodeName
        self.scene     = scene
        self.action    = action
        # Create.
        self.impl           = CraneControlsImpl(scene, action)
        self.listenerAction = CraneControlsListenerAction(self.impl, sceneName)
        self.listenerScene  = CraneControlsListenerScene(self.impl)
        # Prepare.
        self.impl.setupButtons(sceneName, nodeName)
        keys = ["{0}.active".format(self.impl.pressButtonSeq)]
        self.action.addListener(keys, self.listenerAction)
        key = "selector.{0}.selectedNode".format(sceneName)
        self.scene.addListener([key], self.listenerScene)
    def __del__(self):
        # Tear down.
        self.action.removeListener(self.listenerAction)
        self.scene.removeListener(self.listenerScene)
        # Destroy.
        del self.listenerAction
        del self.listenerScene
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None

def SCRIPT_CREATE(sceneName, nodeName, scene, action):
    return CraneControls(sceneName, nodeName, scene, action)

def SCRIPT_DESTROY(instance):
    del instance

