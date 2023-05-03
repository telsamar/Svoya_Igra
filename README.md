# Своя Игра

## Описание

Своя Игра - это проект на языке программирования Python, который представляет собой простую игру-викторину, основанную на популярном теле-шоу "Своя Игра". В этой игре, участники должны отвечать на вопросы, разделенные на категории и сложность. Игра разработана с использованием библиотеки pygame для графического интерфейса.

## Особенности

- Поддержка от 2 до 5 игроков
- Возможность выбора игрока с помощью клика мышью
- Вопросы и ответы загружаются из файла questions.txt
- Игровое поле с кнопками для каждой категории и уровня сложности
- Отображение правильных и неправильных ответов зеленым и красным цветом соответственно
- Подсчет и отображение набранных игроками очков

## Установка и запуск

1. Установите Python (версия 3.6 и выше) на вашем компьютере, если он еще не установлен.
2. Установите библиотеку pygame, используя следующую команду:
```python
pip install pygame
```
3. Скачайте файлы проекта из репозитория и разместите их в одной директории.
4. Создайте текстовый файл questions.txt и заполните его вопросами и ответами в формате:
```python
Категория,Вопрос,Ответ
```
5. Запустите игру, выполнив следующую команду в терминале или командной строке:
```python
python main.py
```

## Как играть

1. Выберите количество игроков (от 2 до 5) и нажмите кнопку "Старт".
2. Для активации игрока кликните на его круг на игровом поле.
3. Активный игрок выбирает категорию и уровень сложности вопроса, кликая на соответствующую кнопку.
4. Ответьте на вопрос, вводя текст с клавиатуры и нажмите Enter.
5. Если ответ верный, игрок получит очки, если неверный - потеряет очки.
6. Продолжайте игру до тех пор, пока не закончатся все вопросы.