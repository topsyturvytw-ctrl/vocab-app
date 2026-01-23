import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 1. 基礎強制設定 (極簡化)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 狀態變數 (不使用 client_storage 避免啟動崩潰，改用變數)
    all_words = []
    session_words = []
    current_index = 0
    rem_count = 0
    forg_count = 0

    # 2. UI 元件
    word_display = ft.Text("單字載入中", size=45, weight="bold", color="blue")
    mean_display = ft.Text("請稍候", size=24, color="black")
    stat_text = ft.Text("", size=16)

    def update_ui():
        if session_words:
            w = session_words[current_index]
            # 兼容標頭名稱
            word_val = ""
            mean_val = ""
            for k, v in w.items():
                k_c = k.strip() if k else ""
                if "單字" in k_c or "Word" in k_c: word_val = v
                if "翻譯" in k_c or "meaning" in k_c: mean_val = v
            
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"第 {current_index + 1} / 30 題 (O:{rem_count} X:{forg_count})"
            page.update()

    def mark(is_o):
        nonlocal current_index, rem_count, forg_count
        if is_o: rem_count += 1
        else: forg_count += 1
        
        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "單元結束"
            mean_display.value = f"本次成績: O={rem_count}"
            page.update()

    def start_game(e):
        nonlocal session_words, current_index, rem_count, forg_count
        if all_words:
            session_words = random.sample(all_words, min(30, len(all_words)))
            current_index = 0
            rem_count = 0
            forg_count = 0
            update_ui()

    # 3. 建立畫面 (先放最簡單的按鈕)
    page.add(
        ft.Column(
            [
                ft.Text("皇翔單字機 3.0 (安全模式)", size=12, color="grey"),
                word_display,
                mean_display,
                stat_text,
                ft.Row([
                    ft.ElevatedButton("O 記得", on_click=lambda _: mark(True), bgcolor="green", color="white"),
                    ft.ElevatedButton("X 忘記", on_click=lambda _: mark(False), bgcolor="red", color="white"),
                ], alignment="center"),
                ft.Container(height=20),
                ft.ElevatedButton("隨機抽 30 題", on_click=start_game, width=200),
            ],
            horizontal_alignment="center",
        )
    )

    # 4. 讀取 CSV
    path = "vocabulary_full_list.csv"
    if not os.path.exists(path): path = f"assets/{path}"
    
    if os.path.exists(path):
        for enc in ['utf-8-sig', 'cp950', 'big5', 'utf-8']:
            try:
                with open(path, "r", encoding=enc) as f:
                    all_words = list(csv.DictReader(f))
                    if all_words:
                        word_display.value = "已讀取成功"
                        mean_display.value = f"共 {len(all_words)} 字"
                        page.update()
                        break
            except: continue
    page.update()

ft.app(target=main)
