import eventmanager
import model
import views
import controller

def run():
    evManager = eventmanager.EventManager()
    gamemodel = model.Game(evManager)
    graphics = views.GraphicalView(evManager, gamemodel)
    keyboard = controller.KeyboardController(evManager, gamemodel)

    gamemodel.run()

if __name__ == '__main__':
    run()