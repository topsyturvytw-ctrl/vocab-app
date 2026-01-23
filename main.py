import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    page.title = "皇翔單字機"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    
    # 單字庫
    words = []
    
    # 讀取 CSV 檔案
    try:
        # Flet 打包後，檔案會放在 assets 或是跟目錄
        csv_path = "vocabulary_full_list.csv"
        if not os.path.exists(csv_path):
            csv_path = "assets/vocabulary_full_list.csv"
            
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            words = list(reader)
    except Exception as e:
        page.add(ft.Text(f"讀取失敗: {e}", color="red"))
        return

    # UI 元件
    word_text = ft.Text("點擊下方開始", size=40, weight="bold")
    mean_text = ft.Text("", size=20, italic=True, color="grey")
    
    def next_word(e):
        if words:
            selected = random.choice(words)
            word_text.value = selected.get('word', 'N/A')
            mean_text.value = selected.get('meaning', '無翻譯')
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("皇翔存股必備單字", size=16, color="blue"),
                ft.Divider(),
                word_text,
                mean_text,
                ft.Container(height=40),
                ft.ElevatedButton(
                    "下一個單字", 
                    on_click=next_word,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )
    )

ft.app(target=main)
