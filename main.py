import flet as ft
import csv
import random
import io
import urllib.parse

def get_all_words():
    # 請在此貼上你完整 2127 個單字的 CSV 內容
    raw_csv_data = """單字 (Word),詞性 (POS),中文翻譯
abandon,v.,放棄
ability,n.,能力
aboard,adv./prep.,在船(飛機/車)上
about,prep./adv.,關於
above,prep./adv.,在...上方"""
    
    f = io.StringIO(raw_csv_data.strip())
    return list(csv.DictReader(f))

def main(page: ft.Page):
    page.title = "皇翔單字機 3.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.padding = 20

    all_words = get_all_words()
    session_words = []
    current_index = 0
    
    def get_storage(key):
        try: return page.get_client_storage().get(key) or []
        except: return []

    def set_storage(key, value):
        try: page.get_client_storage().set(key, value)
        except: pass

    # 🔊 1. 建立標準 Flet 網頁音訊播放器
    audio_player = ft.Audio(src="", autoplay=False)
    page.overlay.append(audio_player) # 放入網頁最底層

    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    pos_display = ft.Text("", size=18, italic=True, color="grey")
    mean_display = ft.Text("請選擇模式開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("", size=14)

    # 🔊 2. 純 Python 原生發音控制（完全不用 JavaScript）
    def speak_word(e):
        word = word_display.value
        if word in ["皇翔單字機", "練習結束", "無資料", "已重置"]: 
            return
        
        encoded_word = urllib.parse.quote(word)
        # 使用 Google 翻譯的官方公開發音 API（tl=en 代表美式英文），這個來源對網頁版的支援度最穩定
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={encoded_word}"
        
        # 透過 Flet 標準屬性更換聲音網址並播放
        audio_player.src = tts_url
        audio_player.play()

    # 綁定點擊單字發音
    word_click_container = ft.GestureDetector(
        content=word_display,
        on_tap=speak_word,
    )

    def update_total_info():
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")
        total_info.value = f"累計標記 -> O: {len(rem)} | X: {len(forg)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = w.get('單字 (Word)') or list(w.values())[0]
            pos_val = w.get('詞性 (POS)') or list(w.values())[1]
            mean_val = w.get('中文翻譯') or list(w.values())[2]
            
            word_display.value = word_val
            pos_display.value = f"({pos_val})" if pos_val else ""
            mean_display.value = mean_val
            stat_text.value = f"目前進度: {current_index + 1} / {len(session_words)}"
            page.update()
            
            # 切換單字時，嘗試在背景自動放音
            speak_word(None)

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value in ["練習結束", "無資料"]: return
        
        w_id = f"{word_display.value}_{mean_display.value}"
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")
        
        if status == "O":
            if w_id not in rem: rem.append(w_id)
            if w_id in forg: forg.remove(w_id)
        else:
            if w_id not in forg: forg.append(w_id)
            if w_id in rem: rem.remove(w_id)
            
        set_storage("rem_list", rem)
        set_storage("forg_list", forg)
        update_total_info()

        if current_index < len(session_words) - 1:
            current_index += 1
            update_ui()
        else:
            word_display.value = "練習結束"
            pos_display.value = ""
            mean_display.value = "切換模式繼續複習"
            page.update()

    def start_session(mode):
        nonlocal session_words, current_index
        if not all_words: return
        
        rem = get_storage("rem_list")
        forg = get_storage("forg_list")

        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_o":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[2])}" in rem]
        elif mode == "review_x":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[2])}" in forg]
        
        if not session_words:
            word_display.value = "無資料"
            pos_display.value = ""
            mean_display.value = "清單目前是空的"
            page.update()
        else:
            current_index = 0
            update_ui()

    def reset_all():
        try: page.get_client_storage().clear()
        except: pass
        update_total_info()
        word_display.value = "已重置"
        pos_display.value = ""
        mean_display.value = "紀錄已清除"
        page.update()

    page.add(
        ft.Column([
            ft.Text("皇翔單字機 3.0", size=18, weight="bold"),
            total_info,
            ft.Divider(),
            word_click_container,
            pos_display,
            # 大大的發音按鈕，點擊立刻發音
            ft.OutlinedButton("📢 點此聽發音", on_click=speak_word),
            mean_display,
            stat_text,
            ft.Container(height=10),
            ft.Row([
                ft.ElevatedButton("O 記得", on_click=lambda _: mark("O"), bgcolor="green", color="white"),
                ft.ElevatedButton("X 忘記", on_click=lambda _: mark("X"), bgcolor="red", color="white"),
            ], alignment="center"),
            ft.Divider(),
            ft.Row([
                ft.OutlinedButton("隨機 30 題", on_click=lambda _: start_session("30")),
                ft.OutlinedButton("複習 X", on_click=lambda _: start_session("review_x")),
                ft.OutlinedButton("複習 O", on_click=lambda _: start_session("review_o")),
            ], alignment="center"),
            ft.TextButton("清除所有紀錄", on_click=lambda _: reset_all())
        ], horizontal_alignment="center")
    )
    update_total_info()

ft.app(target=main)
