import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(
        ft.Column([
            ft.Text("🎉 皇翔單字機 2.0 啟動成功！", size=25, weight="bold"),
            ft.Text("看到這行字，代表我們可以開始背單字了。", size=16),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main)
