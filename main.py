import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 強制設定淺色背景，確保文字看得見
    page.title = "皇翔單字機"
    page.bgcolor = ft.colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 定義顯示文字
    word_display = ft.Text("點擊下方開始", size=45, weight="bold", color="blue")
    mean_display = ft.Text("", size=25, color="grey-800")
    error_log = ft.Text("", color="red", size=12)

    words = []

    def load_words():
        nonlocal words
        csv_path = "vocabulary_full_list.csv"
        
        # 檢查路徑
        if not os.path.exists(csv_path):
            if os.path.exists(f"assets/{csv_path}"):
                csv_path = f"assets/{csv_path}"
            else:
                return f"找不到檔案: {csv_path}"

        # 嘗試編碼解決 utf-8 報錯
        for enc in ['utf-8-sig', 'big5', 'utf-8', 'cp950']:
            try:
                with open(csv_path, mode='r', encoding=enc) as f:
                    # 使用 DictReader 讀取
                    reader = csv.DictReader(f)
                    # 清洗資料：移除空白列
                    words = [row for row in reader if row.get('單字 (Word)')]
                    if words:
                        return None
            except:
                continue
        return "無法辨識 CSV 編碼，請確認檔案格式"

    def next_word(e):
        if words:
            pick = random.choice(words)
            # --- 關鍵修正：對齊你的 CSV 標頭名稱 ---
            # 根據 image_da2198.png 的欄位名稱
            word_display.value = pick.get('單字 (Word)', '欄位錯誤')
            mean_display.value = pick.get('中文翻譯', '無翻譯')
            page.update()

    # 執行載入
    err = load_words()
    if err:
        error_log.value = err
        # 提供一組備用資料確保 App 不會全白
        words = [{"單字 (Word)": "讀取失敗", "中文翻譯": err}]

    # 畫面佈局
    page.add(
        ft.Column(
            [
                ft.Text("HX Vocab Master", size=16, color="grey-500"),
                ft.Divider(height=50),
                word_display,
                ft.Container(height=10),
                mean_display,
                ft.Container(height=60),
                ft.ElevatedButton(
                    content=ft.Text("下一個單字", size=20),
                    on_click=next_word,
                    width=250,
                    height=60,
                ),
                ft.Container(height=20),
                error_log,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
