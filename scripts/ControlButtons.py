
import pymjin2

# Setup.
CONTROL_BUTTONS_MOVE_BUTTON_DOWN = "moveBy.default.moveButtonDown"
CONTROL_BUTTONS_MOVE_BUTTON_UP   = "moveBy.default.moveButtonUp"
CONTROL_BUTTONS_PRESS_BUTTON     = "sequence.default.pressButton"
CONTROL_BUTTONS_POSTFIX_DOWN     = "Down"
CONTROL_BUTTONS_POSTFIX_LEFT     = "Left"
CONTROL_BUTTONS_POSTFIX_RIGHT    = "Right"
CONTROL_BUTTONS_POSTFIX_UP       = "Up"

class ControlButtonsImpl(object):
    def __init__(self, scene, action, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.listeners = listeners
        # State.
        self.buttons          = []
        self.pressedNodeName  = None
        self.pressedSceneName = None
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        self.listeners = None
    def onActionState(self, sceneName, actionName, state):
        if (not state):
            if (actionName == CONTROL_BUTTONS_PRESS_BUTTON):
                self.pressedNodeName  = None
                self.pressedSceneName = None
            elif (actionName == CONTROL_BUTTONS_MOVE_BUTTON_DOWN):
                for listener in self.listeners:
                    listener.onControlButtonsExecute(self.pressedSceneName,
                                                     self.pressedNodeName)
    def onSelection(self, sceneName, nodeName):
        if (nodeName in self.buttons):
            self.pressButton(sceneName, nodeName)
    def pressButton(self, sceneName, nodeName):
        if (self.pressedNodeName):
            return
        self.pressedSceneName = sceneName
        self.pressedNodeName  = nodeName
        node = sceneName + "." + nodeName
        st = pymjin2.State()
        # Assign actions.
        key = "{0}.node".format(CONTROL_BUTTONS_MOVE_BUTTON_UP)
        st.set(key, node)
        key = "{0}.node".format(CONTROL_BUTTONS_MOVE_BUTTON_DOWN)
        st.set(key, node)
        # Run.
        key = "{0}.active".format(CONTROL_BUTTONS_PRESS_BUTTON)
        st.set(key, "1")
        self.action.setState(st)
    def setupButtons(self, sceneName, nodeName):
        # Collect all 4 buttons.
        key = "node.{0}.{1}.children".format(sceneName, nodeName)
        st = self.scene.state([key])
        for k in st.keys:
            children = st.value(k)
            for c in children:
                if (c.endswith(CONTROL_BUTTONS_POSTFIX_UP)   or
                    c.endswith(CONTROL_BUTTONS_POSTFIX_DOWN) or
                    c.endswith(CONTROL_BUTTONS_POSTFIX_LEFT) or
                    c.endswith(CONTROL_BUTTONS_POSTFIX_RIGHT)):
                    self.buttons.append(c)

class ControlButtonsListenerAction(pymjin2.ComponentListener):
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

class ControlButtonsListenerScene(pymjin2.ComponentListener):
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

class ControlButtons:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.scene     = scene
        self.action    = action
        # Create.
        self.listeners      = {}
        self.impl           = ControlButtonsImpl(scene, action, self.listeners)
        self.listenerAction = ControlButtonsListenerAction(self.impl, sceneName)
        self.listenerScene  = ControlButtonsListenerScene(self.impl)
        # Prepare.
        self.impl.setupButtons(sceneName, nodeName)
        keys = ["{0}.active".format(CONTROL_BUTTONS_PRESS_BUTTON),
                "{0}.active".format(CONTROL_BUTTONS_MOVE_BUTTON_DOWN)]
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
    def addListener(self, listener):
        self.listeners[listener] = True
    def removeListener(self, listener):
        if (listener is self.listeners):
            del self.listeners[listener]

