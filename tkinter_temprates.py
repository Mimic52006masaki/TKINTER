import tkinter as tk

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("基本テンプレートアプリ")
        self.geometry("400x300")
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
        """ウィジェットの作成"""
        self.label = tk.Label(self, text="入力してください:")
        self.entry = tk.Entry(self, width=30)
        self.button = tk.Button(self, text="実行", command=self._on_submit)
        self.output = tk.Label(self, text="ここに出力されます")

    def _layout_widgets(self):
        """ウィジェットの配置"""
        self.label.pack(pady=10)
        self.entry.pack(pady=5)
        self.button.pack(pady=10)
        self.output.pack(pady=10)

    def _on_submit(self):
        """ボタンが押されたときの処理"""
        value = self.entry.get().strip()
        if value:
            self.output.config(text=f"入力内容: {value}")
        else:
            self.output.config(text="入力が空です")

if __name__ == "__main__":
    app = BaseApp()
    app.mainloop()
