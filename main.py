import flet as ft
import csv
import random
import os
import time

def main(page: ft.Page):
    # 1. 基礎設定
    page.title = "皇翔單字機 - 學習管理版"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.padding = 20
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    tts = ft.TextToSpeech()
    page.overlay.append(tts)

    # 狀態變數
    all_words = []
    session_words = []
    current_index = 0
    
    # 從本地儲存讀取已記錄的清單
    remembered_ids = page.client_storage.get("remembered") or []
    forgotten_ids = page.client_storage.get("forgotten") or []

    # UI 元件
    word_display = ft.Text("請先選擇模式", size=45, weight="bold", color="blue")
    mean_display = ft.Text("", size=24, color="black")
    progress_text = ft.Text("", size=14, color="grey")
    total_stats = ft.Text(f"累計紀錄 - O: {len(remembered_ids)} | X: {len(forgotten_ids)}", size=12)

    # 2. 核心邏輯
    def start_session(mode="random"):
        nonlocal session_words, current_index
        if not all_words: return
        
        if mode == "random":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_x":
            # 只抽出當初標記為 X 的單字
            session_words = [w for w in all_words if w.get('單字 (Word)') in forgotten_ids]
            if not session_words:
                word_display.value = "目前沒有標記為 X 的單字"
                page.update()
                return
            random.shuffle(session_words)
        
        current_index = 0
        update_ui()

    def update_ui():
        if session_words:
            w_obj = session_words[current_index]
            word = ""
            meaning = ""
            for k, v in w_obj.items():
                k_clean = k.strip() if k else ""
                if "單字" in k_clean or "Word" in k_clean: word = v
                if "翻譯" in k_clean or "meaning" in k_clean: meaning = v
            
            word_display.value = word
            mean_display.value = meaning
            progress_text.value = f"進度: {current_index + 1} / {len(session_words)}"
            if word: tts.speak(word)
            page.update()

    def mark_action(is_remembered):
        nonlocal current_index
        w_id = word_display.value
        if is_remembered:
            if w_id not in remembered_ids: remembered_ids.append(w_id)
            if w_id in forgotten_ids: forgotten_ids.remove(w_id)
        else:
            if w_id not in forgotten_ids: forgotten_ids.append(w_id)
            if w_id in remembered_ids: remembered_ids.remove(w_id)
        
        # 存入手機儲存空間
        page.client_storage.set("remembered", remembered_ids)
        page.client_storage.set("forgotten", forgotten_ids)
        total_stats.value = f"累計紀錄 - O: {len(remembered_ids)} | X: {len(forgotten_ids)}"
        
        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "單元完成！"
            mean_display.value = "請選擇新模式"
            page.update()

    def reset_all_data(e):
        # 重製功能：清空所有紀錄
        nonlocal remembered_ids, forgotten_ids
        remembered_ids.clear()
        forgotten_ids.clear()
        page.client_storage.set("remembered", [])
        page.client_storage.set("forgotten", [])
        total_stats.value = "紀錄已重製"
        word_display.value = "已重製"
        page.update()

    # 3. 畫面佈局
    page.add(
        ft.Column(
            [
                ft.Text("皇翔單字機 3.0 - 學習管理", size=16, weight="bold"),
                total_stats,
                ft.Divider(),
                progress_text,
                word_display,
                mean_display,
                ft.Container(height=30),
                ft.Row(
                    [
                        ft.ElevatedButton("O 記得", on_click=lambda _: mark_action(True), bgcolor="green", color="white", width=120),
                        ft.ElevatedButton("X 忘記", on_click=lambda _: mark_action(False), bgcolor="red", color="white", width=120),
                    ],
                    alignment="center"
                ),
                ft.Container(height=40),
                ft.Row(
                    [
                        ft.OutlinedButton("隨機抽 30 題", on_click=lambda _: start_session("random")),
                        ft.OutlinedButton("複習 X 單字", on_click=lambda _: start_session("review_x")),
                    ],
                    alignment="center"
                ),
                ft.TextButton("重製所有紀錄", on_click=reset_all_data, font_style="italic", color="grey"),
            ],
            horizontal_alignment="center",
        )
    )

    # 4. 檔案讀取
    csv_path = "vocabulary_full_list.csv"
    if not os.path.exists(csv_path): csv_path = f"assets/{csv_path}"
    if os.path.exists(csv_path):
        for enc in ['utf-8-sig', 'cp950', 'big5', 'utf-8']:
            try:
                with open(csv_path, "r", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    all_words = list(reader)
                    if all_words: break
            except: continue
    page.update()

ft.app(target=main)
