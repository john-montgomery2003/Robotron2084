import eventmanager
import model
import views
import controller
import sys
def run(mode):
    evManager = eventmanager.EventManager()
    gamemodel = model.Game(evManager)
    graphics = views.GraphicalView(evManager, gamemodel)
    keyboard = controller.KeyboardController(evManager, gamemodel)

    gamemodel.run(mode)

if __name__ == '__main__':
    if sys.argv[1].lower() == 'test':
        run('test')
