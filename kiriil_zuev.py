import curses

def main(stdscr):
    # Инициализация
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Красный текст, черный фон
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Зеленый текст, черный фон

    # Отключаем отображение курсора
    curses.curs_set(0)
    stdscr.clear()

    # Текст для отображения
    text = "Привеssssssт, мир!"

    # Вывод текста с разными цветами на i-й и j-й позициях
    i, j = 2, 7  # Позиции для изменения цвета

    for idx, char in enumerate(text):
        if idx == i:
            stdscr.addch(0, idx, char, curses.color_pair(1))  # Красный цвет на позиции i
        elif idx == j:
            stdscr.addch(0, idx, char, curses.color_pair(2))  # Зеленый цвет на позиции j
        else:
            stdscr.addch(0, idx, char)  # Обычный цвет для остальных

    stdscr.refresh()
    stdscr.getch()  # Ожидание нажатия клавиши

# Запуск curses
curses.wrapper(main)
