import graphics
import theme
import gameloop
import stage

def exit():
    graphics.exit()

def run():
    try:
        stage.init()
        graphics.init()
        theme.init()
        gameloop.start()

    finally:
        exit()

run()
