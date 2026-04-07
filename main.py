import flet as ft
from datetime import datetime
import os

FILE_NAME = "history.txt"


def main_page(page: ft.Page):
    page.title = 'Мое первое приложение'
    page.theme_mode = ft.ThemeMode.LIGHT

    text_hello = ft.Text(value='Hello Geeks')

    greeting_history = []
    favorites = []

    history_text = ft.Text(value='История приветствий: ')
    favorites_text = ft.Text(value='Избранные имена: ')

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            lines = f.readlines()
            greeting_history = [line.strip() for line in lines]
            history_text.value = "История приветствий:\n" + "\n".join(greeting_history)

    def save_to_file(text):
        with open(FILE_NAME, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def on_button_click(_):
        name = name_input.value

        def get_greeting():
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y:%m:%d - %H:%M:%S")
            return f"{formatted_time} - Привет, {name}!"

        if name:
            message = get_greeting()

            text_hello.value = message
            name_input.value = None

            greeting_history.append(message)
            history_text.value = "История приветствий\n" + "\n".join(greeting_history)

            save_to_file(message)

        else:
            text_hello.color = ft.Colors.RED
            text_hello.value = 'Введите имя'

        page.update()

    def add_to_favorites(_):
        if greeting_history:
            last_message = greeting_history[-1]

            name = last_message.split("Привет,")[-1].replace("!", "").strip()

            if name not in favorites:
                favorites.append(name)
                favorites_text.value = "Избранные имена:\n" + "\n".join(favorites)

        page.update()

    def clear_history(_):
        greeting_history.clear()
        history_text.value = 'История приветствий: '
        page.update()

    def toggle_theme(_):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    name_input = ft.TextField(
        on_submit=on_button_click,
        label='Введите имя',
        expand=True
    )

    send_button = ft.ElevatedButton(
        'send',
        icon=ft.Icons.SEND,
        on_click=on_button_click
    )

    theme_button = ft.IconButton(
        icon=ft.Icons.BRIGHTNESS_6,
        on_click=toggle_theme
    )

    clear_button = ft.ElevatedButton(
        'Очистить историю',
        on_click=clear_history
    )

    fav_button = ft.ElevatedButton(
        'Добавить в избранное',
        on_click=add_to_favorites
    )

    main_row = ft.Row([name_input, send_button, theme_button, fav_button])
    history_row = ft.Row([history_text, clear_button])

    page.add(text_hello, main_row, history_row, favorites_text)


ft.app(main_page)