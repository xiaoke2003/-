import tkinter as tk


root = tk.Tk()

entry1 = tk.Entry(root)
entry1.pack(fill = tk.X, padx = 10, pady = 5)

entry2 = tk.Entry(root)
entry2.pack(fill = tk.X, padx = 10, pady = 5)

entry3 = tk.Entry(root)
entry3.pack(fill = tk.X, padx = 10, pady = 5)

root.mainloop()