import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

class SimpleImageConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG画像変換")
        self.root.geometry("300x150")
        self.root.configure(bg="#f8f9fa")

        self.select_btn = tk.Button(
            root,
            text="フォルダを選択",
            command=self.select_folder,
            bg="#4a90e2",
            fg="black",
            font=("Helvetica", 12),
            relief="flat",
            padx=20,
            pady=10
        )
        self.select_btn.pack(expand=True)

    def select_folder(self):
        # macOSのデスクトップパスを取得
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        folder_path = filedialog.askdirectory(
            title="変換対象フォルダを選択",
            initialdir=desktop_path
        )

        if folder_path:
            self.convert_images(folder_path)
            messagebox.showinfo("完了", "JPGへの変換が完了しました！")

    def convert_images(self, folder_path):
        target_extensions = ['.png', '.webp']
        files = sorted(os.listdir(folder_path))

        for file_name in files:
            ext = os.path.splitext(file_name.lower())[1]
            if ext in target_extensions:
                file_path = os.path.join(folder_path, file_name)
                new_file_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + '.jpg')
                try:
                    image = cv2.imread(file_path)
                    if image is not None:
                        cv2.imwrite(new_file_path, image)
                        os.remove(file_path)
                except Exception as e:
                    print(f"エラー: {file_name} - {e}")

# 実行
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleImageConverter(root)
    root.mainloop()
