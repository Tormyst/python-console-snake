
import stage
import gameloop
import math
import random
import config

direction = (0, 0)
lastPos = (0, 0)
snake = []
speed = 1
apple = None
grow = config.initial_size - 1
score = 0


def get_input():
    closest_wall=[
            snake[0][0]-stage.boundaries['top'],
            stage.boundaries['right']-snake[0][1],
            stage.boundaries['bottom']-snake[0][0],
            snake[0][1]-stage.boundaries['left']
            ]

    for location in snake[1:]:
        if snake[0][0] == location[0]:
            distance = snake[0][1] - location[1]
            # print "here x", distance, closest_wall[3], closest_wall[1]
            if distance >= 0:
                distance -= 1
                if distance < closest_wall[3]:
                    closest_wall[3] = distance
            else:
                distance += 1
                distance = -distance
                if distance < closest_wall[1]:
                    closest_wall[1] = distance
        if snake[0][1] == location[1]:
            # print "here y"
            distance = snake[0][0] - location[0]
            if distance >= 0:
                distance -= 1
                if distance < closest_wall[0]:
                    closest_wall[0] = distance
            else:
                distance += 1
                distance = -distance
                if distance < closest_wall[2]:
                    closest_wall[2] = distance


    return [
            apple[0]-snake[0][0],
            apple[1]-snake[0][1],
            closest_wall[0],
            closest_wall[1],
            closest_wall[2],
            closest_wall[3]
            ]

def get_direction(p):
    in_vals = get_input()
    p.set_input(in_vals)
    p.run()
    return p.get_value()

def update(p):
    global direction
    if p:
        direction = [(1,0),(0,1),(-1,0),(0,-1)][get_direction(p)]
    moveSnake()
    retVal = checkCatch()
    checkPositionAllowed()
    return retVal


def checkCatch():
    if not len(snake) or not apple:
        return False

    if (snake[0][0]) == apple[0] and (snake[0][1]) == apple[1]:
        eatApple()
        return True
    return False

def eatApple():
    global grow, score

    spawnApple()
    grow += config.food_values['apple']
    score += config.score_values['apple']


def moveSnake():
    global grow, lastPos

    last_unchanged = None
    lastPos = (snake[len(snake)-1][0], snake[len(snake)-1][1])
    for i, part in enumerate(snake):
        if i == 0:
            x = part[0] + speed * direction[0]
            y = part[1] + speed * direction[1]
        else:
            x = last_unchanged[0]
            y = last_unchanged[1]

        last_unchanged = (snake[i][0], snake[i][1])
        snake[i] = (x, y)

    if grow:
        snake.append(last_unchanged)
        grow -= 1


def getGameArea():
    w = math.fabs(stage.boundaries['right'] - stage.boundaries['left'])
    h = math.fabs(stage.boundaries['top'] - stage.boundaries['bottom'])

    return int(math.floor(w * h))


def reset():
    global direction, snake, apple, score, grow

    direction = (1, 0)
    snake = [(0, 0)]
    gameloop.frame = 1
    grow = config.initial_size - 1
    spawnApple()
    score = 0


def spawnApple():
    global apple
    position_unset = True
    while position_unset:
        x = random.randrange(stage.boundaries['left'], stage.boundaries['right'])
        y = random.randrange(stage.boundaries['top'], stage.boundaries['bottom'])
        if isOutOfBoundaries(x, y): continue
        for part in snake:
            if part[0] == x and part[1] == y:
                continue
        position_unset = False

    apple = (x, y)


def isOutOfBoundaries(x, y):
    if x < stage.boundaries['left'] or x > stage.boundaries['right'] - 1:
        return True

    elif y < stage.boundaries['top'] or y > stage.boundaries['bottom'] - 1:
        return True

    return False


def checkPositionAllowed():
    collides_with_body = False
    x = snake[0][0]
    y = snake[0][1]

    for i in range(1, len(snake) - 1):
        if x == snake[i][0] and y == snake[i][1]:
            collides_with_body = True
            break

    if (collides_with_body or isOutOfBoundaries(x, y)):
        gameloop.state = 1
