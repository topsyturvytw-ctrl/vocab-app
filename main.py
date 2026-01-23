import flet as ft
import csv
import random
import os
import time

def main(page: ft.Page):
    # 1. 基礎強制設定
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.padding = 20
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 狀態變數
    all_words = []
    session_words = []
    current_index = 0
    
    # 語音元件先設為 None，延後初始化
    tts = ft.TextToSpeech()
    page.overlay.append(tts)

    # UI 元件
    word_display = ft.Text("單字載入中", size=45, weight="bold", color="blue")
    mean_display = ft.Text("請稍候...", size=24, color="black")
    progress_text = ft.Text("", size=14, color="grey")
    total_stats = ft.Text("正在讀取進度...", size=12)

    # 核心邏輯
    def start_session(mode="random"):
        nonlocal session_words, current_index
        if not all_words: return
        
        if mode == "random":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_x":
            forgotten_ids = page.client_storage.get("forgotten") or []
            session_words = [w for w in all_words if w.get('單字 (Word)', '').strip() in forgotten_ids]
            if not session_words:
                word_display.value = "目前無 X 紀錄"
                page.update()
                return
        
        current_index = 0
        update_ui()

    def update_ui():
        if session_words:
            w_obj = session_words[current_index]
            word = ""
            meaning = ""
            # 欄位自動清洗匹配
            for k, v in w_obj.items():
                k_clean = k.strip() if k else ""
                if "單字" in k_clean or "Word" in k_clean: word = v
                if "翻譯" in k_clean or "meaning" in k_clean: meaning = v
            
            word_display.value = word
            mean_display.value = meaning
            progress_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            
            # 安全語音調用
            try:
                if word: tts.speak(word)
            except:
                pass
            page.update()

    def mark_action(is_remembered):
        nonlocal current_index
        w_id = word_display.value.strip()
        rem = page.client_storage.get("remembered") or []
        forg = page.client_storage.get("forgotten") or []

        if is_remembered:
            if w_id not in rem: rem.append(w_id)
            if w_id in forg: forg.remove(w_id)
        else:
            if w_id not in forg: forg.append(w_id)
            if w_id in rem: rem.remove(w_id)
        
        page.client_storage.set("remembered", rem)
        page.client_storage.set("forgotten", forg)
        total_stats.value = f"累計紀錄 - O: {len(rem)} | X: {len(forg)}"
        
        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "單元完成"
            mean_display.value = "請再抽 30 題"
            page.update()

    # 建立畫面佈局
    main_layout = ft.Column(
        [
            ft.Text("皇翔單字機 3.0", size=16, weight="bold", color="grey"),
            total_stats,
            ft.Divider(),
            progress_text,
            word_display,
            mean_display,
            ft.Container(height=20),
            ft.Row([
                ft.ElevatedButton("O 記得", on_click=lambda _: mark_action(True), bgcolor="green", color="white", width=130),
                ft.ElevatedButton("X 忘記", on_click=lambda _: mark_action(False), bgcolor="red", color="white", width=130),
            ], alignment="center"),
            ft.Container(height=30),
            ft.Row([
                ft.OutlinedButton("隨機 30 題", on_click=lambda _: start_session("random")),
                ft.OutlinedButton("複習 X", on_click=lambda _: start_session("review_x")),
            ], alignment="center"),
            ft.TextButton("重製所有紀錄", on_click=lambda _: page.client_storage.clear())
        ],
        horizontal_alignment="center",
    )

    page.add(main_layout)
    page.update()

    # 延遲讀取檔案，確保 UI 已經畫在畫面上
    time.sleep(1)
    
    csv_path = "vocabulary_full_list.csv"
    if not os.path.exists(csv_path): csv_path = f"assets/{csv_path}"
    
    if os.path.exists(csv_path):
        for enc in ['utf-8-sig', 'cp950', 'big5', 'utf-8']:
            try:
                with open(csv_path, "r", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    all_words = list(reader)
                    if all_words:
                        rem = page.client_storage.get("remembered") or []
                        forg = page.client_storage.get("forgotten") or []
                        total_stats.value = f"累計紀錄 - O: {len(rem)} | X: {len(forg)}"
                        word_display.value = "準備就緒"
                        mean_display.value = "請選擇測驗模式"
                        break
            except: continue
    
    page.update()

ft.app(target=main)
