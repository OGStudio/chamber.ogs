
import pymjin2

# Setup.
CRANE           = "crane_base"
CRANE_MOVE_DOWN = "moveBy.default.moveCraneDown"
CRANE_MOVE_UP   = "moveBy.default.moveCraneUp"

class CraneImpl(object):
    def __init__(self, scene, action, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.listeners = listeners
        # State.
        self.craneName = None
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        self.listeners = None
#    def onActionState(self, sceneName, actionName, state):
#        if (not state):
#            if (actionName == CONTROL_BUTTONS_PRESS_BUTTON):
#                self.pressedNodeName  = None
#                self.pressedSceneName = None
#            elif (actionName == CONTROL_BUTTONS_MOVE_BUTTON_DOWN):
#                for listener in self.listeners:
#                    listener.onCraneExecute(self.pressedSceneName,
#                                                     self.pressedNodeName)
#    def onSelection(self, sceneName, nodeName):
#        if (nodeName in self.buttons):
#            self.pressButton(sceneName, nodeName)
    def moveUp(self, up):
        print "move crane up:", up
        st = pymjin2.State()
        key = "{0}.active".format(CRANE_MOVE_UP)
        if (not up):
            key = "{0}.active".format(CRANE_MOVE_DOWN)
        st.set(key, "1")
        self.action.setState(st)
        # TODO: temporarily.
#        for listener in self.listeners:
#            listener.onCraneMoveUp(up)
#    def pressButton(self, sceneName, nodeName):
#        if (self.pressedNodeName):
#            return
#        self.pressedSceneName = sceneName
#        self.pressedNodeName  = nodeName
#        node = sceneName + "." + nodeName
#        st = pymjin2.State()
#        # Assign actions.
#        key = "{0}.node".format(CONTROL_BUTTONS_MOVE_BUTTON_UP)
#        st.set(key, node)
#        key = "{0}.node".format(CONTROL_BUTTONS_MOVE_BUTTON_DOWN)
#        st.set(key, node)
#        # Run.
#        key = "{0}.active".format(CONTROL_BUTTONS_PRESS_BUTTON)
#        st.set(key, "1")
#        self.action.setState(st)
    def setupNodes(self, sceneName, nodeName):
        self.craneName = sceneName + "." + nodeName
        st = pymjin2.State()
        st.set("{0}.node".format(CRANE_MOVE_DOWN), self.craneName)
        st.set("{0}.node".format(CRANE_MOVE_UP), self.craneName)
        self.action.setState(st)

#class CraneListenerAction(pymjin2.ComponentListener):
#    def __init__(self, impl, sceneName):
#        pymjin2.ComponentListener.__init__(self)
#        # Refer.
#        self.impl = impl
#        self.sceneName = sceneName
#    def __del__(self):
#        # Derefer.
#        self.impl = None
#    def onComponentStateChange(self, st):
#        for k in st.keys:
#            actionName = k.replace(".active", "")
#            state = (st.value(k)[0] == "1")
#            self.impl.onActionState(self.sceneName, actionName, state)
#
#class CraneListenerScene(pymjin2.ComponentListener):
#    def __init__(self, impl):
#        pymjin2.ComponentListener.__init__(self)
#        # Refer.
#        self.impl = impl
#    def __del__(self):
#        # Derefer.
#        self.impl = None
#    def onComponentStateChange(self, st):
#        for k in st.keys:
#            v = k.split(".")
#            sceneName = v[1]
#            nodeName = st.value(k)[0]
#            self.impl.onSelection(sceneName, nodeName)

class Crane:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.scene     = scene
        self.action    = action
        # Create.
        self.listeners      = {}
        self.impl           = CraneImpl(scene, action, self.listeners)
#        self.listenerAction = CraneListenerAction(self.impl, sceneName)
#        self.listenerScene  = CraneListenerScene(self.impl)
        # Prepare.
        self.impl.setupNodes(sceneName, CRANE)
#        keys = ["{0}.active".format(CONTROL_BUTTONS_PRESS_BUTTON),
#                "{0}.active".format(CONTROL_BUTTONS_MOVE_BUTTON_DOWN)]
#        self.action.addListener(keys, self.listenerAction)
#        key = "selector.{0}.selectedNode".format(sceneName)
#        self.scene.addListener([key], self.listenerScene)
    def __del__(self):
        # Tear down.
#        self.action.removeListener(self.listenerAction)
#        self.scene.removeListener(self.listenerScene)
#        # Destroy.
#        del self.listenerAction
#        del self.listenerScene
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
    def addListener(self, listener):
        self.listeners[listener] = True
    def moveUp(self, up):
        self.impl.moveUp(up)
    def removeListener(self, listener):
        if (listener is self.listeners):
            del self.listeners[listener]

