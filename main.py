import flet as ft
import csv
import random
import requests # 引入網路請求功能
import io

def main(page: ft.Page):
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    all_words = []
    session_words = []
    current_index = 0

    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    mean_display = ft.Text("點擊下方開始練習", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = w.get('單字 (Word)', '').strip() or list(w.values())[0]
            mean_val = w.get('中文翻譯', '').strip() or list(w.values())[1]
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            page.update()

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value == "完成練習": return
        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "完成練習"
            page.update()

    def start_session(mode):
        nonlocal session_words, current_index, all_words
        
        if not all_words:
            mean_display.value = "從雲端下載單字中..."
            page.update()
            try:
                # 【!!! 重要：請將下方網址中的 [你的帳號] 和 [專案名] 換成你自己的 !!!】
                # 這是直接抓取 GitHub 上的原始檔案路徑
                csv_url = "https://github.com/topsyturvytw-ctrl/vocab-app/blob/main/assets/vocabulary_full_list.csv"
                
                response = requests.get(csv_url)
                response.encoding = 'utf-8-sig'
                
                if response.status_code == 200:
                    f = io.StringIO(response.text)
                    all_words = list(csv.DictReader(f))
                else:
                    # 備援：如果雲端失敗，嘗試讀取本地 assets
                    with open("assets/vocabulary_full_list.csv", "r", encoding="utf-8-sig") as f:
                        all_words = list(csv.DictReader(f))
            except Exception as e:
                mean_display.value = f"讀取失敗：{str(e)}"
                page.update()
                return

        if all_words:
            session_words = random.sample(all_words, min(30, len(all_words)))
            current_index = 0
            update_ui()

    page.add(
        ft.Column([
            ft.Text("米米單字機 3.0", size=18, weight="bold"),
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
