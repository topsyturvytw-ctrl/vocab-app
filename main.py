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

    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    pos_display = ft.Text("", size=18, italic=True, color="grey")
    mean_display = ft.Text("請選擇模式開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    total_info = ft.Text("", size=14)

    # 🔊 終極回歸：使用最純粹的 launch_url，完全不使用任何音訊控制項
    def speak_word(e):
        word = word_display.value
        if word in ["皇翔單字機", "練習結束", "無資料", "已重置"]: 
            return
        
        encoded_word = urllib.parse.quote(word)
        # 採用最不易被跨網域封鎖的 Google 語音連結
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={encoded_word}"
        
        # 直接由瀏覽器核心接管這個 URL，100% 不會引發 Flet 元件錯誤
        page.launch_url(tts_url)

    # 點擊英文單字亦可觸發 launch
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

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value in ["練習結束", "無資料"]: return
        
        w_id = f"{word_display.value}_{mean_
