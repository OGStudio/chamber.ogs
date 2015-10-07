
import pymjin2

# Setup.
CRANE_PISTON        = "crane_arms_piston"
CRANE_LIFT          = "moveBy.default.liftCranePiston"
CRANE_LOWER         = "moveBy.default.lowerCranePiston"

class CraneLiftImpl(object):
    def __init__(self, scene, action, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.listeners = listeners
        # State.
        self.isMoving  = False
        self.isUp      = True
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        self.listeners = None
    def onActionState(self, sceneName, actionName, state):
        if (not state):
            self.isMoving = False
        for listener in self.listeners:
            listener.onCraneLift(state)
    def lift(self, up):
        if (self.isMoving):
            return
        # Already in the target position.
        if (up == self.isUp):
            return
        self.isMoving = True
        self.isUp = up
        st = pymjin2.State()
        key = "{0}.active".format(CRANE_LIFT if up else CRANE_LOWER)
        st.set(key, "1")
        self.action.setState(st)
    def setupNodes(self, sceneName, nodeName):
        node = sceneName + "." + nodeName
        st = pymjin2.State()
        st.set("{0}.node".format(CRANE_LIFT),  node)
        st.set("{0}.node".format(CRANE_LOWER), node)
        self.action.setState(st)

class CraneLiftListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl, sceneName):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
        self.sceneName = sceneName
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        # Ignore other instances.
        if (not self.impl.isMoving):
            return
        for k in st.keys:
            actionName = k.replace(".active", "")
            state = (st.value(k)[0] == "1")
            self.impl.onActionState(self.sceneName, actionName, state)

class CraneLift:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.scene     = scene
        self.action    = action
        # Create.
        self.listeners      = {}
        self.impl           = CraneLiftImpl(scene, action, self.listeners)
        self.listenerAction = CraneLiftListenerAction(self.impl, sceneName)
        # Prepare.
        self.impl.setupNodes(sceneName, CRANE_PISTON)
        keys = ["{0}.active".format(CRANE_LIFT),
                "{0}.active".format(CRANE_LOWER)]
        self.action.addListener(keys, self.listenerAction)
    def __del__(self):
        # Tear down.
        self.action.removeListener(self.listenerAction)
        # Destroy.
        del self.listenerAction
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
    def addListener(self, listener):
        self.listeners[listener] = True
    def lift(self, up):
        self.impl.lift(up)
    def removeListener(self, listener):
        if (listener is self.listeners):
            del self.listeners[listener]

