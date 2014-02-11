from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import math

class EmoGame(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.environ.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-10, 0, -10)


        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

    def spinCameraTask(self, task):
        ang = task.time*60.0
        angRad = math.radians(ang)
        self.camera.setPos(20*math.sin(angRad), -20*math.cos(angRad),3)
        self.camera.setHpr(ang, 0, 0)
        return Task.cont

game = EmoGame()
game.run()

