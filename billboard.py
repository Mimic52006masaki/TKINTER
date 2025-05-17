import tkinter as tk
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

class BillboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Billboard Hot 100 書き込みアプリ")
        self.geometry("400x150")
        self.create_widgets()

        # スプレッドシート情報（必要に応じて変更してください）
        self.CREDENTIAL_FILE_PATH = '/Users/masaki/Desktop/【json】/gspread-test-408312-2072e3277dcd.json'
        self.SPREADSHEET_KEY = '1mF2nBRBPxeYog7YnBFy-1QNxDmjwUl5O2ZhqB6y7_Qw'
        self.WORKSHEET_NAME = 'Billboard'

    def create_widgets(self):
        self.label = tk.Label(self, text="Billboard Hot 100")
        self.label.pack(pady=10)

        self.button = tk.Button(self, text="実行", command=self.fetch_and_write)
        self.button.pack(pady=10)

    def fetch_and_write(self):
        try:
            # 認証
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIAL_FILE_PATH)
            gc = gspread.authorize(credentials)
            sh = gc.open_by_key(self.SPREADSHEET_KEY)
            worksheet = sh.worksheet(self.WORKSHEET_NAME)

            # Billboardのデータ取得
            url = 'https://www.billboard.com/charts/hot-100/'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            chart_results = soup.find_all('div', attrs={'class': 'o-chart-results-list-row-container'})
            data_list = []
            for chart_result in chart_results:
                rank = chart_result.find_all('span', attrs={'class': 'c-label'})[0].text.strip()
                rank = int(rank)
                title = chart_result.find_all('h3', attrs={'class': 'c-title'})[0].text.strip()
                artist_name = chart_result.find_all('span', class_='a-no-trucate')[0].text.strip()
                lastWeek = chart_result.find_all('span', class_='c-label')[2].text.strip()
                data_list.append([rank, title, artist_name, lastWeek])

            # 空白行5行分
            num_blank_rows = 0
            blank_rows = [[''] * len(data_list[0])] * num_blank_rows
            data_with_blanks = blank_rows + data_list

            # 書き込み範囲の計算
            start_row = 2
            total_rows = len(data_with_blanks)
            total_cols = len(data_with_blanks[0])
            end_col_letter = chr(ord('A') + total_cols - 1)
            end_row_number = start_row + total_rows - 1
            range_str = f'A{start_row}:{end_col_letter}{end_row_number}'

            # スプレッドシート更新
            worksheet.update(range_str, data_with_blanks)

            messagebox.showinfo("成功", "スプレッドシートにデータを書き込みました。")
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました:\n{e}")

if __name__ == '__main__':
    app = BillboardApp()
    app.mainloop()
