import graphics
import theme
import gameloop
import stage
import random

def exit():
    if graphics.screen:
        graphics.exit()

def run(visual, program_runner):
    #random.seed(0)
    score = 0
    try:
        stage.init()
        if visual:
            graphics.init()
        theme.init()
        score = gameloop.start(program_runner)
    finally:
        exit()
    return score
