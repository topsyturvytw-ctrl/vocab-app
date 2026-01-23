import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 1. 基礎設定：強制白色背景避免黑屏
    page.title = "皇翔單字機"
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. 建立顯示元件
    word_display = ft.Text("點擊開始", size=40, weight="bold", color=ft.colors.BLUE)
    mean_display = ft.Text("等待中...", size=20, color=ft.colors.BLACK54)
    error_log = ft.Text("", color=ft.colors.RED, size=12)

    words = []

    # 3. 強化版讀取邏輯
    def load_words():
        nonlocal words
        csv_path = "vocabulary_full_list.csv"
        
        # 檢查檔案是否存在
        if not os.path.exists(csv_path):
            if os.path.exists(f"assets/{csv_path}"):
                csv_path = f"assets/{csv_path}"
            else:
                return f"找不到檔案: {csv_path}"

        # 嘗試多種編碼順序：utf-8 -> big5 -> utf-8-sig (Excel 帶 BOM)
        encodings = ['utf-8', 'big5', 'utf-8-sig', 'cp950']
        last_error = ""
        
        for enc in encodings:
            try:
                with open(csv_path, mode='r', encoding=enc) as f:
                    reader = csv.DictReader(f)
                    words = [row for row in reader if row.get('word')]
                    if words:
                        return None # 讀取成功
            except Exception as e:
                last_error = str(e)
                continue
        return f"所有編碼嘗試失敗。最後錯誤: {last_error}"

    # 4. 點擊事件
    def next_word(e):
        if words:
            pick = random.choice(words)
            word_display.value = pick.get('word', '欄位錯誤')
            mean_display.value = pick.get('meaning', '無翻譯')
        else:
            word_display.value = "庫存為空"
        page.update()

    # 5. 執行載入
    err = load_words()
    if err:
        error_log.value = err
        # 備用資料，避免 App 變空殼
        words = [{"word": "Loading Error", "meaning": "請檢查 CSV 編碼"}]

    # 6. 建置畫面佈局
    page.add(
        ft.Column(
            [
                ft.Text("Huangxiang Study Tool", size=14, color=ft.colors.GREY_500),
                ft.Divider(),
                word_display,
                mean_display,
                ft.Container(height=30),
                ft.ElevatedButton(
                    "下一個單字", 
                    on_click=next_word,
                    width=200,
                    height=50
                ),
                ft.Container(height=20),
                error_log
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    page.update()

ft.app(target=main)
