import flet as ft


def main(page: ft.Page):
    page.add(ft.Text("Привет, Flet!"))


ft.app(target=main, view=ft.AppView.WEB_BROWSER)  # Запуск в браузере
