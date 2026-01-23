import flet as ft
import csv
import random
import os
import time

def main(page: ft.Page):
    # 1. 最強力的基礎設定
    page.title = "HX Vocab"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.padding = 30
    
    # 建立 UI 元件預算
    word_display = ft.Text("載入中...", size=40, weight="bold", color="blue")
    mean_display = ft.Text("請稍候", size=20, color="black")
    log_text = ft.Text("Initializing...", size=10, color="grey")
    
    words = []

    # 2. 定義切換單字邏輯
    def next_word(e):
        if words:
            pick = random.choice(words)
            word_display.value = pick.get('單字 (Word)', '欄位出錯')
            mean_display.value = pick.get('中文翻譯', '無翻譯')
            page.update()

    # 3. 畫面佈局
    container = ft.Column(
        [
            ft.Text("皇翔單字機 2.0 (Stable)", size=12, color="grey-400"),
            ft.Divider(),
            word_display,
            mean_display,
            ft.Container(height=40),
            ft.ElevatedButton("下一個單字", on_click=next_word, width=200, height=50),
            ft.Container(height=20),
            log_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # 4. 強制渲染流程：先放容器，再刷新
    page.add(container)
    page.update() 
    
    # 延遲一下下，給 Nokia 系統一點反應時間
    time.sleep(0.5)

    # 5. 嘗試讀取資料
    csv_path = "vocabulary_full_list.csv"
    if not os.path.exists(csv_path):
        csv_path = f"assets/{csv_path}"

    if os.path.exists(csv_path):
        # 針對台灣 Excel 常用編碼進行循環嘗試
        for enc in ['cp950', 'utf-8-sig', 'big5', 'utf-8']:
            try:
                with open(csv_path, "r", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    words = [row for row in reader if row.get('單字 (Word)')]
                    if words:
                        word_display.value = "準備就緒"
                        mean_display.value = f"已讀取 {len(words)} 個單字"
                        log_text.value = f"Success with {enc}"
                        break
            except:
                continue
    else:
        log_text.value = "Error: CSV file not found in root or assets"
    
    page.update()

# 使用非同步方式啟動，這是解決白屏的關鍵
if __name__ == "__main__":
    ft.app(target=main)
