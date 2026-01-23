import flet as ft
import csv
import random
import os

def main(page: ft.Page):
    # 強制設定基礎屬性，防止黑屏
    page.title = "皇翔單字機 2.0"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 先定義好 UI，不要放進 Try 裡面
    word_display = ft.Text("點擊下方按鈕", size=40, weight="bold", color="blue")
    mean_display = ft.Text("等待中...", size=20, color="black")
    error_info = ft.Text("", size=12, color="red")
    
    words = []

    def load_csv_data():
        nonlocal words
        # 測試多個可能路徑
        paths_to_check = ["vocabulary_full_list.csv", "assets/vocabulary_full_list.csv", "/assets/vocabulary_full_list.csv"]
        target_path = ""
        
        for p in paths_to_check:
            if os.path.exists(p):
                target_path = p
                break
        
        if not target_path:
            return "錯誤：找不到 CSV 檔案，請確認檔案已上傳到 GitHub 根目錄"

        # 嘗試編碼
        for enc in ['utf-8-sig', 'big5', 'utf-8', 'cp950']:
            try:
                with open(target_path, mode='r', encoding=enc) as f:
                    reader = csv.DictReader(f)
                    # 根據你提供的截圖欄位名稱
                    temp_list = [row for row in reader if row.get('單字 (Word)')]
                    if temp_list:
                        words = temp_list
                        return None
            except:
                continue
        return "錯誤：無法讀取 CSV 內容，請檢查欄位標頭"

    def handle_click(e):
        if words:
            pick = random.choice(words)
            # 對齊截圖中的欄位
            word_display.value = pick.get('單字 (Word)', '欄位出錯')
            mean_display.value = pick.get('中文翻譯', '無翻譯')
            error_info.value = f"成功載入 {len(words)} 個單字"
        else:
            error_info.value = "目前無單字資料"
        page.update()

    # 畫面先建立出來，不論讀取成功與否
    page.add(
        ft.Column(
            [
                ft.Text("Huangxiang Vocab", size=16, color="grey-600"),
                ft.Divider(),
                word_display,
                mean_display,
                ft.Container(height=40),
                ft.ElevatedButton("下一個單字", on_click=handle_click, width=200),
                ft.Container(height=20),
                error_info,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    
    # UI 出來後再偷偷跑讀取
    load_err = load_csv_data()
    if load_err:
        error_info.value = load_err
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
