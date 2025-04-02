import tkinter as tk
from query_data import query_faq  

def start_gui():
    def handle_query():
        question = entry.get()
        response = query_faq(question)
        output.config(text=response)

    root = tk.Tk()
    root.title("FAQ-Assistent")

    tk.Label(root, text="Frage:").pack()
    entry = tk.Entry(root, width=50)
    entry.pack()

    tk.Button(root, text="Absenden", command=handle_query).pack()

    output = tk.Label(root, text="", wraplength=400)
    output.pack()

    root.mainloop()
