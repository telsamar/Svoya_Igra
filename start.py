import pygame
import random

# Инициализация pygame
pygame.init()

# Определение размеров и цветов экрана
screen_width = 1200
screen_height = 800
white = (255, 255, 255)
blue = (0, 0, 255)
grey = (200, 200, 200)
green =  (0, 255, 0)
black = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Своя игра")

# Загрузка шрифтов
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

def read_questions_from_file(filename):
    questions = {}
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            category, question, answer = line.strip().split(",")
            if category not in questions:
                questions[category] = []
            questions[category].append({"question": question, "answer": answer})
    return questions

questions = read_questions_from_file("questions.txt")

def draw_player_circle(player, x, y, active, score):
    pygame.draw.circle(screen, blue if active else grey, (x, y), 50)

    # Центрирование текста "Человек {player}" внутри круга
    player_text = f"Человек {player}"
    player_text_surface = font_small.render(player_text, True, white if active else blue)
    player_text_rect = player_text_surface.get_rect(center=(x, y))
    screen.blit(player_text_surface, player_text_rect)

    # Выравнивание счета над кругом по центру по ширине
    score_text = f"{score}"
    score_text_surface = font_small.render(score_text, True, white)
    score_text_rect = score_text_surface.get_rect(center=(x, y - 70))
    screen.blit(score_text_surface, score_text_rect)


question_states = {}
for category in questions:
    question_states[category] = [None] * len(questions[category])

def draw_text(text, x, y, font_obj, color=white):
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

def wrap_text(text, font_obj, max_width):
    words = text.split(' ')
    lines = []
    current_line = words[0]

    for word in words[1:]:
        new_line = current_line + ' ' + word
        new_line_width, _ = font_obj.size(new_line)

        if new_line_width <= max_width:
            current_line = new_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines


def ask_question(category, question_index, active_player):
    q = questions[category][question_index]
    correct = False

    wrapped_question = wrap_text(f"Вопрос из категории '{category}': {q['question']}", font, screen_width - 50)
    line_spacing = 36
    answer_y = 50 + len(wrapped_question) * line_spacing

    user_answer = ""
    while not correct:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_answer.lower() == q["answer"].lower():
                        draw_text(f"Правильно. Молодец!!!", 50, answer_y + line_spacing, font)
                        question_states[category][question_index] = True
                        player_scores[active_player - 1] += (question_index + 1) * 100
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        return
                    else:
                        draw_text(f"Неправильно. Правильный ответ: {q['answer']}", 50, answer_y + line_spacing, font)
                        question_states[category][question_index] = False
                        player_scores[active_player - 1] -= (question_index + 1) * 100  # Уменьшаем счет игрока
                        pygame.display.flip()
                        pygame.time.delay(2000)
                        return
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode
        
        background_image_q = pygame.image.load("fon.jpg")
        background_image_q = pygame.transform.scale(background_image_q, (1200, 800))
        screen.blit(background_image_q, (0, 0))
        # screen.fill(black)
        for i, line in enumerate(wrapped_question):
            draw_text(line, 50, 50 + i * 36, font)
        draw_text("Ваш ответ: " + user_answer, 50, answer_y, font)
        pygame.display.flip()



def main():
    running = True
    active_player = None  # 1 или 2
    active_players = [False, False]  # Состояние кружков с человечками
    global player_scores
    player_scores = [0, 0]
    background_image = pygame.image.load("fon.jpg")
    background_image = pygame.transform.scale(background_image, (1200, 800))

    while running:
        screen.blit(background_image, (0, 0))

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
                                    active_player = None  # Сбрасываем значение активного игрока
                                    active_players = [False, False]  # Сбрасываем состояние активности игроков
                                    
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