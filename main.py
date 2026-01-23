import flet as ft

def main(page: ft.Page):
    # 強制設定頁面屬性，避免黑屏
    page.title = "HX Vocab Test"
    page.window_width = 400
    page.window_height = 800
    page.bgcolor = ft.colors.WHITE  # 強制背景白色，避免看起來像黑屏
    
    # 加入最單純的內容
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Hello! 皇翔單字機", size=30, color="blue", weight="bold"),
                        ft.Text("環境測試中...", size=20, color="black"),
                        ft.ElevatedButton("成功點擊測試", on_click=lambda _: print("OK")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
