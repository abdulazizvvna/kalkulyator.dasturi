import tkinter as tk
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulyator")
        self.root.geometry("360x550")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.expression = ""
        self.history = []
        self.dark_mode = False
        
        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.display_var, font=("Helvetica", 24), justify='right',
                                bg="lightgray", fg="black", insertbackground="black")
        self.display.pack(fill='x', ipady=20, padx=20, pady=20)

        btn_frame = tk.Frame(root, bg="white")
        btn_frame.pack(padx=10, pady=10)

        self.buttons = [
            ["C", "(", ")", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "^", "="],
            ["sin", "cos", "tan", "√"],
            ["log", "exp", "pi", "mode"],
            ["history"]
        ]

        for r, row in enumerate(self.buttons):
            for c, char in enumerate(row):
                btn = tk.Button(btn_frame, text=char.capitalize(), font=("Helvetica", 14),
                                command=lambda ch=char: self.on_click(ch), width=6, height=2)
                btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(len(self.buttons)):
            btn_frame.rowconfigure(i, weight=1)

        self.root.bind("<Key>", self.key_press)

    def set_dark_theme(self):
        self.root.configure(bg="black")
        self.display.configure(bg="gray10", fg="white", insertbackground="white")
        
    def set_light_theme(self):
        self.root.configure(bg="white")
        self.display.configure(bg="lightgray", fg="black", insertbackground="black")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("")
        elif char == "=":
            try:
                result = self.evaluate_expression(self.expression)
                self.history.append(f"{self.expression} = {result}")
                self.display_var.set(result)
                self.expression = str(result)
            except Exception as e:
                self.display_var.set("Xatolik")
                self.expression = ""
        elif char == "√":
            self.expression += "math.sqrt("
        elif char == "sin":
            self.expression += "math.sin(math.radians("
        elif char == "cos":
            self.expression += "math.cos(math.radians("
        elif char == "tan":
            self.expression += "math.tan(math.radians("
        elif char == "log":
            self.expression += "math.log10("
        elif char == "exp":
            self.expression += "math.exp("
        elif char == "pi":
            self.expression += str(math.pi)
        elif char == "^":
            self.expression += "**"
        elif char == "mode":
            self.toggle_theme()
            return
        elif char == "history":
            self.show_history()
            return
        else:
            self.expression += str(char)

        self.display_var.set(self.expression)

    def key_press(self, event):
        key = event.keysym

        if key == "Return":
            self.on_click("=")
        elif key == "BackSpace":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
        elif key == "Escape":
            self.on_click("C")
        elif key in "0123456789":
            self.on_click(key)
        elif key in ("plus", "KP_Add"):
            self.on_click("+")
        elif key in ("minus", "KP_Subtract"):
            self.on_click("-")
        elif key in ("asterisk", "KP_Multiply"):
            self.on_click("*")
        elif key in ("slash", "KP_Divide"):
            self.on_click("/")
        elif key == "period":
            self.on_click(".")
        elif key == "parenleft":
            self.on_click("(")
        elif key == "parenright":
            self.on_click(")")
        elif key == "asciicircum":
            self.on_click("^")

    def evaluate_expression(self, expr):
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        return eval(expr, {"__builtins__": None}, allowed_names)

    def show_history(self):
        hist = tk.Toplevel(self.root)
        hist.title("Tarix")
        hist.geometry("300x300")
        hist.configure(bg="black" if self.dark_mode else "white")

        text = tk.Text(hist,
                       bg="gray15" if self.dark_mode else "white",
                       fg="white" if self.dark_mode else "black",
                       font=("Helvetica", 12))
        text.pack(expand=True, fill='both')

        for line in self.history:
            text.insert(tk.END, line + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()