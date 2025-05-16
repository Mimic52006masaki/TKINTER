import tkinter as tk

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Frameテンプレートアプリ")
        self.geometry("400x300")
        self._create_frames()
        self._create_widgets()
        self._layout_widgets()

    def _create_frames(self):
        """Frameの作成"""
        self.top_frame = tk.Frame(self)
        self.middle_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)

    def _create_widgets(self):
        """ウィジェットの作成"""
        # Top Frame: 入力関連
        self.label = tk.Label(self.top_frame, text="入力:")
        self.entry = tk.Entry(self.top_frame, width=30)

        # Middle Frame: ボタン
        self.button = tk.Button(self.middle_frame, text="実行", command=self._on_submit)

        # Bottom Frame: 出力
        self.output = tk.Label(self.bottom_frame, text="ここに出力されます")

    def _layout_widgets(self):
        """Frameとウィジェットの配置"""
        self.top_frame.pack(pady=10)
        self.middle_frame.pack(pady=10)
        self.bottom_frame.pack(pady=10)

        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT)

        self.button.pack()

        self.output.pack()

    def _on_submit(self):
        """ボタンクリック時の処理"""
        value = self.entry.get().strip()
        if value:
            self.output.config(text=f"入力された値: {value}")
        else:
            self.output.config(text="入力が空です")

if __name__ == "__main__":
    app = BaseApp()
    app.mainloop()
