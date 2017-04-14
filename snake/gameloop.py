import time
import graphics
import game
import controls
import config

last_update = None
playing = False
state = 0
p = None
frame_time = 0.07
run_count = 1


def update():
    retVal = game.update(p)
    graphics.update(p)
    return retVal


def start(program_runner):
    global playing, state, p

    playing = True
    p = program_runner

    totalScore = 0
    totalTime = 0

    for _ in range(run_count): # Score based on multiple runs decided by value.
        t = 0
        timeout = config.timeout['init']
        init()
        while state == 0 and t < timeout:
            if graphics.screen:
                controls.update()
                time.sleep(frame_time)
            if update() and timeout < config.timeout['max']:  # update returns true if ate an apple
                timeout += config.timeout['step']
            t += 1
        totalScore += game.score
        totalTime += t
        reset()

    playing = False
    return (totalScore, totalTime)

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
