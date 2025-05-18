import tkinter as tk

def click(event):
    current = entry.get()
    text = event.widget["text"]
    if text == "=":
        try:
            result = eval(current)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "エラー")
    elif text == "c":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)
        
root = tk.Tk()        
root.title('電卓アプリ')

entry = tk.Entry(root, font="Arial 20")
entry.pack(fill="both", ipadx=8, ipady=8)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", "C", "=", "+"]
]

for row in buttons:
    frame = tk.Frame(root)
    frame.pack()
    for btn in row:
        button = tk.Button(frame, text=btn, font="Arial 20", width=4, height=2)
        button.pack(side="left", padx=5, pady=5)
        button.bind("<Button-1>", click)
        
root.mainloop()        