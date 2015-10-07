
import pymjin2

# Setup.
CRANE            = "crane_base"
CRANE_ARMS_BASE  = "crane_arms_base"
CRANE_MOVE_DOWN  = "moveBy.default.moveCraneDown"
CRANE_MOVE_LEFT  = "moveBy.default.moveBeltLeft"
CRANE_MOVE_RIGHT = "moveBy.default.moveBeltRight"
CRANE_MOVE_UP    = "moveBy.default.moveCraneUp"
CRANE_STEPS_H    = 3
CRANE_STEPS_V    = 3

class CraneImpl(object):
    def __init__(self, scene, action, listeners):
        # Refer.
        self.scene     = scene
        self.action    = action
        self.listeners = listeners
        # State.
        self.isMoving  = False
        self.stepH     = 1
        self.stepV     = 1
    def __del__(self):
        # Derefer.
        self.scene     = None
        self.action    = None
        self.listeners = None
    def onActionState(self, sceneName, actionName, state):
        if (not state):
            self.isMoving = False
        for listener in self.listeners:
            listener.onCraneMove(state)
    def moveRight(self, right):
        if (self.isMoving):
            return
        if (not self.validateNewStepV(right)):
            return
        self.isMoving = True
        st = pymjin2.State()
        key = "{0}.active".format(CRANE_MOVE_RIGHT if right else CRANE_MOVE_LEFT)
        st.set(key, "1")
        self.action.setState(st)
    def moveUp(self, up):
        if (self.isMoving):
            return
        if (not self.validateNewStepH(up)):
            return
        self.isMoving = True
        st = pymjin2.State()
        key = "{0}.active".format(CRANE_MOVE_UP if up else CRANE_MOVE_DOWN)
        st.set(key, "1")
        self.action.setState(st)
    def setupNodes(self, sceneName, crane, craneArmsBase):
        craneName = sceneName + "." + crane
        craneArmsBaseName = sceneName + "." + craneArmsBase
        st = pymjin2.State()
        st.set("{0}.node".format(CRANE_MOVE_DOWN),  craneName)
        st.set("{0}.node".format(CRANE_MOVE_UP),    craneName)
        st.set("{0}.node".format(CRANE_MOVE_LEFT),  craneArmsBaseName)
        st.set("{0}.node".format(CRANE_MOVE_RIGHT), craneArmsBaseName)
        self.action.setState(st)
    def validateNewStepH(self, up):
        newStepH = self.stepH - 1 if up else self.stepH + 1
        ok = False
        if (up):
            ok = (newStepH >= 0)
        else:
            ok = (newStepH < CRANE_STEPS_H)
        if (ok):
            self.stepH = newStepH
        return ok
    def validateNewStepV(self, right):
        newStepV = self.stepV + 1 if right else self.stepV - 1
        ok = False
        if (right):
            ok = (newStepV < CRANE_STEPS_V)
        else:
            ok = (newStepV >= 0)
        if (ok):
            self.stepV = newStepV
        return ok

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
        # Only listen to actions when we do it.
        if (not self.impl.isMoving):
            return
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
        self.impl.setupNodes(sceneName, CRANE, CRANE_ARMS_BASE)
        keys = ["{0}.active".format(CRANE_MOVE_DOWN),
                "{0}.active".format(CRANE_MOVE_UP),
                "{0}.active".format(CRANE_MOVE_LEFT),
                "{0}.active".format(CRANE_MOVE_RIGHT)]
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
    def moveRight(self, right):
        self.impl.moveRight(right)
    def moveUp(self, up):
        self.impl.moveUp(up)
    def removeListener(self, listener):
        if (listener is self.listeners):
            del self.listeners[listener]

