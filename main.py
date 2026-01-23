import flet as ft
import csv
import random
import io

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
    word_display = ft.Text("載入中...", size=45, weight="bold", color="blue")
    mean_display = ft.Text("正在從雲端抓取單字...", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("", size=12)

    # 語音元件
    tts = ft.TextToSpeech()
    page.overlay.append(tts)

    def update_total_info():
        rem = page.client_storage.get("rem_list") or []
        forg = page.client_storage.get("forg_list") or []
        total_info.value = f"累計標記 -> O: {len(rem)} | X: {len(forg)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = w.get('單字 (Word)', '').strip() or list(w.values())[0]
            mean_val = w.get('中文翻譯', '').strip() or list(w.values())[1]
            word_display.value = word_val
            mean_display.value = mean_val
            stat_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            if tts and word_val: tts.speak(word_val)
            page.update()

    def mark(status):
        nonlocal current_index
        if not session_words: return
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
            word_display.value = "無紀錄"
            page.update()
        else:
            current_index = 0
            update_ui()

    # 先建立介面
    page.add(
        ft.Column([
            ft.Text("皇翔單字機 3.0 (Cloud)", size=18, weight="bold"),
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

    # --- 關鍵修正：使用網頁路徑抓取 CSV ---
    def load_csv(e=None):
        # 網頁版需要直接讀取 assets 下的檔案
        try:
            # 這是 Flet 網頁版讀取資源的標準路徑
            import requests
            # 自動偵測當前網址來獲取 CSV
            file_url = "vocabulary_full_list.csv" 
            with open(file_url, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                nonlocal all_words
                all_words = list(reader)
                word_display.value = "載入成功"
                mean_display.value = f"共 {len(all_words)} 個單字"
                update_total_info()
        except:
            # 如果直接讀取失敗，通常是因為網頁路徑環境
            word_display.value = "請點擊下方"
            mean_display.value = "選擇模式開始練習"
        page.update()

    # 啟動時先跑一次
    load_csv()

ft.app(target=main, assets_dir="assets")
