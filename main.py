import flet as ft
import csv
import random

def main(page: ft.Page):
    # 設定基本的頁面參數
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 極簡 UI 確保能成功渲染
    page.add(
        ft.Column([
            ft.Text("皇翔單字機 已恢復", size=30, weight="bold"),
            ft.Text("如果看到這個畫面，請告訴我", size=16),
            ft.ElevatedButton("點擊測試", on_click=lambda _: print("OK"))
        ], horizontal_alignment="center")
    )
    page.update()

ft.app(target=main)
