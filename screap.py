import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import chardet
import gspread
from google.oauth2.service_account import Credentials

class MultiCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("URL結果 個別コピーアプリ")
        self.text_widgets = []

        # URL入力欄
        url_label = tk.Label(root, text="URLを改行で入力（最大7件）:")
        url_label.pack(pady=5, padx=10, anchor='w')
        self.url_text = scrolledtext.ScrolledText(root, height=6, width=80)
        self.url_text.pack(pady=5, padx=10, anchor='w')

        scrape_btn = tk.Button(root, text="スクレイピング実行", command=self.scrape_urls)
        scrape_btn.pack(pady=10, padx=10, anchor='w')

        save_btn = tk.Button(root, text="スプレッドシートに保存", command=self.save_to_spreadsheet)
        save_btn.pack(pady=10, padx=10, anchor='w')

        self.result_frames = []

        for i in range(7):
            frame = tk.Frame(root, borderwidth=1, relief="solid", padx=5, pady=5)
            frame.pack(padx=10, pady=5, fill="x", expand=True)

            label = tk.Label(frame, text=f"出力 {i+1}")
            label.pack(anchor='w', padx=5)

            text = tk.Text(frame, height=6, width=80, wrap="word")
            text.pack(side="left", padx=(0, 10))
            self.text_widgets.append(text)

            copy_btn = tk.Button(frame, text="コピー", command=lambda i=i: self.copy_text(i))
            copy_btn.pack(side="right", padx=5)

    def save_to_spreadsheet(self):
        # スプレッドシートに書き込む
        credentials_path = '/Users/masaki/Desktop/【json】/gspread-test-408312-2072e3277dcd.json'
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_file(credentials_path, scopes=scope)
        gc = gspread.authorize(creds)
        spreadsheet = gc.open_by_key('1mF2nBRBPxeYog7YnBFy-1QNxDmjwUl5O2ZhqB6y7_Qw')
        ws = spreadsheet.worksheet('出力')

        # 各出力結果をスプレッドシートに書き込む
        for i, text_widget in enumerate(self.text_widgets):
            output = text_widget.get("1.0", tk.END).strip()
            if output:
                ws.update_cell(2, i + 1, output)  # A2, B2, C2... に出力
            else:
                ws.update_cell(2, i + 1, "結果なし")

        # メッセージ表示
        messagebox.showinfo("保存完了", "結果をスプレッドシートに保存しました！")

        # 入力欄と出力欄をクリア
        self.url_text.delete("1.0", tk.END)
        for text_widget in self.text_widgets:
            text_widget.delete("1.0", tk.END)

    def scrape_urls(self):
        urls = self.url_text.get("1.0", tk.END).strip().splitlines()
        if not urls:
            messagebox.showerror("エラー", "URLを1つ以上入力してください")
            return
        if len(urls) > 7:
            messagebox.showwarning("警告", "URLは最大7件までです")
            return

        for i in range(7):
            self.text_widgets[i].delete("1.0", tk.END)

        for i, url in enumerate(urls):
            try:
                res = requests.get(url)
                encoding = chardet.detect(res.content)['encoding']
                soup = BeautifulSoup(res.content, 'html.parser', from_encoding=encoding)

                output = ""

                # タイトル取得
                titles = soup.find_all('h1')
                for title in titles:
                    output += f"{title.text.strip()}\n\n"

                # 参照URL取得
                reference_div = soup.find('div', class_='post__reference')
                if reference_div:
                    a_tag = reference_div.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        output += f"{a_tag['href']}\n\n"

                # 日付と本文
                dates = soup.find_all('div', class_='t_h')
                contents = soup.find_all('div', class_='t_b')

                for date, content in zip(dates, contents):
                    date_text = date.text.strip().replace('"', '')
                    content_text = ''
                    for elem in content.children:
                        if elem.name == 'br':
                            content_text += '.\n'
                        elif elem.string:
                            content_text += elem.string.strip()
                    content_text = content_text.replace('"', '')
                    output += f"{date_text}\n{content_text}\n\n"

                self.text_widgets[i].insert("1.0", output.strip())

            except Exception as e:
                self.text_widgets[i].insert("1.0", f"エラー: {e}")
    def copy_text(self, index):
        content = self.text_widgets[index].get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            self.root.update()
            messagebox.showinfo("コピー完了", f"出力 {index + 1} をコピーしました")
        else:
            messagebox.showwarning("警告", f"出力 {index + 1} にコピー可能な内容がありません")

# 実行
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiCopyApp(root)
    root.mainloop()
