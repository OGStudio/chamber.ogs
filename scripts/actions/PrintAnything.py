
import pymjin2

class PrintAnything:
    def __init__(self, groupName, actionName, scene, action):
        print "PrintAnything({0}, {1}, {2}). START".format(id(self),
                                                           groupName,
                                                           actionName)
        # Refer.
        self.groupName  = groupName
        self.actionName = actionName
        # Create.
        self.calls = 0
    def __del__(self):
        print "PrintAnything({0}, {1}, {2}). FINISH".format(id(self),
                                                            self.groupName,
                                                            self.actionName)
    def setNode(self, sceneName, nodeName):
        print "PrintAnything.setNode({0}, {1})".format(sceneName, nodeName)
    def step(self, dt):
        self.calls = self.calls + 1
        print "PrintAnything.step({0}) call #{1}".format(dt, self.calls)
        return False

def ACTION_SCRIPT_CREATE(groupName, actionName, scene, action):
    return PrintAnything(groupName, actionName, scene, action)

def ACTION_SCRIPT_DESTROY(instance):
    del instance

