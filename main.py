import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 1. 基礎強制設定：解決白屏問題
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "white"
    page.window_always_on_top = True
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    # 2. 先把 UI 物件宣告出來
    word_text = ft.Text("單字載入中...", size=40, color="blue", weight="bold")
    mean_text = ft.Text("請稍候", size=20, color="black")
    msg_text = ft.Text("系統準備就緒", size=12, color="green")
    
    words_data = []

    # 3. 定義抓取單字的動作
    def get_next(e):
        if words_data:
            p = random.choice(words_data)
            word_text.value = p.get('單字 (Word)', '欄位出錯')
            mean_text.value = p.get('中文翻譯', '無翻譯')
        else:
            msg_text.value = "目前無資料，請確認 CSV 是否上傳"
        page.update()

    # 4. 立即把畫面塞進去，確保一開機有東西
    page.add(
        ft.Column(
            [
                ft.Icon(ft.icons.CHURCH, color="gold", size=50), # 皇翔建設風格圖示
                ft.Text("皇翔專屬單字機 2.0", size=16),
                ft.Divider(),
                word_text,
                mean_text,
                ft.Container(height=40),
                ft.ElevatedButton("下一個", on_click=get_next, width=200, height=50),
                ft.Container(height=20),
                msg_text,
            ],
            horizontal_alignment="center",
        )
    )
    page.update()

    # 5. 畫面出來後，才開始讀取檔案
    csv_name = "vocabulary_full_list.csv"
    try:
        # 搜尋檔案
        actual_path = csv_name if os.path.exists(csv_name) else f"assets/{csv_name}"
        
        if os.path.exists(actual_path):
            # 嘗試編碼解決你的 0xb3 報錯
            for c in ['utf-8-sig', 'big5', 'cp950']:
                try:
                    with open(actual_path, "r", encoding=c) as f:
                        reader = csv.DictReader(f)
                        words_data = [r for r in reader if r.get('單字 (Word)')]
                        if words_data:
                            msg_text.value = f"成功載入 {len(words_data)} 個皇翔精選單字"
                            msg_text.color = "blue"
                            break
                except:
                    continue
        else:
            msg_text.value = "錯誤：根目錄找不到 vocabulary_full_list.csv"
            msg_text.color = "red"
    except Exception as ex:
        msg_text.value = f"系統錯誤: {str(ex)}"
        msg_text.color = "red"
    
    page.update()

ft.app(target=main)
