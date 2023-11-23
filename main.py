import tkinter as tk
from controller.main_controller import MainController

def main():
    root = tk.Tk()
    root.title("Compilador costeñol")
    root.resizable(width=False, height=False)
    app = MainController(master=root)
    app.view.pack(expand=True, fill='both')
    root.mainloop()

if __name__ == '__main__':
    main()