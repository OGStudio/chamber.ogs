
import pymjin2

class StandControlsImpl(object):
    def __init__(self, scene, action):
        # Refer.
        self.scene  = scene
        self.action = action
        # Setup.
        self.belts     = ["lineBelt3",
                          "lineBelt1",
                          "lineBelt2"]
        self.lights    = ["lineLight3",
                          "lineLight1",
                          "lineLight2"]
        self.lightOn   = "line_segment_light_on"
        self.lightOff  = "line_segment_light_off"
        self.nodeLeft  = "arrowLeft"
        self.nodeRight = "arrowRight"
        self.nodeUp    = "arrowUp"
        self.nodeDown  = "arrowDown"
        self.moveLeft  = "moveBy.default.moveBeltLeft"
        self.moveRight = "moveBy.default.moveBeltRight"
        # State.
        self.currentLight = 0
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
    def moveSelectedLine(self, sceneName, right):
        print "moveSelectedLine", right
        keyNode = "{0}.node".format(self.moveLeft)
        keyRun  = "{0}.active".format(self.moveLeft)
        if (right):
            keyNode = "{0}.node".format(self.moveRight)
            keyRun  = "{0}.active".format(self.moveRight)
        value = self.belts[self.currentLight]
        st = pymjin2.State()
        st.set(keyNode, sceneName + "." + value)
        st.set(keyRun, "1")
        self.action.setState(st)
    def processLineCommand(self, sceneName, cmd):
        if (cmd == self.nodeUp):
            self.switchLine(sceneName, False)
        elif (cmd == self.nodeDown):
            self.switchLine(sceneName, True)
        elif (cmd == self.nodeLeft):
            self.moveSelectedLine(sceneName, False)
        elif (cmd == self.nodeRight):
            self.moveSelectedLine(sceneName, True)
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

class StandControlsListenerScene(pymjin2.ComponentListener):
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

class StandControls:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.nodeName  = nodeName
        self.scene     = scene
        # Create.
        self.impl          = StandControlsImpl(scene, action)
        self.listenerScene = StandControlsListenerScene(self.impl)
        # Prepare.
        key = "selector.{0}.selectedNode".format(sceneName)
        self.scene.addListener([key], self.listenerScene)
    def __del__(self):
        # Tear down.
        self.scene.removeListener(self.listenerScene)
        # Destroy.
        del self.listenerScene
        del self.impl
        # Derefer.
        self.scene = None

def SCRIPT_CREATE(sceneName, nodeName, scene, action):
    return StandControls(sceneName, nodeName, scene, action)

def SCRIPT_DESTROY(instance):
    del instance

