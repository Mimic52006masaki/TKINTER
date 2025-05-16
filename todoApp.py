import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ===== Googleスプレッドシート接続クラス =====
class GoogleSheetDB:
    def __init__(self, cred_path, spreadsheet_key, sheet_name):
        self.cred_path = cred_path
        self.spreadsheet_key = spreadsheet_key
        self.sheet_name = sheet_name
        self.sheet = self._connect()

    def _connect(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_path, scope)
        client = gspread.authorize(creds)
        return client.open_by_key(self.spreadsheet_key).worksheet(self.sheet_name)

    def save_note(self, title, content):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sheet.append_row([title, content, now])

    def load_notes(self):
        values = self.sheet.get_all_values()
        return values[1:]  # ヘッダーを除く


# ===== Tkinter GUIアプリ本体クラス =====
class NoteApp(tk.Tk):
    def __init__(self, db):
        super().__init__()
        self.title("ノートアプリ（Google Sheets連携）")
        self.geometry("600x400")
        self.db = db
        self.notes = []

        self.create_widgets()

    def create_widgets(self):
        # タイトル入力
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.pack(pady=5)

        # 内容入力
        self.content_text = tk.Text(self, height=5, width=60)
        self.content_text.pack(pady=5)

        # ボタンエリア
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="保存", command=self.on_save).pack(side="left", padx=5)
        tk.Button(btn_frame, text="読み込み", command=self.on_load).pack(side="left", padx=5)

        # ノート一覧表示
        self.note_listbox = tk.Listbox(self, width=60)
        self.note_listbox.pack(pady=10)
        self.note_listbox.bind("<<ListboxSelect>>", self.on_select)

    def on_save(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", "end-1c").strip()

        if not title or not content:
            messagebox.showwarning("入力エラー", "タイトルと内容は必須です。")
            return

        self.db.save_note(title, content)
        messagebox.showinfo("保存成功", "ノートを保存しました。")
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def on_load(self):
        self.notes = self.db.load_notes()
        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            self.note_listbox.insert(tk.END, f"{note[0]} ({note[2]})")

    def on_select(self, event):
        if not self.note_listbox.curselection():
            return

        index = self.note_listbox.curselection()[0]
        note = self.notes[index]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note[0])
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert(tk.END, note[1])


# ===== 実行セクション =====
if __name__ == "__main__":
    # スプレッドシートの情報を設定
    CREDENTIAL_FILE_PATH = '/Users/masaki/Desktop/【json】/gspread-test-408312-2072e3277dcd.json'
    SPREADSHEET_KEY = '1mF2nBRBPxeYog7YnBFy-1QNxDmjwUl5O2ZhqB6y7_Qw'
    SHEET_NAME = 'test'  # シートにヘッダー: A1=Title, B1=Content, C1=Updated を入れておく

    # DB接続とアプリ起動
    db = GoogleSheetDB(CREDENTIAL_FILE_PATH, SPREADSHEET_KEY, SHEET_NAME)
    app = NoteApp(db)
    app.mainloop()
