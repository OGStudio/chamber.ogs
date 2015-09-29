
import pymjin2

class StandControlsImpl(object):
    def __init__(self, scene):
        # Refer.
        self.scene = scene
        # Setup.
        self.lights = ["lineLight3",
                       "lineLight1",
                       "lineLight2"]
        self.lightOn  = "line_segment_light_on"
        self.lightOff = "line_segment_light_off"
        # State.
        self.currentLight = 0
    def __del__(self):
        # Derefer.
        self.scene = None
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
            if (value == "arrowUp"):
                self.impl.switchLine(sceneName, False)
            elif (value == "arrowDown"):
                self.impl.switchLine(sceneName, True)

class StandControls:
    def __init__(self, sceneName, nodeName, scene, action):
        # Refer.
        self.sceneName = sceneName
        self.nodeName  = nodeName
        self.scene     = scene
        # Create.
        self.impl          = StandControlsImpl(scene)
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

