
import pymjin2

# Setup.
CRANE           = "crane_base"
CRANE_MOVE_DOWN = "moveBy.default.moveCraneDown"
CRANE_MOVE_UP   = "moveBy.default.moveCraneUp"
CRANE_STEPS_H   = 3

class CraneImpl(object):
    def __init__(self, scene, action, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.listeners = listeners
        # State.
        self.craneName = None
        self.canMove   = True
        self.stepH     = 1
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        self.listeners = None
    def onActionState(self, sceneName, actionName, state):
        print "Crane.onActionState", actionName, state
        if (not state):
            self.canMove = True
        if ((actionName == CRANE_MOVE_UP) or
            (actionName == CRANE_MOVE_DOWN)):
            for listener in self.listeners:
                listener.onCraneMoveUp(actionName == CRANE_MOVE_UP, state)
    def moveUp(self, up):
        if (not self.canMove):
            return
        # Check new step.
        newStepH = self.stepH - 1 if up else self.stepH + 1
        ok = False
        if (up):
            ok = (newStepH >= 0)
        else:
            ok = (newStepH < CRANE_STEPS_H)
        if (not ok):
            return
        self.stepH = newStepH
        # Move.
        self.canMove = False
        st = pymjin2.State()
        key = "{0}.active".format(CRANE_MOVE_UP)
        if (not up):
            key = "{0}.active".format(CRANE_MOVE_DOWN)
        st.set(key, "1")
        self.action.setState(st)
    def setupNodes(self, sceneName, nodeName):
        self.craneName = sceneName + "." + nodeName
        st = pymjin2.State()
        st.set("{0}.node".format(CRANE_MOVE_DOWN), self.craneName)
        st.set("{0}.node".format(CRANE_MOVE_UP), self.craneName)
        self.action.setState(st)

class CraneListenerAction(pymjin2.ComponentListener):
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

class Crane:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.scene     = scene
        self.action    = action
        # Create.
        self.listeners      = {}
        self.impl           = CraneImpl(scene, action, self.listeners)
        self.listenerAction = CraneListenerAction(self.impl, sceneName)
        # Prepare.
        self.impl.setupNodes(sceneName, CRANE)
        keys = ["{0}.active".format(CRANE_MOVE_DOWN),
                "{0}.active".format(CRANE_MOVE_UP)]
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
    def moveUp(self, up):
        self.impl.moveUp(up)
    def removeListener(self, listener):
        if (listener is self.listeners):
            del self.listeners[listener]

