import tkinter as tk
from tkinter import messagebox

# 置換ルール（追加可能）
replace_dict = {
    '"<': '<',
    '>"': '>',
    '.<': '<',
    ".'": "'",
}

def replace_text():
    input_text = input_field.get("1.0", tk.END)
    output_text = input_text
    for old, new in replace_dict.items():
        output_text = output_text.replace(old, new)
    output_field.delete("1.0", tk.END)
    output_field.insert(tk.END, output_text)

def copy_to_clipboard():
    text = output_field.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("コピー完了", "変換後のテキストをクリップボードにコピーしました。")

    # 変換前テキストフィールドをクリア
    input_field.delete("1.0", tk.END)

# GUI作成
root = tk.Tk()
root.title("テキストリプレイスツール")

# ラベルと入力欄
tk.Label(root, text="変換前のテキスト:").pack()
input_field = tk.Text(root, height=10, width=80)
input_field.pack()

# リプレイスボタン
replace_button = tk.Button(root, text="リプレイス実行", command=replace_text)
replace_button.pack(pady=5)

# 出力欄
tk.Label(root, text="変換後のテキスト:").pack()
output_field = tk.Text(root, height=10, width=80)
output_field.pack()

# コピーボタン
copy_button = tk.Button(root, text="コピー", command=copy_to_clipboard)
copy_button.pack(pady=5)

# メインループ
root.mainloop()
