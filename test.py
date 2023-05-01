import pygame
import random

# Инициализация pygame
pygame.init()

# Определение размеров и цветов экрана
screen_width = 800
screen_height = 600
white = (255, 255, 255)
blue = (0, 0, 255)
grey = (200, 200, 200)

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Своя игра")

# Загрузка шрифтов
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Определение категорий и вопросов
questions = {
    "Математика": [
        {"question": "Сколько будет 2+2?", "answer": "4"},
        {"question": "Какой корень из 9?", "answer": "3"},
        {"question": "Сколько градусов в прямом угле?", "answer": "90"}
    ],
    "География": [
        {"question": "Столица Франции?", "answer": "Париж"},
        {"question": "На каком континенте находится Африка?", "answer": "Африка"},
        {"question": "Какой самый большой океан?", "answer": "Тихий"}
    ],
    "История": [
        {"question": "В каком году открылся первый макдоналдс в СССР?", "answer": "1990"},
        {"question": "Кто изобрел телефон?", "answer": "Александр Грэм Белл"},
        {"question": "Когда произошла Битва при Бородине?", "answer": "1812"}
    ]
}

def draw_player_circle(player, x, y, active, score):
    pygame.draw.circle(screen, blue if active else grey, (x, y), 50)
    draw_text(f"Человек {player}", x - 30, y - 10, font_small, white if active else blue)
    draw_text(f"{score}", x - 10, y - 70, font_small, blue)

question_states = {}
for category in questions:
    question_states[category] = [None] * len(questions[category])

def draw_text(text, x, y, font_obj, color=blue):
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(text, x, y, w, h, color=grey):
    pygame.draw.rect(screen, color, (x, y, w, h))
    draw_text(text, x + 10, y + 5, font_small)

def draw_circle(text, x, y, radius, color):
    pygame.draw.circle(screen, color, (x, y), radius)
    text_surface = font_small.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def ask_question(category, question_index, active_player):
    q = questions[category][question_index]
    correct = False

    draw_text(f"Вопрос из категории '{category}': {q['question']}", 50, 50, font)

    user_answer = ""
    while not correct:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_answer.lower() == q["answer"].lower():
                        draw_text(f"Правильно. Молодец!!!", 50, 150, font)
                        question_states[category][question_index] = True
                        player_scores[active_player - 1] += (question_index + 1) * 100
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        return
                    else:
                        draw_text(f"Неправильно. Правильный ответ: {q['answer']}", 50, 150, font)
                        question_states[category][question_index] = False
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        return
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode

        screen.fill(white)
        draw_text(f"Вопрос из категории '{category}': {q['question']}", 50, 50, font)
        draw_text("Ваш ответ: " + user_answer, 50, 100, font)
        pygame.display.flip()


def main():
    running = True
    active_player = None  # 1 или 2
    active_players = [False, False]  # Состояние кружков с человечками
    global player_scores
    player_scores = [0, 0]

    while running:
        screen.fill(white)

        # Рисуем кнопки для категорий и вопросов
        button_width = 150
        button_height = 50
        button_margin = 20
        total_width = len(questions) * button_width + (len(questions) - 1) * button_margin
        start_x = (screen_width - total_width) // 2

        for i, category in enumerate(questions.keys()):
            draw_text(category, start_x + i * (button_width + button_margin), 50, font)
            for j in range(len(questions[category])):
                button_color = grey
                if question_states[category][j] is True:
                    button_color = (0, 255, 0)  # Зеленый
                elif question_states[category][j] is False:
                    button_color = (255, 0, 0)  # Красный
                draw_button(str((j + 1) * 100), start_x + i * (button_width + button_margin), 100 + j * (button_height + button_margin), button_width, button_height, button_color)

        draw_player_circle(1, screen_width // 2 - 100, screen_height - 100, active_player == 1, player_scores[0])
        draw_player_circle(2, screen_width // 2 + 100, screen_height - 100, active_player == 2, player_scores[1])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Проверяем клик по кружкам с человечками
                for i in range(2):
                    circle_x = screen_width // 2 + (-100 if i == 0 else 100)
                    circle_y = screen_height - 100
                    if ((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2) <= 50 ** 2:
                        active_player = i + 1
                        active_players = [not active_players[i] if j == i else False for j in range(2)]

                # Если выбран активный игрок, проверяем клик по квадратикам с вопросами
                if active_player is not None:
                    for i, category in enumerate(questions.keys()):
                        for j in range(len(questions[category])):
                            button_x = start_x + i * (button_width + button_margin)
                            button_y = 100 + j * (button_height + button_margin)
                            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                                if question_states[category][j] is None:  # Только если вопрос еще не был отвечен
                                    screen.fill(white)
                                    ask_question(category, j, active_player)
                                    # Обновляем состояние кнопки в зависимости от ответа
                                    if question_states[category][j]:
                                        button_color = (0, 255, 0)  # Зеленый
                                    else:
                                        button_color = (255, 0, 0)  # Красный
                                    draw_button(str(j + 1), button_x, button_y, button_width, button_height, button_color)
                            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()



