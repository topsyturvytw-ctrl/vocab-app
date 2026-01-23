import flet as ft
import csv
import random
import os
import time

def main(page: ft.Page):
    page.title = "HX Vocab"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.padding = 30
    
    word_display = ft.Text("載入中...", size=40, weight="bold", color="blue")
    mean_display = ft.Text("請稍候", size=24, color="black") # 稍微放大翻譯文字
    log_text = ft.Text("Ready", size=10, color="grey")
    
    words = []

    def next_word(e):
        if words:
            pick = random.choice(words)
            # 這裡加入自動修剪功能，解決 CSV 欄位名稱有空格的問題
            # 我們同時嘗試多種可能的欄位寫法
            word = ""
            meaning = ""
            
            for k, v in pick.items():
                clean_key = k.strip() if k else ""
                if "單字" in clean_key or "Word" in clean_key:
                    word = v
                if "翻譯" in clean_key or "meaning" in clean_key:
                    meaning = v
            
            word_display.value = word if word else "找不到單字欄位"
            mean_display.value = meaning if meaning else "找不到翻譯欄位"
            page.update()

    container = ft.Column(
        [
            ft.Text("皇翔單字機 2.0 (Stable)", size=12, color="grey-400"),
            ft.Divider(),
            word_display,
            ft.Container(height=10),
            mean_display,
            ft.Container(height=50),
            ft.ElevatedButton("下一個單字", on_click=next_word, width=220, height=60),
            ft.Container(height=20),
            log_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(container)
    page.update() 
    time.sleep(0.3)

    # 讀取資料邏輯
    csv_path = "vocabulary_full_list.csv"
    if not os.path.exists(csv_path):
        csv_path = f"assets/{csv_path}"

    if os.path.exists(csv_path):
        # 針對台灣 Excel 常用編碼
        for enc in ['utf-8-sig', 'cp950', 'big5', 'utf-8']:
            try:
                with open(csv_path, "r", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    # 讀取時不進行過濾，先全部抓進來
                    words = list(reader)
                    if words:
                        word_display.value = "連線成功"
                        mean_display.value = f"已準備好 {len(words)} 個單字"
                        log_text.value = f"Encoded by {enc}"
                        break
            except:
                continue
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
