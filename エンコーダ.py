import os
import cv2
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_images():
    folder_path = filedialog.askdirectory(initialdir=os.path.expanduser("~/Desktop"))
    if not folder_path:
        return

    target_extensions = ['.png', '.webp', '.gif', '.avif']
    files = sorted(os.listdir(folder_path))
    converted_count = 0

    for file_name in files:
        file_lower = file_name.lower()
        ext = os.path.splitext(file_lower)[1]

        if ext in target_extensions:
            file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, os.path.splitext(file_name)[0] + '.jpg')

            try:
                if ext in ['.png', '.webp']:
                    try:
                        # Pillow優先。OpenCVで読み込めない画像もあるため。
                        with Image.open(file_path) as im:
                            rgb_im = im.convert('RGB')
                            rgb_im.save(new_file_path, 'JPEG')
                    except:
                        image = cv2.imread(file_path)
                        if image is not None:
                            cv2.imwrite(new_file_path, image)
                        else:
                            print(f"OpenCVでも読み込めませんでした: {file_name}")
                            continue

                elif ext in ['.gif', '.avif']:
                    with Image.open(file_path) as im:
                        rgb_im = im.convert('RGB')
                        rgb_im.save(new_file_path, 'JPEG')

                os.remove(file_path)
                converted_count += 1

            except Exception as e:
                print(f"変換エラー: {file_name} → {e}")

    messagebox.showinfo("完了", f"{converted_count} 枚の画像をJPGに変換し、元ファイルを削除しました。")

# UI部分（同じ）
root = tk.Tk()
root.title("画像一括JPG変換")
root.geometry("400x180")
root.configure(bg="#f9f9f9")

btn = tk.Button(
    root,
    text="フォルダを選んで変換開始",
    command=convert_images,
    font=("Helvetica", 14),
    bg="#4CAF50",
    fg="black",
    padx=20,
    pady=10,
    relief="flat",
    bd=0
)
btn.pack(expand=True)

root.mainloop()
