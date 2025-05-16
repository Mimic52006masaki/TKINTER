import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

class MangaScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("まとめサイト Scraper")

        # スタイル設定
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 14, "bold"),
                        foreground="black", background="#4CAF50", padding=50)
        style.map("Custom.TButton", background=[("active", "#45a049")])

        self.label = tk.Label(root, text="取得対象のサイトを選択", font=("Helvetica", 12))
        self.label.pack(pady=10)

        # ラジオボタンでサイト選択
        self.site_var = tk.StringVar(value="manga")  # デフォルト
        tk.Radiobutton(root, text="漫画まとめ速報", variable=self.site_var, value="manga").pack()
        tk.Radiobutton(root, text="アニメまとめCH", variable=self.site_var, value="anime").pack()

        # 実行ボタン
        self.button = ttk.Button(
            root, text="実行", command=self.run_scraper, style="Custom.TButton", width=10)
        self.button.pack(pady=10)

    def run_scraper(self):
        try:
            # 認証とシート接続
            credentials_path = '/Users/masaki/Desktop/【json】/gspread-test-408312-2072e3277dcd.json'
            spreadsheet_key = '1mF2nBRBPxeYog7YnBFy-1QNxDmjwUl5O2ZhqB6y7_Qw'

            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path)
            gc = gspread.authorize(creds)
            sh = gc.open_by_key(spreadsheet_key)
            worksheet = sh.worksheet('python')

            # URLと処理を分岐
            site = self.site_var.get()
            if site == "manga":
                url = "https://anaguro.yanen.org/search.cgi?key=%e6%bc%ab%e7%94%bb%e3%81%be%e3%81%a8%e3%82%81%e9%80%9f%e5%a0%b1"
            else:
                url = "https://anaguro.yanen.org/search.cgi?c_10=1&c_11=1&c_15=1&c_16=1&c_17=1&c_20=1&c_24=1&c_30=1&c_31=1&c_40=1&c_41=1&c_45=1&c_51=1&c_60=1&c_61=1&c_63=1&c_70=1&c_95=1&c_99=1&type=month&key=%E3%82%A2%E3%83%8B%E3%83%A1%E3%81%BE%E3%81%A8%E3%82%81&btn=%E3%81%8A&chkb=1"

            # Webスクレイピング共通処理（分岐あり）
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            posts = soup.find_all('table', class_='table01')

            hr_post = []
            for post in posts:
                for row in post.find_all('tr'):
                    if row.find('hr'):
                        hr_post.append(row)

            data_list = []
            for titles in hr_post:
                title_elem = titles.find('td', class_='title')
                a_tag = titles.find('a', class_='title')

                if title_elem and a_tag:
                    title = title_elem.text.strip()
                    # URLの置換方法をサイトごとに分岐
                    if site == "manga":
                        url_A = a_tag['href'].replace('./cnt.cgi?1778=', '')
                    else:
                        url_A = a_tag['href'].replace('./cnt.cgi?1996=', '')
                    data_list.append([title, url_A])

            # 既存データ取得と追記
            existing_data = worksheet.get_all_values()
            num_existing_rows = len(existing_data)
            num_blank_rows = 5
            blank_rows = [[''] * len(existing_data[0])] * num_blank_rows
            data_with_blanks = blank_rows + data_list
            worksheet.append_rows(data_with_blanks, table_range=f'A{num_existing_rows + 1}')

            messagebox.showinfo("完了", f"{'漫画まとめ速報' if site == 'manga' else 'アニメまとめCH'}のデータを追加しました！")

        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {e}")

# GUIアプリ実行
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x250")
    app = MangaScraperApp(root)
    root.mainloop()
