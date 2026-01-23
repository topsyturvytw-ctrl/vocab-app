import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 基礎設定
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 狀態變數
    all_words = []
    session_words = []
    current_index = 0
    
    # 建立紀錄檔案路徑
    record_file = os.path.join(page.utils.get_user_data_dir(), "hx_record.txt")

    # UI 元件
    word_display = ft.Text("單字載入中", size=45, weight="bold", color="blue")
    mean_display = ft.Text("請稍候", size=24, color="black")
    stat_text = ft.Text("請點擊下方模式開始", size=16, color="grey")
    total_info = ft.Text("", size=12)

    def get_records():
        """讀取長期紀錄：格式為 word|status"""
        records = {}
        if os.path.exists(record_file):
            with open(record_file, "r", encoding="utf-8") as f:
                for line in f:
                    if "|" in line:
                        w, s = line.strip().split("|")
                        records[w] = s
        return records

    def save_record(word, status):
        """儲存紀錄"""
        records = get_records()
        records[word] = status
        with open(record_file, "w", encoding="utf-8") as f:
            for w, s in records.items():
                f.write(f"{w}|{s}\n")
        update_total_info()

    def update_total_info():
        recs = get_records()
        os_count = list(recs.values()).count("O")
        xs_count = list(recs.values()).count("X")
        total_info.value = f"目前累計標記 -> 已記得(O): {os_count} | 忘記(X): {xs_count}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = ""
            mean_val = ""
            for k, v in w.items():
                k_c = k.strip() if k else ""
                if "單字" in k_c or "Word" in k_c: word_val = v
                if "翻譯" in k_c or "meaning" in k_c: mean_val = v
            
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"目前進度: {current_index + 1} / {len(session_words)}"
            page.update()

    def mark(status):
        nonlocal current_index
        if session_words:
            current_word = word_display.value
            save_record(current_word, status)
            
            if current_index < len(session_words) - 1:
                current_index += 1
                update_ui()
            else:
                word_display.value = "單元完成"
                mean_display.value = "請選擇下一個模式"
                page.update()

    def start_session(mode):
        nonlocal session_words, current_index
        recs = get_records()
        
        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_o":
            o_list = [w for w in all_words if recs.get(w.get('單字 (Word)', '').strip()) == "O"]
            session_words = o_list if o_list else []
        elif mode == "review_x":
            x_list = [w for w in all_words if recs.get(w.get('單字 (Word)', '').strip()) == "X"]
            session_words = x_list if x_list else []

        if not session_words:
            word_display.value = "尚無紀錄"
            mean_display.value = "請先進行隨機練習"
            page.update()
        else:
            current_index = 0
            update_ui()

    def reset_data(e):
        if os.path.exists(record_file):
            os.remove(record_file)
        update_total_info()
        word_display.value = "已清空紀錄"
        page.update()

    # 畫面佈局
    page.add(
        ft.Column(
            [
                ft.Text("皇翔單字管理系統", size=18, weight="bold"),
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
                    ft.OutlinedButton("複習 O", on_click=lambda _: start_session("review_o")),
                    ft.OutlinedButton("複習 X", on_click=lambda _: start_session("review_x")),
                ], alignment="center"),
                ft.TextButton("重製所有標記", on_click=reset_data, icon=ft.icons.DELETE_FOREVER),
            ],
            horizontal_alignment="center",
        )
    )

    # 讀取 CSV
    path = "vocabulary_full_list.csv"
    if not os.path.exists(path): path = f"assets/{path}"
    if os.path.exists(path):
        for enc in ['utf-8-sig', 'cp950', 'big5', 'utf-8']:
            try:
                with open(path, "r", encoding=enc) as f:
                    all_words = list(csv.DictReader(f))
                    if all_words:
                        word_display.value = "載入完成"
                        mean_display.value = f"共 {len(all_words)} 字"
                        update_total_info()
                        break
            except: continue
    page.update()

ft.app(target=main)
