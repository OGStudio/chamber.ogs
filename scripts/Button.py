
import pymjin2

#BUTTON_ACTION_PRESS = "moveBy.default.pressButton"
BUTTON_ACTION_PRESS_TYPE  = "moveBy"
BUTTON_ACTION_PRESS_GROUP = "default"
BUTTON_ACTION_PRESS_NAME  = "moveButtonDown"

class ButtonImpl(object):
    def __init__(self, scene, action, senv):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = senv
        # Create.
        self.selectable = {}
        self.actions    = {}
    def __del__(self):
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
    def onActionState(self, actionName, state):
        # Ignore activation.
        if (state):
            return
        # Ignore other actions.
        if (actionName not in self.actions):
            return
        print "onActionState", actionName, state
        # Report.
        st = pymjin2.State()
        key = "button.{0}.selected".format(self.actions[actionName])
        st.set(key, "1")
        self.senv.reportStateChange(st)
        st.set(key, "0")
        self.senv.reportStateChange(st)
    def onSelection(self, sceneName, nodeName):
        if ((sceneName not in self.selectable) or
            (nodeName not in self.selectable[sceneName])):
            return
        actionName = self.selectable[sceneName][nodeName]
        node = "{0}.{1}".format(sceneName, nodeName)
        st = pymjin2.State()
        st.set("{0}.node".format(actionName), node)
        st.set("{0}.active".format(actionName), "1")
        self.action.setState(st)
    def setSelectable(self, sceneName, nodeName, state):
        # Make sure scene exists.
        if (sceneName not in self.selectable):
            self.selectable[sceneName] = {}
        if (state):
            key = "{0}.{1}.{2}.clone".format(BUTTON_ACTION_PRESS_TYPE,
                                             BUTTON_ACTION_PRESS_GROUP,
                                             BUTTON_ACTION_PRESS_NAME)
            st = self.action.state([key])
            newGroupName = st.value(key)[0]
            newActionName = "{0}.{1}.{2}".format(BUTTON_ACTION_PRESS_TYPE,
                                                 newGroupName,
                                                 BUTTON_ACTION_PRESS_NAME)
            self.selectable[sceneName][nodeName] = newActionName
            self.actions[newActionName] = "{0}.{1}".format(sceneName, nodeName)
        # Remove disabled.
        elif (nodeName in self.selectable[sceneName]):
            actionName = self.selectable[sceneName][nodeName]
            del self.actions[actionName]
            del self.selectable[sceneName][nodeName]

class ButtonListenerAction(pymjin2.ComponentListener):
    def __init__(self, impl):
        pymjin2.ComponentListener.__init__(self)
        # Refer.
        self.impl = impl
    def __del__(self):
        # Derefer.
        self.impl = None
    def onComponentStateChange(self, st):
        for k in st.keys:
            actionName = k.replace(".active", "")
            state = (st.value(k)[0] == "1")
            self.impl.onActionState(actionName, state)

class ButtonListenerSelection(pymjin2.ComponentListener):
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
            # Ignore deselection.
            if (not len(nodeName)):
                continue
            self.impl.onSelection(sceneName, nodeName)

class ButtonExtensionScriptEnvironment(pymjin2.Extension):
    def __init__(self, impl):
        pymjin2.Extension.__init__(self)
        # Refer.
        self.impl = impl
    def deinit(self):
        # Derefer.
        self.impl = None
        print "ButtonExt.deinit"
    def description(self):
        return "Turn any node into a simple button"
    def keys(self):
        return ["button...selectable",
                "button...selected"]
    def name(self):
        return "ButtonExtensionScriptEnvironment"
    def set(self, key, value):
        v = key.split(".")
        sceneName = v[1]
        nodeName  = v[2]
        self.impl.setSelectable(sceneName, nodeName, value == "1")

class Button:
    def __init__(self, scene, action, scriptEnvironment):
        # Refer.
        self.scene  = scene
        self.action = action
        self.senv   = scriptEnvironment
        # Create.
        self.impl              = ButtonImpl(scene, action, scriptEnvironment)
        self.listenerAction    = ButtonListenerAction(self.impl)
        self.listenerSelection = ButtonListenerSelection(self.impl)
        self.extension         = ButtonExtensionScriptEnvironment(self.impl)
        # Prepare.
        key = "selector..selectedNode"
        self.scene.addListener([key], self.listenerSelection)
        key = "{0}..{1}.active".format(BUTTON_ACTION_PRESS_TYPE,
                                       BUTTON_ACTION_PRESS_NAME)
        self.action.addListener([key], self.listenerAction)
        self.senv.addExtension(self.extension)
        print "{0} Button.__init__".format(id(self))
    def __del__(self):
        # Tear down.
        self.action.removeListener(self.listenerAction)
        self.scene.removeListener(self.listenerSelection)
        self.senv.removeExtension(self.extension)
        # Destroy.
        del self.listenerAction
        del self.listenerSelection
        del self.extension
        del self.impl
        # Derefer.
        self.scene  = None
        self.action = None
        self.senv   = None
        print "{0} Button.__del__".format(id(self))

