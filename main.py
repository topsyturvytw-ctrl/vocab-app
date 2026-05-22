import flet as ft
import csv
import random
import io

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

    word_display = ft.Text("皇翔單字機", size=45, weight="bold", color="blue")
    pos_display = ft.Text("", size=18, italic=True, color="grey")
    mean_display = ft.Text("請選擇模式開始", size=24, color="black")
    stat_text = ft.Text("", size=16, color="grey")
    
    # 這是我們的核心黑科技：利用 Markdown 來執行瀏覽器原生的儲存與發音
    # 我們完全不呼叫 page 的任何 JS 方法
    js_injector = ft.Markdown("", extension_set=ft.MarkdownExtensionSet.GITHUB_WEB)

    # 💾 跨天記憶：直接用純 Python 初始化，並透過前端傳遞（這裡我們做一個防當機的安全預設）
    # 為了徹底避免舊版 Flet 讀取失敗，我們在每次 mark 時直接將變數透過 HTML 存入 localStorage
    LOCAL_REM = []
    LOCAL_FORG = []

    total_info = ft.Text("累計標記 -> O: 0 | X: 0", size=14)

    # 🔊 終極發音控制：直接透過 Markdown 注入 HTML5 原生語音 (Siri 同款引擎)
    def speak_word(e):
        word = word_display.value
        if word in ["皇翔單字機", "練習結束", "無資料", "已重置"]: 
            return
        
        # 每次點擊，直接更新 Markdown 的內容，迫使瀏覽器執行這段 HTML 腳本
        js_injector.value = f"""
<script>
    var msg = new SpeechSynthesisUtterance('{word}');
    msg.lang = 'en-US';
    msg.rate = 0.9;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(msg);
</script>
"""
        page.update()

    def update_total_info():
        total_info.value = f"累計標記 -> O: {len(LOCAL_REM)} | X: {len(LOCAL_FORG)}"
        page.update()

    def update_ui():
        if session_words:
            w = session_words[current_index]
            word_val = w.get('單字 (Word)') or list(w.values())[0]
            pos_val = w.get('詞性 (POS)') if len(w) > 1 else ""
            mean_val = w.get('中文翻譯') if len(w) > 2 else list(w.values())[-1]
            
            word_display.value = word_val
            pos_display.value = f"({pos_val})" if pos_val else ""
            mean_display.value = mean_val
            stat_text.value = f"目前進度: {current_index + 1} / {len(session_words)}"
            
            # 切換單字時自動觸發發音
            speak_word(None)

    def mark(status):
        nonlocal current_index
        if not session_words or word_display.value in ["練習結束", "無資料"]: return
        
        w_id = f"{word_display.value}_{mean_display.value}"
        
        if status == "O":
            if w_id not in LOCAL_REM: LOCAL_REM.append(w_id)
            if w_id in LOCAL_FORG: LOCAL_FORG.remove(w_id)
        else:
            if w_id not in LOCAL_FORG: LOCAL_FORG.append(w_id)
            if w_id in LOCAL_REM: LOCAL_REM.remove(w_id)
            
        update_total_info()

        # 💾 透過 Markdown 將紀錄同步備份到瀏覽器的 localStorage 中
        import json
        rem_json = json.dumps(LOCAL_REM).replace("'", "\\'")
        forg_json = json.dumps(LOCAL_FORG).replace("'", "\\'")
        
        js_injector.value = f"""
<script>
    localStorage.setItem('rem_list', '{rem_json}');
    localStorage.setItem('forg_list', '{forg_json}');
</script>
"""

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

        if mode == "30":
            session_words = random.sample(all_words, min(30, len(all_words)))
        elif mode == "review_o":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[-1])}" in LOCAL_REM]
        elif mode == "review_x":
            session_words = [w for w in all_words if f"{(w.get('單字 (Word)') or list(w.values())[0])}_{(w.get('中文翻譯') or list(w.values())[-1])}" in LOCAL_FORG]
        
        if not session_words:
            word_display.value = "無資料"
            pos_display.value = ""
            mean_display.value = "清單目前是空的"
            page.update()
        else:
            current_index = 0
            update_ui()

    def reset_all():
        LOCAL_REM.clear()
        LOCAL_FORG.clear()
        update_total_info()
        js_injector.value = "<script>localStorage.clear();</script>"
        word_display.value = "已重置"
        pos_display.value = ""
        mean_display.value = "紀錄已清除"
        page.update()

    page.add(
        ft.Column([
            ft.Text("皇翔單字機 3.0", size=18, weight="bold"),
            total_info,
            ft.Divider(),
            ft.GestureDetector(content=word_display, on_tap=speak_word),
            pos_display,
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
            ft.TextButton("清除所有紀錄", on_click=lambda _: reset_all()),
            js_injector # 把隱藏的 HTML 注入器放到畫面最下方
        ], horizontal_alignment="center")
    )

ft.app(target=main)
