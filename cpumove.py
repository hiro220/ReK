import random
import math

PI = 3.141592

class Sample1():
    
    def move():
        return left()

class Sample2():

    def  __init__(self):
        self.count = 0

    def move(self):
        if 0 <= self.count <= 14:
                dx, dy = -2.5, 3
                self.count += 1
                return dx, dy
        elif 15 <= self.count <= 30:
            dx, dy = -2.5, -3
            self.count += 1
            if self.count == 31:
                self.count = 0
            return dx, dy

class Sample3():

    def __init__(self):
        self.count = 0
        self.curve_count = 0

    def move(self, dx, dy):
        if self.count <= 100:
            self.count += 1
            return left()

        dx, dy, self.curve_count = curve(-10, -5, 200, self.curve_count, dx, dy)
        return dx, dy

  
class Sample4():
    
    def __init__(self):
        self.count = 0
        self.curve_count = 0

    def move(self, dx, dy):
        if self.count <= 150:
            self.count += 1
            return left()
        elif self.count <= 220:
            self.count += 1
            return rightup()
        elif self.count >= 221:
            dx, dy, self.curve_count = curve(-10, -6, 160, self.curve_count, dx, dy)
            return dx, dy

class Sample5():
    def __init__(self):
        self.count = 0
        self.curve_count = 0

    def move(self, dx, dy):
        if self.count <= 150:
            self.count += 1
            return left()
        elif self.count <= 220:
            self.count += 1
            return rightdown()
        elif self.count >= 221:
            dx, dy, self.curve_count = curve(-10, 6, 160, self.curve_count, dx, dy)
            return dx, dy

class Sample6():
    
    def __init__(self):
        self.count = 0
        self.circle_count = 0

    def move(self, dx, dy):
        if self.count <= 80:
            self.count += 1
            return left()
        elif self.count <= 400:
            self.count += 1
            dx, dy, self.circle_count = circle(-7, -7, 50, self.circle_count)
            return dx, dy
        elif self.count >= 401:
            return dx, dy

class Sample7():
    
    def __init__(self):
        self.count = 0
        self.circle_count = 0

    def move(self, dx, dy):
        if self.count <= 80:
            self.count += 1
            return left()
        elif self.count <= 400:
            self.count += 1
            dx, dy, self.circle_count = circle(-7, 7, 50, self.circle_count)
            return dx, dy
        elif self.count >= 401:
            return dx, dy


class Sample8():
    
    def __init__(self):
        self.count = 0
        self.circle_count = 0

    def move(self, dx, dy):
        if self.count <= 80:
            self.count += 1
            return left()
        elif self.count <= 400:
            self.count += 1
            dx, dy, self.circle_count = circle(7, 7, 50, self.circle_count)
            return dx, dy
        elif self.count >= 401:
            return dx, dy
            
class Sample9():
    
    def __init__(self):
        self.count = 0
        self.circle_count = 0

    def move(self, dx, dy):
        if self.count <= 80:
            self.count += 1
            return left()
        elif self.count <= 400:
            self.count += 1
            dx, dy, self.circle_count = circle(7, -7, 50, self.circle_count)
            return dx, dy 
        elif self.count >= 401:
            return dx, dy

def left():
    return -5, 0

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
    return 3, -3

def rightdown():
    return 3, 3

def curve(velx, vely, cycle, count, dx, dy):
    if count != cycle/2: 
        dx = math.sin(PI * (count) / cycle) * velx
        dy = math.sin(PI * (count+(cycle/2)) / cycle) *vely
        count += 1
        return dx, dy, count

    return dx, dy, count
    
def circle(velx, vely, cycle, count): 
    dx = math.sin(PI * (count) / cycle) * velx
    dy = math.sin(PI * (count+(cycle/2)) / cycle) *vely
    count += 1
    return dx, dy, count

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