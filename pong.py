from lcd_display import LCD_1inch14
import time
import random

lcd = LCD_1inch14()

# Constants
WIDTH = lcd.width
HEIGHT = lcd.height
PADDLE_WIDTH = 6
PADDLE_HEIGHT = 30
BALL_SIZE = 5
WIN_SCORE = 3

# Game state
left_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
right_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 2
ball_dy = 2

score_left = 0
score_right = 0

prev_left_y = left_y
left_velocity = 0

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-2, 2])
    ball_dy = random.choice([-2, 2])
    while ball_dy == 0:
        ball_dy = random.choice([-2, 2])

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def draw_text_centered(text, y, color):
    x = (WIDTH - len(text) * 8) // 2
    lcd.text(text, x, y, color)

def draw():
    lcd.fill(lcd.black)

    # Middle net
    for i in range(0, HEIGHT, 10):
        lcd.fill_rect(WIDTH // 2 - 1, i, 2, 5, lcd.white)

    # Paddles
    lcd.fill_rect(5, left_y, PADDLE_WIDTH, PADDLE_HEIGHT, lcd.blue)
    lcd.fill_rect(WIDTH - 5 - PADDLE_WIDTH, right_y, PADDLE_WIDTH, PADDLE_HEIGHT, lcd.red)

    # Ball
    lcd.fill_rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE, lcd.white)

    # Score
    draw_text_centered(f"{score_left} : {score_right}", 5, lcd.white)

    lcd.show()

def show_win_screen(winner):
    lcd.fill(lcd.black)
    msg = "PLAYER WINS" if winner == "left" else "CPU WINS"
    draw_text_centered("GAME OVER", 40, lcd.white)
    draw_text_centered(msg, 60, lcd.white)
    draw_text_centered("PRESS MIDDLE", 85, lcd.white)
    draw_text_centered("TO RESTART", 100, lcd.white)
    lcd.show()

    # Wait for middle button
    while True:
        buttons = lcd.read_buttons()
        if buttons["MIDDLE"]:
            break
        time.sleep(0.1)

# Function to wait for the middle button to start the game
def wait_for_start():
    lcd.fill(lcd.black)
    draw_text_centered("PRESS MIDDLE TO START", HEIGHT // 2, lcd.white)
    lcd.show()

    # Wait for middle button press
    while True:
        buttons = lcd.read_buttons()
        if buttons["MIDDLE"]:
            break
        time.sleep(0.1)

# Main game loop
while True:
    # Wait for the user to press the middle button before starting
    wait_for_start()

    # Reset the game state
    left_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    right_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    score_left = 0
    score_right = 0
    reset_ball()

    # Game loop
    while True:
        buttons = lcd.read_buttons()

        # Move player
        if buttons["UP"] and left_y > 0:
            left_y -= 3
        if buttons["DOWN"] and left_y < HEIGHT - PADDLE_HEIGHT:
            left_y += 3

        left_velocity = left_y - prev_left_y
        prev_left_y = left_y

        # AI paddle
        if right_y + PADDLE_HEIGHT // 2 < ball_y and right_y < HEIGHT - PADDLE_HEIGHT:
            right_y += 2
        elif right_y + PADDLE_HEIGHT // 2 > ball_y and right_y > 0:
            right_y -= 2

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce top/bottom
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_dy = -ball_dy

        # Paddle collisions
        if (ball_x <= 5 + PADDLE_WIDTH and
            left_y <= ball_y <= left_y + PADDLE_HEIGHT):
            ball_dx = abs(ball_dx)
            ball_dy += left_velocity // 2
            ball_dy = clamp(ball_dy, -4, 4)

        if (ball_x + BALL_SIZE >= WIDTH - 5 - PADDLE_WIDTH and
            right_y <= ball_y <= right_y + PADDLE_HEIGHT):
            ball_dx = -abs(ball_dx)

        # Scoring
        if ball_x < 0:
            score_right += 1
            if score_right >= WIN_SCORE:
                show_win_screen("right")
                score_left = 0
                score_right = 0
            reset_ball()

        if ball_x > WIDTH:
            score_left += 1
            if score_left >= WIN_SCORE:
                show_win_screen("left")
                score_left = 0
                score_right = 0
            reset_ball()

        draw()
        time.sleep(0.016)
