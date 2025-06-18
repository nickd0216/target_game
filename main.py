import math
import random
import time
import pygame
from button import Button
from dropdown import Dropdown
pygame.init()
music_on = True
pygame.mixer.music.load("Fish.mp3")
pygame.mixer.music.set_volume(.05)
if music_on:
    pygame.mixer.music.play(-1)



WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = .2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
        
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

def draw(win, targets):
    pygame.draw.rect(win, BG_COLOR, (0, TOP_BAR_HEIGHT, WIDTH, HEIGHT - TOP_BAR_HEIGHT))

    for target in targets:
        target.draw(win)

    pygame.display.update()

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100 )
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")
    
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    restart_button = Button(WIDTH//2 - 175, 500, 150, 50, "Restart", LABEL_FONT, "green", "lightgreen")
    menu_button = Button(WIDTH//2 + 25, 500, 200, 50, "Back to Main Menu", LABEL_FONT, "blue", "lightblue")

    restart_button.draw(win)
    menu_button.draw(win)

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()
            if restart_button.is_clicked(event):
                return "restart"
            if menu_button.is_clicked(event):
                return "menu"

def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2

def main_menu(win):
    win.fill(BG_COLOR)
    title = LABEL_FONT.render("Aim Trainer Main Menu", 1, "white")
    win.blit(title, (get_middle(title), 100))

    play_button = Button(WIDTH//2 - 100, 300, 200, 50, "Play", LABEL_FONT, "blue", "lightblue")
    options_button = Button(WIDTH//2 - 100, 350, 200, 50, "Options", LABEL_FONT, "orange", "lightyellow")
    pygame.display.update()

    run = True
    while run:
        play_button.draw(win)
        options_button.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if play_button.is_clicked(event):
                run = False
            if options_button.is_clicked(event):
                options_menu(win)
                win.fill(BG_COLOR)  # Clear screen when returning
                title = LABEL_FONT.render("Aim Trainer Main Menu", 1, "white")
                win.blit(title, (get_middle(title), 100))

def options_menu(win):
    music_on = True
    run = True
    rainbow_colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
    
    dropdown = Dropdown(WIDTH//2 - 100, 100, 200, 40, LABEL_FONT, rainbow_colors, "lightgray", "darkgray")
    back_button = Button(WIDTH//2 - 100, 500, 200, 50, "Back", LABEL_FONT, "blue", "lightblue")
    music_button = Button(5, 5, 120, 30, "Music: On", LABEL_FONT, "gray", "lightgray")


    while run:
        win.fill(BG_COLOR)
        title = LABEL_FONT.render("Options Menu", 1, "white")
        win.blit(title, (get_middle(title), 100))

        dropdown.draw(win)
        back_button.draw(win)
        music_button.draw(win)

        Target.COLOR = dropdown.selected


        selected_color = dropdown.selected
        selected_label = LABEL_FONT.render(f"Selected Color: {selected_color}", 1, "white")
        win.blit(selected_label, (get_middle(selected_label), 50))

        music_button.text = "Music: On" if music_on else "Music: Off"
        music_button.draw(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if music_button.is_clicked(event):
                music_on = not music_on
                if music_on:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause()
            
            dropdown.handle_event(event)
            if not dropdown.expanded and back_button.is_clicked(event):
                run = False

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            return end_screen(WIN, elapsed_time, target_pressed, clicks)
            

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()

while True:
        main_menu(WIN)
        result = main()

        if result == "menu":
            continue 
        elif result == "restart":
            result = main()
            while result == "restart":
                result = main()