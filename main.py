import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 狀態變數 (暫存於記憶體，重新整理網頁會歸零)
    all_words = []
    session_words = []
    current_index = 0
    rem_list = []
    forg_list = []

    # UI 元件
    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    mean_display = ft.Text("請按下方按鈕開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("準備就緒", size=14)

    def update_total_info():
        total_info.value = f"本次練習 -> 記得(O): {len(rem_list)} | 忘記(X): {len(forg_list)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            # 兼容你的 CSV 標頭
            word_val = w.get('單字 (Word)', '').strip() or list(w.values())[0]
            mean_val = w.get('中文翻譯', '').strip() or list(w.values())[1]
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            page.update()

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value == "完成練習": return
        
        w_id = word_display.value
        if status == "O":
            if w_id not in rem_list: rem_list.append(w_id)
        else:
            if w_id not in forg_list: forg_list.append(w_id)
        
        update_total_info()

        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "完成練習"
            mean_display.value = "請重新選擇模式"
            page.update()

    def start_session(mode):
        nonlocal session_words, current_index, all_words
        
        # 讀取 CSV
        if not all_words:
            try:
                # 因為你的檔案在 assets 資料夾
                csv_path = "assets/vocabulary_full_list.csv"
                with open(csv_path, "r", encoding="utf-8-sig") as f:
                    all_words = list(csv.DictReader(f))
            except:
                mean_display.value = "讀取失敗，請確認檔案位置"
                page.update()
                return

        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        
        current_index = 0
        update_ui()

    page.add(
        ft.Column([
            ft.Text("皇翔單字機 3.0", size=18, weight="bold"),
            total_info,
            ft.Divider(),
            word_display,
            mean_display,
            stat_text,
            ft.Row([
                ft.ElevatedButton("O 記得", on_click=lambda _: mark("O"), bgcolor="green", color="white", width=120),
                ft.ElevatedButton("X 忘記", on_click=lambda _: mark("X"), bgcolor="red", color="white", width=120),
            ], alignment="center"),
            ft.Container(height=20),
            ft.Row([
                ft.OutlinedButton("隨機30題", on_click=lambda _: start_session("30")),
            ], alignment="center"),
        ], horizontal_alignment="center")
    )

ft.app(target=main, assets_dir="assets")
