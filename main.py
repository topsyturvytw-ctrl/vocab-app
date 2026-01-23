import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 狀態變數
    all_words = []
    session_words = []
    current_index = 0

    # UI 元件
    word_display = ft.Text("點擊下方開始", size=45, weight="bold", color="blue")
    mean_display = ft.Text("系統載入中...", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("", size=12)

    def update_total_info():
        # 網頁版儲存機制
        rem = page.client_storage.get("rem_list") or []
        forg = page.client_storage.get("forg_list") or []
        total_info.value = f"累計標記 -> O: {len(rem)} | X: {len(forg)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            # 兼容各種 CSV 標頭名稱
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
        rem = page.client_storage.get("rem_list") or []
        forg = page.client_storage.get("forg_list") or []

        if status == "O":
            if w_id not in rem: rem.append(w_id)
            if w_id in forg: forg.remove(w_id)
        else:
            if w_id not in forg: forg.append(w_id)
            if w_id in rem: rem.remove(w_id)
        
        page.client_storage.set("rem_list", rem)
        page.client_storage.set("forg_list", forg)
        update_total_info()

        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "完成練習"
            mean_display.value = "請重新選擇模式"
            page.update()

    def start_session(mode):
        nonlocal session_words, current_index
        if not all_words: return
        
        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_x":
            recs_forg = page.client_storage.get("forg_list") or []
            session_words = [w for w in all_words if w.get('單字 (Word)', '').strip() in recs_forg]
        
        if not session_words:
            word_display.value = "目前無紀錄"
            mean_display.value = "請先玩隨機30題"
            page.update()
        else:
            current_index = 0
            update_ui()

    # 建立介面
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
                ft.OutlinedButton("複習 X", on_click=lambda _: start_session("review_x")),
            ], alignment="center"),
            ft.TextButton("清除紀錄", on_click=lambda _: [page.client_storage.clear(), update_total_info()])
        ], horizontal_alignment="center")
    )

    # 讀取 CSV
    csv_file = "vocabulary_full_list.csv"
    try:
        with open(csv_file, "r", encoding="utf-8-sig") as f:
            all_words = list(csv.DictReader(f))
            word_display.value = "載入成功"
            mean_display.value = f"共 {len(all_words)} 個單字"
            update_total_info()
    except:
        word_display.value = "讀取失敗"
        mean_display.value = "請確認 CSV 檔案路徑"
    
    page.update()

ft.app(target=main)
