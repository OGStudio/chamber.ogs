
import pymjin2

class ControlsImpl(object):
    def __init__(self, scene, action):
        # Refer.
        self.scene  = scene
        self.action = action
        # Setup.
        self.beltSteps = 3
        self.belts     = { "lineBelt1" : 0,
                           "lineBelt2" : 0,
                           "lineBelt3" : 0}
        self.lights    = ["lineLight1",
                          "lineLight2",
                          "lineLight3"]
        self.lightOn   = "line_segment_light_on"
        self.lightOff  = "line_segment_light_off"
        self.signal    = "controlSignal"
        self.signalOn  = "control_signal_on"
        self.signalOff = "control_signal_off"
        self.nodeLeft  = "controlArrowLeft"
        self.nodeRight = "controlArrowRight"
        self.nodeUp    = "controlArrowUp"
        self.nodeDown  = "controlArrowDown"
        self.moveLeft  = "moveBy.default.moveBeltLeft"
        self.moveRight = "moveBy.default.moveBeltRight"
        self.pressNode = "moveBy.default.pressArrow"
        # State.
        self.currentLight = 0
        self.beltIsMoving = False
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
    def moveSelectedLine(self, sceneName, right):
        belts = sorted(self.belts.keys())
        beltName = belts[self.currentLight]
        step = self.belts[beltName]
        newStep = step + 1 if right else step - 1
        ok = False
        if (right):
            ok = newStep < self.beltSteps
        else:
            ok = newStep >= 0
        if (not ok):
            return
        self.belts[beltName] = newStep
        keyNode = "{0}.node".format(self.moveLeft)
        keyRun  = "{0}.active".format(self.moveLeft)
        if (right):
            keyNode = "{0}.node".format(self.moveRight)
            keyRun  = "{0}.active".format(self.moveRight)
        st = pymjin2.State()
        st.set(keyNode, sceneName + "." + beltName)
        st.set(keyRun, "1")
        self.action.setState(st)
    def onActionState(self, sceneName, actionName, state):
        self.beltIsMoving = state
        # Set signal material based on activity.
        mat = self.signalOff
        if (state):
            mat = self.signalOn
        key = "node.{0}.{1}.material".format(sceneName, self.signal)
        st = pymjin2.State()
        st.set(key, mat)
        self.scene.setState(st)
    def pressArrow(self, sceneName, arrowName):
        print "pressArrow", sceneName, arrowName
        st = pymjin2.State()
        keyNode = "{0}.node".format(self.pressNode)
        keyRun  = "{0}.active".format(self.pressNode)
        st.set(keyNode, sceneName + "." + arrowName)
        st.set(keyRun, "1")
        self.action.setState(st)
    def processLineCommand(self, sceneName, cmd):
        if (cmd == self.nodeUp):
            self.switchLine(sceneName, False)
            self.pressArrow(sceneName, cmd);
        elif (cmd == self.nodeDown):
            self.switchLine(sceneName, True)
            self.pressArrow(sceneName, cmd);
        if (not self.beltIsMoving):
            if (cmd == self.nodeLeft):
                self.moveSelectedLine(sceneName, False)
                self.pressArrow(sceneName, cmd);
            elif (cmd == self.nodeRight):
                self.moveSelectedLine(sceneName, True)
                self.pressArrow(sceneName, cmd);
    def setLightState(self, sceneName, lightName, state):
        key = "node.{0}.{1}.children".format(sceneName, lightName)
        st = self.scene.state([key])
        mat = self.lightOn if state else self.lightOff
        st2 = pymjin2.State()
        for k in st.keys:
            children = st.value(k)
            for c in children:
                key = "node.{0}.{1}.material".format(sceneName, c)
                st2.set(key, mat)
        self.scene.setState(st2)
    def switchLine(self, sceneName, next):
        currentLight = self.currentLight
        # Stop on edges.
        if (next):
            currentLight = currentLight + 1
            if (currentLight >= len(self.lights)):
                currentLight = len(self.lights) - 1
        else:
            currentLight = currentLight - 1
            if (currentLight < 0):
                currentLight = 0
        # Do nothing if nothing changed.
        if (currentLight == self.currentLight):
            return
        # Deselect previous line.
        self.setLightState(sceneName, self.lights[self.currentLight], False)
        # Select new one.
        self.setLightState(sceneName, self.lights[currentLight], True)
        # Save new selection.
        self.currentLight = currentLight

class ControlsListenerAction(pymjin2.ComponentListener):
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

class ControlsListenerScene(pymjin2.ComponentListener):
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
            value = st.value(k)[0]
            self.impl.processLineCommand(sceneName, value)

class Controls:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.nodeName  = nodeName
        self.scene     = scene
        self.action    = action
        # Create.
        self.impl           = ControlsImpl(scene, action)
        self.listenerAction = ControlsListenerAction(self.impl, sceneName)
        self.listenerScene  = ControlsListenerScene(self.impl)
        # Prepare.
        keys = ["{0}.active".format(self.impl.moveLeft),
                "{0}.active".format(self.impl.moveRight)]
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
    return Controls(sceneName, nodeName, scene, action)

def SCRIPT_DESTROY(instance):
    del instance

