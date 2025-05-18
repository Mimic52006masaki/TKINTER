import os
import cv2
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ImageConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📁 画像一括JPG変換ツール")
        self.geometry("600x400")
        self.configure(bg="#e6f7ff")  # 鮮やかな背景
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)

        self.selected_path = tk.StringVar()
        self._create_widgets()

    def _create_widgets(self):
        # スタイル定義
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("TButton",
                        font=("Helvetica", 14, "bold"),
                        padding=10,
                        background="#007acc",
                        foreground="white")
        style.map("TButton",
                  background=[("active", "#005f99")])

        # タイトルラベル
        title = tk.Label(
            self,
            text="画像を一括JPG変換",
            font=("Helvetica", 26, "bold"),
            bg="#e6f7ff",
            fg="#007acc"
        )
        title.pack(pady=(40, 20))

        # 選択フォルダパス表示
        self.path_label = tk.Label(
            self,
            textvariable=self.selected_path,
            font=("Helvetica", 11),
            bg="#e6f7ff",
            fg="#006080"
        )
        self.path_label.pack(pady=(0, 10))

        # ボタン（ttk）
        convert_button = ttk.Button(
            self,
            text="フォルダ選択＆変換開始",
            command=self.select_folder_and_convert
        )
        convert_button.pack(pady=30)

        # フッター
        footer = tk.Label(
            self,
            text="対応形式: PNG / WEBP / GIF / AVIF → JPG",
            font=("Helvetica", 10),
            bg="#e6f7ff",
            fg="#888"
        )
        footer.pack(side="bottom", pady=15)

    def select_folder_and_convert(self):
        folder_selected = filedialog.askdirectory(
            initialdir=os.path.expanduser("~/Desktop"))
        if folder_selected:
            self.selected_path.set(
                f"選択されたフォルダ: {os.path.basename(folder_selected)}")
            self.convert_images_in_folder(folder_selected)

    def convert_images_in_folder(self, folder_path):
        target_extensions = ['.png', '.webp', '.gif', '.avif']
        files = sorted(os.listdir(folder_path))

        for file_name in files:
            ext = os.path.splitext(file_name.lower())[1]
            if ext in target_extensions:
                file_path = os.path.join(folder_path, file_name)
                new_file_path = os.path.join(
                    folder_path, os.path.splitext(file_name)[0] + '.jpg')

                try:
                    if ext in ['.png', '.webp']:
                        image = cv2.imread(file_path)
                        if image is not None:
                            cv2.imwrite(new_file_path, image)
                        else:
                            print(f"OpenCVで読み込めませんでした: {file_name}")
                    elif ext == '.gif':
                        with Image.open(file_path) as im:
                            rgb_im = im.convert('RGB')
                            rgb_im.save(new_file_path, 'JPEG')
                    elif ext == '.avif':
                        with Image.open(file_path) as im:
                            rgb_im = im.convert('RGB')
                            rgb_im.save(new_file_path, 'JPEG')

                    os.remove(file_path)
                    print(f"{file_name} → JPG変換＆削除完了")

                except Exception as e:
                    print(f"変換中にエラーが発生しました: {file_name}, エラー: {e}")

        messagebox.showinfo("完了", "すべてのJPG変換が完了しました！")


if __name__ == "__main__":
    app = ImageConverterApp()
    app.mainloop()
