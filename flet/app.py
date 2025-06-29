import flet as ft


def main(page: ft.Page):
    page.add(ft.Text("Привет, Flet!"))


# Запуск в браузере
# ft.app(target=main, view=ft.AppView.WEB_BROWSER)

# Запуск в десктоп окне
# ft.app(target=main)

# Запуск PWA
ft.app(target=main, view=ft.AppView.FLET_APP_WEB)
