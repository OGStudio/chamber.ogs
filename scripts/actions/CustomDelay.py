
import pymjin2

class CustomDelay:
    def __init__(self, groupName, actionName, scene, action):
        print "CustomDelay({0}, {1}, {2}). START".format(id(self),
                                                         groupName,
                                                         actionName)
        # Refer.
        self.groupName  = groupName
        self.actionName = actionName
        # Create.
        self.calls = 0
    def __del__(self):
        print "CustomDelay({0}, {1}, {2}). FINISH".format(id(self),
                                                          self.groupName,
                                                          self.actionName)
    def setNode(self, sceneName, nodeName):
        print "CustomDelay.setNode({0}, {1})".format(sceneName, nodeName)
    def step(self, dt):
        self.calls = self.calls + 1
        print "CustomDelay.step({0}) calls: {1}".format(dt, self.calls)
        return True if self.calls < 5 else False

def ACTION_SCRIPT_CREATE(groupName, actionName, scene, action):
    return CustomDelay(groupName, actionName, scene, action)

def ACTION_SCRIPT_DESTROY(instance):
    del instance

