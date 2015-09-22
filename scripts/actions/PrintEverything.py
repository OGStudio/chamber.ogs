
import pymjin2

class PrintEverything:
    def __init__(self, groupName, actionName, scene, action):
        print "PrintEverything({0}, {1}, {2}). START".format(id(self),
                                                             groupName,
                                                             actionName)
        # Refer.
        self.groupName  = groupName
        self.actionName = actionName
    def __del__(self):
        print "PrintEverything({0}, {1}, {2}). FINISH".format(id(self),
                                                              self.groupName,
                                                              self.actionName)
    def setNode(self, sceneName, nodeName):
        print "PrintEverything.setNode({0}, {1})".format(sceneName, nodeName)
    def step(self, dt):
        print "PrintEverything.step({0})".format(dt)
        return False

def ACTION_SCRIPT_CREATE(groupName, actionName, scene, action):
    return PrintEverything(groupName, actionName, scene, action)

def ACTION_SCRIPT_DESTROY(instance):
    del instance

