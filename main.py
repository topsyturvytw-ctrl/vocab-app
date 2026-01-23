import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 針對 Android 13 的 UI 強制設定
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40

    word_display = ft.Text("點擊開始", size=40, weight="bold", color="blue")
    mean_display = ft.Text("準備就緒", size=20, color="black")
    debug_text = ft.Text("", size=10, color="grey")
    
    words = []

    def load_data():
        nonlocal words
        # 定義多種可能的編碼，包含你提到的 cp950
        target_encodings = ['cp950', 'utf-8-sig', 'big5', 'utf-8']
        file_name = "vocabulary_full_list.csv"
        
        # 尋找檔案
        path = file_name if os.path.exists(file_name) else f"assets/{file_name}"
        
        if not os.path.exists(path):
            return "錯誤：找不到檔案，請確認 CSV 已上傳"

        for enc in target_encodings:
            try:
                with open(path, "r", encoding=enc) as f:
                    # 使用 DictReader 處理標頭
                    reader = csv.DictReader(f)
                    # 匹配你截圖中的繁體中文標頭
                    temp = [row for row in reader if row.get('單字 (Word)')]
                    if temp:
                        words = temp
                        return f"成功載入 ({enc})"
            except Exception as e:
                continue
        return "錯誤：編碼不匹配 (嘗試過 CP950/UTF8)"

    def next_word(e):
        if words:
            pick = random.choice(words)
            word_display.value = pick.get('單字 (Word)', '欄位出錯')
            mean_display.value = pick.get('中文翻譯', '無翻譯')
        else:
            word_display.value = "無資料"
        page.update()

    # 先畫 UI，確保畫面不會白屏
    page.add(
        ft.Column(
            [
                ft.Text("Nokia G21 專用版", size=12, color="grey-400"),
                ft.Divider(),
                word_display,
                mean_display,
                ft.Container(height=50),
                ft.ElevatedButton("下一個單字", on_click=next_word, width=220, height=60),
                ft.Container(height=20),
                debug_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    
    # UI 顯示後才讀取
    status = load_data()
    debug_text.value = status
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
