
import graphics
import theme
import gameloop
import parser
import stage

def exit():
    graphics.exit()

def run():
    try:
        # parser.init()
        stage.init()
        graphics.init()
        theme.init()
        gameloop.start()

    except KeyboardInterrupt:
        exit()

run()
