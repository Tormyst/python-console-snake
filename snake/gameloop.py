import time
import graphics
import game
import controls
import config

last_update = None
playing = False
state = 0
p = None
frame_time = 0.1


def update():
    game.update(p)
    graphics.update()


def start(program_runner):
    global playing, state, p

    playing = True
    p = program_runner
    final_score = 0
    c = 0

    init()
    for _ in range(3):
        while state == 0 and c < 500:
            if graphics.screen:
                controls.update()
                time.sleep(frame_time)
            update()
            c += 1
        reset()

    playing = False
    return final_score + c * config.score_values['time']

def stop():
    global playing, frame, last_update

    playing = False


def init():
    global state

    game.init()
    graphics.drawGame()
    state = 0


def reset():
    game.reset()
    graphics.drawGame()
