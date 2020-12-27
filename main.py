import eventmanager
import model
import views
import controller

def run():
    evManager = eventmanager.EventManager()

    graphics = views.GraphicalView(evManager)
    keyboard = controller.KeyboardController(evManager)
    gamemodel = model.Game(evManager)
    gamemodel.run()

if __name__ == '__main__':
    run()