import tkinter as tk
from tkinter import ttk  # より見栄えの良い部品を使いたい場合

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.geometry("400x300")
        self._create_widgets()

    def _create_widgets(self):
        """ウィジェットの作成と配置"""
        self.label = ttk.Label(self, text="入力してください:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self, width=30)
        self.entry.pack(pady=5)

        self.button = ttk.Button(self, text="実行", command=self.on_submit)
        self.button.pack(pady=10)

        self.output = tk.Text(self, height=5, width=40)
        self.output.pack(pady=10)

    def on_submit(self):
        """ボタンクリック時の処理"""
        text = self.entry.get()
        self.output.insert(tk.END, f"入力: {text}\n")
        self.entry.delete(0, tk.END)  # 入力欄をクリア

if __name__ == "__main__":
    app = BaseApp()
    app.mainloop()
