import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 設定頁面基礎屬性
    page.title = "皇翔單字機"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.WHITE

    # 儲存單字的清單
    words = []
    
    # 檔案路徑與讀取邏輯
    csv_filename = "vocabulary_full_list.csv"
    
    def load_data():
        nonlocal words
        try:
            # 優先嘗試在當前目錄與 assets 目錄尋找檔案
            target_path = csv_filename if os.path.exists(csv_filename) else f"assets/{csv_filename}"
            
            if not os.path.exists(target_path):
                return f"找不到檔案: {csv_filename}"

            # 嘗試 UTF-8 編碼讀取
            try:
                with open(target_path, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    words = list(reader)
            except UnicodeDecodeError:
                # 如果 UTF-8 失敗，改用 Big5 (Excel 常見編碼)
                with open(target_path, mode='r', encoding='big5') as f:
                    reader = csv.DictReader(f)
                    words = list(reader)
            
            if not words:
                return "CSV 檔案內沒有資料"
            return None
        except Exception as e:
            return str(e)

    # 初始化讀取
    error_msg = load_data()

    # UI 元件定義
    word_display = ft.Text("點擊按鈕開始", size=45, weight="bold", color="blue")
    mean_display = ft.Text("", size=25, color="grey-700")
    status_display = ft.Text("Ready to Study", color="green-600")

    if error_msg:
        word_display.value = "讀取失敗"
        mean_display.value = error_msg
        mean_display.color = "red"

    def handle_next(e):
        if words:
            pick = random.choice(words)
            # 確保欄位名稱符合你的 CSV (word, meaning)
            word_display.value = pick.get('word', '無單字欄位')
            mean_display.value = pick.get('meaning', '無翻譯欄位')
            status_display.value = f"已載入 {len(words)} 個單字"
            page.update()

    # 建立畫面佈局
    page.add(
        ft.Column(
            [
                ft.Icon(ft.icons.AUTO_STORIES, size=50, color="blue-400"),
                ft.Text("Huangxiang Vocab Master", size=16, italic=True),
                ft.Divider(height=40, thickness=2),
                word_display,
                ft.Container(height=10),
                mean_display,
                ft.Container(height=50),
                ft.ElevatedButton(
                    content=ft.Text("下一個單字", size=20, weight="bold"),
                    on_click=handle_next,
                    style=ft.ButtonStyle(
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    width=250,
                ),
                ft.Container(height=20),
                status_display,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
