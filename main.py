import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 設定頁面：強制白底黑字，確保看得到內容
    page.title = "皇翔單字機"
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    word_display = ft.Text("點擊開始", size=45, weight="bold", color=ft.colors.BLUE)
    mean_display = ft.Text("", size=25, color=ft.colors.BLACK87)
    
    words = []

    def load_words():
        nonlocal words
        csv_path = "vocabulary_full_list.csv"
        
        # 尋找檔案路徑
        if not os.path.exists(csv_path):
            if os.path.exists(f"assets/{csv_path}"):
                csv_path = f"assets/{csv_path}"
            else:
                return False

        # 嘗試多種 Excel 常見編碼
        for enc in ['utf-8-sig', 'big5', 'utf-8', 'cp950']:
            try:
                with open(csv_path, mode='r', encoding=enc) as f:
                    reader = csv.DictReader(f)
                    # 這裡對齊你截圖中的 A 欄標頭
                    words = [row for row in reader if row.get('單字 (Word)')]
                    if words:
                        return True
            except:
                continue
        return False

    def next_word(e):
        if words:
            pick = random.choice(words)
            # 抓取 A 欄與 C 欄的資料
            word_display.value = pick.get('單字 (Word)', '找不到單字')
            mean_display.value = pick.get('中文翻譯', '無翻譯')
            page.update()

    # 執行讀取
    success = load_words()

    # 佈局
    page.add(
        ft.Column(
            [
                ft.Text("HX Vocab Master", size=14, color=ft.colors.GREY_400),
                ft.Divider(height=40),
                word_display,
                ft.Container(height=10),
                mean_display,
                ft.Container(height=60),
                ft.ElevatedButton(
                    content=ft.Text("下一個單字", size=20, weight="bold"),
                    on_click=next_word,
                    width=250,
                    height=60,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    
    if not success:
        word_display.value = "讀取失敗"
        mean_display.value = "請確認 CSV 檔案存在且標頭正確"
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
