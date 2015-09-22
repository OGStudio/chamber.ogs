
import pymjin2

class RotateMaterial:
    def __init__(self, groupName, actionName, scene, action):
        print "RotateMaterial({0}, {1}, {2}). START".format(id(self),
                                                            groupName,
                                                            actionName)
        # Refer.
        self.groupName  = groupName
        self.actionName = actionName
        self.scene      = scene
        # Create.
        self.calls = 0
        self.sceneName = None
        self.nodeName = None
        self.materials = ["",
                          "subject",
                          "subjectRed"]
    def __del__(self):
        # Derefer.
        self.scene = None
        print "RotateMaterial({0}, {1}, {2}). FINISH".format(id(self),
                                                             self.groupName,
                                                             self.actionName)
    def setNode(self, sceneName, nodeName):
        print "RotateMaterial.setNode({0}, {1})".format(sceneName, nodeName)
        self.sceneName = sceneName
        self.nodeName = nodeName
    def step(self, dt):
        self.calls = self.calls + 1
        materialID = self.calls % 3
        st = pymjin2.State()
        key = "node.{0}.{1}.material".format(self.sceneName, self.nodeName)
        value = self.materials[materialID]
        #print key, value
        st.set(key, value)
        self.scene.setState(st)
        return False

def ACTION_SCRIPT_CREATE(groupName, actionName, scene, action):
    return RotateMaterial(groupName, actionName, scene, action)

def ACTION_SCRIPT_DESTROY(instance):
    del instance

