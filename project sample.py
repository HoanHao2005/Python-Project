import pygame
import random

pygame.init()

# Các biến khác
# ...

# Thiết lập kích thước màn hình
screen_width = 600
screen_height = 375
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('th')

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
volume = 0.5

noel_x = 0
noel_y = 0
th_x = 0
th_y = 230
caythong_x = 550
caythong_y = 230
robot_x = 600
robot_y = random.randint(50,150)
robot_velocity = 13
x_velocity = 5
y_velocity = 8
score = 0
font = pygame.font.SysFont('san', 20)
font1 = pygame.font.SysFont('san', 40)
current_time = 0
time_interval = 1000
noel = pygame.image.load('background.jpg')
th = pygame.image.load('Santa_Claus.png')
caythong = pygame.image.load('tree.png')
robot = pygame.image.load('robot.png')
play_button = pygame.image.load('playbutton.png')  # Nút play
background = pygame.image.load('play_background.png')  # Hình ảnh background play
sound1 = pygame.mixer.Sound('jump.wav')
sound1.set_volume(0.5)
sound2 = pygame.mixer.Sound('point.wav')
sound2.set_volume(0.1)
sound3 = pygame.mixer.music.load('nhac.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
jump = False
running = True
pausing = False
game_started = False  # Biến cờ để theo dõi xem trò chơi đã bắt đầu hay chưa

# Cài đặt kích thước hình ảnh background
background = pygame.transform.scale(background, (screen_width, screen_height))

# Cài đặt kích thước hình ảnh nút play và vị trí
play_button = pygame.transform.scale(play_button, (100, 50))
play_button_rect = play_button.get_rect(center=(screen_width // 2, screen_height // 2))

def draw_start_screen():
    screen.blit(background, (0, 0))  # Vẽ background
    screen.blit(play_button, play_button_rect)  # Vẽ nút play

    # Hiển thị màn hình bắt đầu
    pygame.display.flip()

def handle_start_screen_events():
    global game_started
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_x, mouse_y):
                game_started = True
                return True

    return True

# Hiển thị màn hình bắt đầu
draw_start_screen()

# Vòng lặp chính
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_started:
            # Nếu trò chơi đã bắt đầu, xử lý sự kiện trong trò chơi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if th_y == 230:
                        pygame.mixer.Sound.play(sound1)
                        jump = True
                    if pausing:
                        noel_x = 0
                        noel_y = 0
                        th_x = 0
                        th_y = 230
                        caythong_x = 550
                        caythong_y = 230
                        x_velocity = 5
                        y_velocity = 7
                        score = 0
                        pausing = False
        else:
            # Nếu trò chơi chưa bắt đầu, chỉ xử lý sự kiện cho màn hình bắt đầu
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_x, mouse_y):
                    game_started = True

    if game_started:
        # Chỉ thực hiện khi trò chơi đã bắt đầu
        pygame.mixer.music.set_volume(volume)
        current_time += clock.get_time()
        if current_time >= time_interval:
            current_time = 0
            x_velocity += 0.1
        clock.tick(60)
        screen.blit(background, (0, 0))  # Vẽ background
        noel1_rect = screen.blit(noel, (noel_x, noel_y))
        noel2_rect = screen.blit(noel, (noel_x + 600, noel_y))
        score_txt = font.render('score:' + str(score), True, BLUE)
        screen.blit(score_txt, (5, 5))
        robot_x -= robot_velocity
        if noel_x + 600 <= 0:
            noel_x = 0
        caythong_x -= x_velocity
        if caythong_x <= -20:
            caythong_x = 600
            score += 1
        if robot_x <= -50:
            robot_x = 600
            robot_y = random.randint(50, 150)
            robot_velocity = random.randint(2, 5)
        screen.blit(robot, (robot_x, robot_y))
        if 230 >= th_y >= 80:
            if jump == True:
                th_y -= y_velocity
        else:
            jump = False
        if th_y < 230:
            if jump == False:
                th_y += y_velocity
        robot_rect = screen.blit(robot, (robot_x, robot_y))
        th_rect = screen.blit(th, (th_x, th_y))
        caythong_rect = screen.blit(caythong, (caythong_x, caythong_y))
        noel_x -= x_velocity
        if th_rect.colliderect(caythong_rect):
            pygame.mixer.Sound.play(sound2)
            pausing = True
            gameover_txt = font1.render('GAME OVER', True, RED)
            screen.blit(gameover_txt, (200, 100))
            x_velocity = 0
            y_velocity = 0
        if th_rect.colliderect(robot_rect):
            pygame.mixer.Sound.play(sound2)
            pausing = True
            gameover_txt = font1.render('GAME OVER', True, RED)
            screen.blit(gameover_txt, (200, 100))
            x_velocity = 0
            y_velocity = 0

    pygame.display.flip()
pygame.quit()
