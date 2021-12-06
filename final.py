
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

screen_width, screen_height = 600, 600

cols = 6
rows = 6

# Number of the glut window.
window = 0

left = [-screen_width // cols // 2, -screen_height // 2 + 20]
right = [screen_width // cols // 2, -screen_height // 2 + 20]

point_x, point_y = [0, -screen_height // 2 + 30]

pressLeft, pressRight = False, False

class Wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50
    
    def create_wall(self):
        self.blocks = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                # rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength  = 1

                lower_left = [-screen_width // 2 + (2 * (col + 1)) + block_x, screen_height // 2 - self.height - (2 * (row + 1)) - block_y]
                higer_left = [-screen_width // 2 + (2 * (col + 1)) + block_x, screen_height // 2 - (2 * (row + 1)) - block_y]
                higher_right = [-screen_width // 2 + self.width + (2 * (col + 1)) + block_x, screen_height // 2 - (2 * (row + 1)) - block_y]
                lower_right = [-screen_width // 2 + self.width + (2 * (col + 1)) + block_x, screen_height // 2 - self.height - (2 * (row + 1)) - block_y]
                
                rect = [lower_left, higer_left, higher_right, lower_right]
                
                block_individual = [rect, strength, False]

                block_row.append(block_individual)

            self.blocks.append(block_row)


    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 3:
                    # block_col = block_blue
                    glColor3f(69.0/255.0, 177.0/255.0, 232.0/255.0)
                elif block[1] == 2:
                    # block_col = block_green
                    glColor3f(86.0/255.0, 174.0/255.0, 87.0/255.0)
                elif block[1] == 1:
                    # block_col = block_red
                    glColor3f(242.0/255.0, 85.0/255.0, 96.0/255.0)
                rect = block[0]
                glBegin(GL_QUADS)
                glVertex2f(rect[0][0], rect[0][1])
                glVertex2f(rect[1][0], rect[1][1])
                glVertex2f(rect[2][0], rect[2][1])
                glVertex2f(rect[3][0], rect[3][1])
                glEnd()
                # glFlush()

class Paddle:
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        # key = pygame.key.get_pressed()
        if pressLeft:
            if self.rect[0][0] > -screen_width // 2:
                self.rect[0][0] -= self.speed
                self.rect[1][0] -= self.speed
                self.direction = -1
        if pressRight:
            if self.rect[1][0] < screen_width // 2:
                self.rect[0][0] += self.speed
                self.rect[1][0] += self.speed
                self.direction = 1
    
    def draw(self):
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glLineWidth(20)
        glBegin(GL_LINES)
        glVertex2f(self.rect[0][0], self.rect[0][1])
        glVertex2f(self.rect[1][0], self.rect[1][1])
        glEnd()
        # glFlush()
    
    def reset(self):
        self.height = 20
        self.width = screen_width // cols
        # self.x = (screen_width // 2) - (self.width // 2)
        self.x = self.width // 2
        # self.y = screen_height - (self.height * 2)
        self.y = screen_height // 2 - self.height * 2
        self.speed = 10
        self.rect = (left, right)
        # self.rect = [[-self.x, -self.y], [self.x, -self.y]]
        self.direction = 0
    

class Ball:
    def __init__(self, x, y):
        self.reset(x, y)
    
    def move(self):

        collision_thresh = 10
        hit = False
        # global wall
    #     wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            block_count = 0
            for block in row:

                if block[0][0][0] < self.rect[0] and self.rect[0] < block[0][3][0]:
                    # print('-----------------------')
                    # collision from above
                    if abs(self.rect[1] - block[0][1][1]) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                        block[2] = True
                        
                    # collision from below
                    if abs(self.rect[1] - block[0][0][1]) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        block[2] = True
                if block[0][0][1] < self.rect[1] and self.rect[1] < block[0][1][1]:
                    # collision from left
                    if abs(self.rect[0] - block[0][0][0]) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                        block[2] = True
                    # collision from right
                    if abs(self.rect[0] - block[0][2][0]) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                        block[2] = True
                
                if wall.blocks[row_count][block_count][1] > 1 and wall.blocks[row_count][block_count][2]:
                    wall.blocks[row_count][block_count][1] -= 1
                    wall.blocks[row_count][block_count][2] = False
                elif wall.blocks[row_count][block_count][1] == 1 and wall.blocks[row_count][block_count][2]:
                    del wall.blocks[row_count][block_count]
                
    #             if wall.blocks[row_count][block_count][0] != (0, 0, 0, 0):
    #                 wall_destroyed = 0
                block_count += 1
            row_count += 1

    #     if wall_destroyed == 1:
    #         self.game_over = 1
                    


        if self.rect[0] < -screen_width // 2 or self.rect[0] > screen_width // 2:
            self.speed_x *= -1
        
        if self.rect[1] > screen_height // 2:
            self.speed_y *= -1
        if self.rect[1] < -screen_height // 2:
            self.game_over = -1

        if left[0] < self.rect[0] and self.rect[0] < right[0]:
            if abs(self.rect[1] - left[1]) < collision_thresh and self.speed_y < 0:
                self.speed_y *= -1
    #     if self.rect.colliderect(player_paddle):

    #         if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
    #             self.speed_y *= -1
    #             self.speed_x += player_paddle.direction
    #             if self.speed_x > self.speed_max:
    #                 self.speed_x = self.speed_max
    #             elif self.speed_x < 0 and self.speed_x < -self.speed_max:
    #                 self.speed_x = - self.speed_max
    #         else:
    #             self.speed_x *= -1

        self.rect[0] += self.speed_x
        self.rect[1] += self.speed_y

        return self.game_over

    def draw(self):
        glColor3f(142.0/255.0, 135.0/255.0, 123.0/255.0)
        glPointSize(20)
        glEnable(GL_POINT_SMOOTH)
        glBegin(GL_POINTS)
        glVertex2f(self.rect[0], self.rect[1])
        glEnd()
        # glFlush()

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        # self.rect = pygame.Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.rect = [point_x, point_y]
        self.speed_x = 4
        self.speed_y = 4
        self.speed_max = 5
        self.game_over = 0


wall = Wall()
wall.create_wall()

player_paddle = Paddle()

ball = Ball(point_x, point_y)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    wall.draw()

    player_paddle.draw()
    player_paddle.move()

    ball.draw()
    ball.move()

    glFlush()
    glutPostRedisplay()
    glutSwapBuffers()

def init():
    glClearColor(234.0/255.0, 218.0/255.0, 184.0/255.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(-screen_width/2, screen_width/2, -screen_height/2, screen_height/2)

def keyPressed(key, x, y):
    global pressLeft, pressRight
    
    if key == GLUT_KEY_LEFT:
        pressLeft = True
    if key == GLUT_KEY_RIGHT:
        pressRight = True
    glutPostRedisplay()

def keyReleased(key, x, y):
    global pressLeft, pressRight
    
    if key == GLUT_KEY_LEFT:
        pressLeft = False
    if key == GLUT_KEY_RIGHT:
        pressRight = False
    glutPostRedisplay()




def main():
    

    # global window
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(screen_width, screen_height)
    window = glutCreateWindow("Breakout")
    init()
    glutDisplayFunc(display)
    # glutTimerFunc(1000//60, display, 0)

    # glutKeyboardFunc(keyPressed)
    glutSpecialFunc(keyPressed)
    glutSpecialUpFunc(keyReleased)
    glutIdleFunc(display)
    # glutTimerFunc(1000//60, keyPressed, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()