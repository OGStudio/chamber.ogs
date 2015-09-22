
import pymjin2

class RunCustomDelay:
    def __init__(self, groupName, actionName, scene, action):
        print "RunCustomDelay({0}, {1}, {2}). START".format(id(self),
                                                            groupName,
                                                            actionName)
        # Refer.
        self.groupName  = groupName
        self.actionName = actionName
        self.action     = action
    def __del__(self):
        # Derefer.
        self.action = None
        print "RunCustomDelay({0}, {1}, {2}). FINISH".format(id(self),
                                                             self.groupName,
                                                             self.actionName)
    def setNode(self, sceneName, nodeName):
        print "RunCustomDelay.setNode({0}, {1})".format(sceneName, nodeName)
    def step(self, dt):
        st = pymjin2.State()
        st.set("script.{0}.customDelay.active".format(self.groupName), "1")
        print "RunCustomDelay. 01.launching CustomDelay"
        self.action.setState(st)
        print "RunCustomDelay. 02.launching CustomDelay"
        return False

def ACTION_SCRIPT_CREATE(groupName, actionName, scene, action):
    return RunCustomDelay(groupName, actionName, scene, action)

def ACTION_SCRIPT_DESTROY(instance):
    del instance

