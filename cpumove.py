import random

def Sample1():
    return left()

def Sample2(count):
    if 0 <= count <= 14:
            dx, dy = -2.5, 3
            count += 1
            return dx, dy, count
    elif 15 <= count <= 30:
        dx, dy = -2.5, -3
        count += 1
        if count == 31:
            count = 0
        return dx, dy, count

def Sample3(dx, acceleNum):
    return acceleration(dx, acceleNum)
  
def Sample4(dx, dy, count, move_count):
    return random_move(dx, dy, count, move_count)


def left():
    return -2.5, 0

def right():
    return 2.5, 0

def up():
    return 0, 2.5

def down():
    return 0, -2.5

def leftup():
    return -2, -2

def leftdown():
    return -2, 2 

def rightup():
    return 2, -2

def rightdown():
    return 2, 2

def acceleration(dx, acceleNum):
    return dx - acceleNum

def random_move(dx,dy, count, move_count):
    if count == move_count:
        count = 0
        num = random.randint(1, 8)
        if num == 1:
            list = left()  
            return list[0], list[1], count
        elif num == 2:
            list = right()
            return list[0],list[1], count
        elif num == 3:
            list = up()
            return list[0], list[1], count
        elif num == 4:
            list = down()
            return list[0], list[1], count
        elif num == 5:
            list = leftup()
            return list[0], list[1], count
        elif num == 6:
            list = leftdown()
            return list[0], list[1], count
        elif num == 7:
            list = rightup()
            return list[0], list[1], count
        elif num == 8:
            list = rightup()
            return list[0], list[1], count
    
    return dx, dy, count+1