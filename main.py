import flet as ft
import csv
import random
import io

# 1. 資料加載函數：這裡預留位置讓你貼上完整的 CSV 內容
def get_all_words():
    # 目前先放 5 個測試，成功後你可以把整個 CSV 內容貼在下面三個引號中間
    raw_csv_data = """單字 (Word),中文翻譯
abandon,放棄
ability,能力
aboard,在船(飛機/車)上
about,關於
above,在...上方"""
    
    f = io.StringIO(raw_csv_data.strip())
    return list(csv.DictReader(f))

def main(page: ft.Page):
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 初始化資料
    all_words = get_all_words()
    session_words = []
    current_index = 0
    rem_list = []
    forg_list = []

    # UI 元件
    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    mean_display = ft.Text("點擊按鈕開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("系統已就緒", size=14)

    def update_total_info():
        total_info.value = f"本次紀錄 -> O: {len(rem_list)} | X: {len(forg_list)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            # 這裡增加一個防錯，萬一 CSV 欄位名稱對不上，改抓前兩個欄位
            word_val = w.get('單字 (Word)') or list(w.values())[0]
            mean_val = w.get('中文翻譯') or list(w.values())[1]
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            page.update()

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value == "練習結束": return
        
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
            word_display.value = "練習結束"
            mean_display.value = "做得好！請重新開始"
            page.update()

    def start_session():
        nonlocal session_words, current_index
        if not all_words: return
        # 隨機抽取 30 個單字
        session_words = random.sample(all_words, min(30, len(all_words)))
        current_index = 0
        update_ui()

    # 建立介面（移除所有可能報錯的 Icon）
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
            ft.ElevatedButton("開始隨機 30 題", on_click=lambda _: start_session(), width=250),
        ], horizontal_alignment="center")
    )

ft.app(target=main)
