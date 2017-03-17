import graphics
import theme
import gameloop
import stage

def exit():
    if graphics.screen:
        graphics.exit()

def run(visual):
    try:
        stage.init()
        if visual:
            graphics.init()
        theme.init()
        gameloop.start()

    finally:
        exit()
