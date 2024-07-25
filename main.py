import pygame
import numpy as np
import json
import time
from tkinter.filedialog import askopenfilename

pygame.init()

#  ЦВеТА
WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
NOTES = {
    'do':15,
    're': 294,
    'mi': 329,
    'fa': 349,
    'sol': 392,
    'lya': 440,
    'si': 493,
}
#-----НАЗНАЧЕНИЕ КЛАВИШ ДЛЯ НОТ------

KEY_MAPPINGS = {
    pygame.K_z: 'do',
    pygame.K_x: 're',
    pygame.K_c: 'mi',
    pygame.K_v: 'fa',
    pygame.K_b: 'sol',
    pygame.K_n: 'lya',
    pygame.K_m: 'si',
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Piano")

font = pygame.font.Font(None, 36)

buttons = []
for i, (note, freq) in enumerate(NOTES.items()):
    button = pygame.Rect(i * 100, 0, 100, 200)
    buttons.append((button, note, freq))

open_button = pygame.Rect(10, 210, 100, 50)
play_button = pygame.Rect(120, 210, 100, 50)
stop_button = pygame.Rect(230, 210, 100, 50)

recording = False #  ЗАПИСЬ вкл/выкл
# перем для записи в массив 
last_note_time = 0
recorded_notes = []
file_number = 1
# МЕЙН КОД
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button, note, freq in buttons:
                if button.collidepoint(event.pos):
                    # ПРОИГРЫВАНИЕ ЗВУК НОТ
                    pygame.mixer.music.load(f"notes/{note}.wav")
                    pygame.mixer.music.play()
                    if recording:
                        current_time = time.time()
                        recorded_notes.append((note, current_time - last_note_time))
                        last_note_time = current_time
            if open_button.collidepoint(event.pos):
                # ДИАЛОГОВОЕ ОКНО
                file_name = askopenfilename(title="Выберите JSON файл", filetypes=[("JSON files", "*.json")])
                if file_name:
                    try:
                        with open(file_name, "r") as file:
                            recorded_notes = json.load(file)
                    except json.JSONDecodeError:
                        print("Invalid JSON file.")
            elif play_button.collidepoint(event.pos):
                # ЗВУК НОТ ПРИ ПРОСЛУШИВАНИЕ ЗЗАПИСИ
                for note, interval in recorded_notes:
                    pygame.mixer.music.load(f"notes/{note}.wav")
                    pygame.mixer.music.play()
                    time.sleep(interval)
            elif stop_button.collidepoint(event.pos):
                #  ОСТАНОВКА МУЗЫКИ ПРИ ПРОСЛУШИВАНИЕ ( P.S РАБОТАЕТ НО НЕ ТОЧНО )
                pygame.mixer.music.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key in KEY_MAPPINGS:
                note = KEY_MAPPINGS[event.key]
                freq = NOTES[note]
                #  ПРОИГРЫВАНИЕ НОТ
                pygame.mixer.music.load(f"notes/{note}.wav")
                pygame.mixer.music.play()
                if recording:
                    current_time = time.time()
                    recorded_notes.append((note, current_time - last_note_time))
                    last_note_time = current_time
            elif event.key == pygame.K_r:
                # ВКЛ/ВЫКЛ ЗАПИСИ
                recording = not recording
                if recording:
                    last_note_time = time.time()
                    recorded_notes = []
                else:
                    # СОХРАНЕНИЕ ЗАПИСАНЫХ НОТ
                    file_name = "music/record_" + str(file_number) + ".json"
                    while True:
                        try:
                            with open(file_name, "x") as file:
                                json.dump(recorded_notes, file)
                            break
                        except FileExistsError:
                            file_number += 1
                            file_name = "music/record_" + str(file_number) + ".json"


    # ОТОБРАЖЕНИЕ НА ЭКРАНЕ
    screen.fill(WHITE)
    for button, note, freq in buttons:
        pygame.draw.rect(screen, BLACK, button, 1)
        text = font.render(note, True, BLACK)
        screen.blit(text, (button.centerx - text.get_width() / 2, button.centery - text.get_height() / 2))
    pygame.draw.rect(screen, BLACK, open_button, 1)
    text = font.render("Open", True, BLACK)
    screen.blit(text, (open_button.centerx - text.get_width() / 2, open_button.centery - text.get_height() / 2))
    pygame.draw.rect(screen, BLACK, play_button, 1)
    text = font.render("Play", True, BLACK)
    screen.blit(text, (play_button.centerx - text.get_width() / 2, play_button.centery - text.get_height() / 2))
    pygame.draw.rect(screen, BLACK, stop_button, 1)
    text = font.render("Stop", True, BLACK)
    screen.blit(text, (stop_button.centerx - text.get_width() / 2, stop_button.centery - text.get_height() / 2))

    #  кругЛЫй шарик для отображения записи
    if recording:
        pygame.draw.circle(screen, RED, (WIDTH - 20, 20), 10)
    else:
        pygame.draw.circle(screen, GREEN, (WIDTH - 20, 20), 10)
    pygame.display.flip()
    
pygame.quit()
