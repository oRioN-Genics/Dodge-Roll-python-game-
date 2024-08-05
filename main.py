from tkinter import *
import random

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
ROAD_WIDTH = 280
ROAD_HEIGHT = WINDOW_HEIGHT
SPEED = 50
NUM_WALLS = 4
WALL_SPEED = 500
SPACE_SIZE = 40
BALL_COLOR = "#FF0000"
WALL_COLOR = "#000000"
BACKGROUND_COLOR = "#ADD8E6"
ROAD_COLOR = "#808080"

class Ball:
    def __init__(self):
        global canvas_to_road
        ball_x = canvas_to_road + int((ROAD_WIDTH + SPACE_SIZE) / 2)
        ball_y = ROAD_HEIGHT - SPACE_SIZE

        self.coordinates = [ball_x, ball_y]
        canvas.create_oval(ball_x, ball_y, ball_x - SPACE_SIZE, ball_y - SPACE_SIZE, fill=BALL_COLOR, tag='ball')

class Wall:
    def __init__(self):
        self.width = random.randint(1, ((ROAD_WIDTH - (2 * SPACE_SIZE)) / SPACE_SIZE)) * SPACE_SIZE
        self.height = random.randint(1, 6) * SPACE_SIZE
        self.position = random.randint(0, (ROAD_WIDTH - self.width))
        self.x = int(self.position + canvas_to_road)
        self.y = int((random.randint(-50, 0)) * SPACE_SIZE)
        self.coordinates = [self.x, self.y]
        self.rectangle = canvas.create_rectangle(self.coordinates[0], self.coordinates[1],
                                                 self.coordinates[0] + self.width,
                                                 self.coordinates[1] - self.height, fill=WALL_COLOR, tag='wall')

    def move_down(self):
        global over
        if not over:
            self.coordinates[1] += SPACE_SIZE
            canvas.move(self.rectangle, 0, SPACE_SIZE)

            if check_collisions(self, ball):
                game_over()
            else:
                window.after(WALL_SPEED, self.move_down)

def change_directions(new_ball_direction):
    global ball_direction
    ball_x, ball_y = ball.coordinates

    left_boundary = canvas_to_road + SPACE_SIZE
    right_boundary = canvas_to_road + ROAD_WIDTH

    if ball_direction == 'stay':
        if new_ball_direction == 'left' and ball_x > left_boundary:
            ball_direction = new_ball_direction
        elif new_ball_direction == 'right' and ball_x < right_boundary:
            ball_direction = new_ball_direction

def next_move(ball):
    ball_x, ball_y = ball.coordinates
    global ball_direction

    if ball_direction == 'left':
        ball_x -= SPACE_SIZE

    elif ball_direction == 'right':
        ball_x += SPACE_SIZE

    canvas.delete('ball')
    ball.coordinates = [ball_x, ball_y]
    canvas.create_oval(ball_x, ball_y, ball_x - SPACE_SIZE, ball_y - SPACE_SIZE, fill=BALL_COLOR, tag='ball')
    ball_direction = 'stay'

    window.after(SPEED, next_move, ball)

def create_wall():
    if len(walls) <= NUM_WALLS:
        for wall in walls:
            if wall.coordinates[1] >= screen_height:
                oldest_wall = walls.pop(-1)
                canvas.delete(oldest_wall.rectangle)

    new_wall = Wall()
    overlap = False
    for wall in walls:
        if (new_wall.x < wall.x + wall.width + SPACE_SIZE and
                new_wall.x + new_wall.width + SPACE_SIZE> wall.x and
                new_wall.y < wall.y + wall.height + SPACE_SIZE and
                new_wall.y + new_wall.height + SPACE_SIZE> wall.y):
            overlap = True
            break
    if not overlap:
        walls.insert(0, new_wall)
        new_wall.move_down()

    window.after(WALL_SPEED, create_wall)

def check_collisions(wall, ball):
    if wall.coordinates[0] <= ball.coordinates[0] <= wall.coordinates[0] + wall.width:
        if wall.coordinates[1] >= ball.coordinates[1] >= wall.coordinates[1] - wall.height:
            return True
        return False

    return False

def update_score():
    global score
    if not over:
        score += 1
        label.config(text='Score:{}'.format(score))

        window.after(1000, update_score)
    else:
        score = score

def game_over():
    global over

    over = True
    canvas.delete(ALL)
    ball.coordinates[1] = window_height + (2 * SPACE_SIZE)

    canvas.config(bg="black")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 50), text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Dodge Roll")
window.resizable(False, False)

score = 0
ball_direction = 'stay'

label = Label(window, text='Score:{}'.format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

window.update()

canvas_width = canvas.winfo_width()
canvas_to_road = (canvas_width-ROAD_WIDTH)//2
canvas.create_rectangle(canvas_to_road,
                        0,
                        canvas_to_road + ROAD_WIDTH,
                        ROAD_HEIGHT + SPACE_SIZE,
                        fill=ROAD_COLOR, outline="#000000", width=2)

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2) - (SPACE_SIZE/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_directions('left'))
window.bind('<Right>', lambda event: change_directions('right'))

ball = Ball()
walls = []
over = False
window.after(WALL_SPEED, create_wall)

next_move(ball)
if score > 20:
    WALL_SPEED += 100
    SPEED += 100
window.after(1000, update_score)

window.mainloop()