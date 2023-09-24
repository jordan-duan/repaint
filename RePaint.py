import tkinter as tk
from tkinter import ttk, colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.dark_mode = False  # Initially, set to light mode
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas_bg_light = "white"
        self.canvas_bg_dark = "black"
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg=self.canvas_bg_light, bd=3, relief=tk.SUNKEN)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.setup_navbar()
        self.setup_tools()
        self.setup_events()
        self.prev_x = None
        self.prev_y = None

    def setup_navbar(self):
        self.navbar = tk.Menu(self.root)
        self.root.config(menu=self.navbar)

        # File menu
        self.file_menu = tk.Menu(self.navbar, tearoff=False)
        self.navbar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        self.edit_menu = tk.Menu(self.navbar, tearoff=False)
        self.navbar.add_cascade(label="Edit", menu=self.edit_menu)

    def setup_tools(self):
        self.selected_tool = "pen"
        self.colors = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple", "White"]
        self.selected_color = self.colors[0]
        self.brush_sizes = [4, 6, 8, 10, 15, 20, 30, 40, 50]
        self.selected_size = self.brush_sizes[0]
        self.pen_types = ["Round", "Line", "Square", "Arrow", "Diamond"]
        self.selected_pen_type = self.pen_types[0]

        self.tool_frame = ttk.LabelFrame(self.root, text="Tools")
        self.tool_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure("Custom.TButton", padding=10, font=("Helvetica", 12))

        self.pen_button = ttk.Button(self.tool_frame, text="Pen", command=self.select_pen_tool, style="Custom.TButton")
        self.pen_button.pack(side=tk.TOP, padx=5, pady=5)

        self.eraser_button = ttk.Button(self.tool_frame, text="Eraser", command=self.select_eraser_tool, style="Custom.TButton")
        self.eraser_button.pack(side=tk.TOP, padx=5, pady=5)

        self.brush_size_label = ttk.Label(self.tool_frame, text="Brush Size:")
        self.brush_size_label.pack(side=tk.TOP, padx=5, pady=5)

        self.brush_size_combobox = ttk.Combobox(self.tool_frame, values=self.brush_sizes, state="readonly")
        self.brush_size_combobox.current(0)
        self.brush_size_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.brush_size_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_size(int(self.brush_size_combobox.get())))

        self.color_label = ttk.Label(self.tool_frame, text="Color:")
        self.color_label.pack(side=tk.TOP, padx=5, pady=5)

        self.color_combobox = ttk.Combobox(self.tool_frame, values=self.colors, state="readonly")
        self.color_combobox.current(0)
        self.color_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.color_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_color(self.color_combobox.get()))

        self.pen_type_label = ttk.Label(self.tool_frame, text="Pen Type:")
        self.pen_type_label.pack(side=tk.TOP, padx=5, pady=5)

        self.pen_type_combobox = ttk.Combobox(self.tool_frame, values=self.pen_types, state="readonly")
        self.pen_type_combobox.current(0)
        self.pen_type_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.pen_type_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_pen_type(self.pen_type_combobox.get()))

        self.custom_color_button = ttk.Button(self.tool_frame, text="Custom Color", command=self.choose_custom_color, style="Custom.TButton")
        self.custom_color_button.pack(side=tk.TOP, padx=5, pady=5)

        self.clear_button = ttk.Button(self.tool_frame, text="Clear Canvas", command=self.clear_canvas, style="Custom.TButton")
        self.clear_button.pack(side=tk.TOP, padx=5, pady=5)

        self.dark_mode_button = ttk.Button(self.tool_frame, text="Toggle Dark Mode", command=self.toggle_dark_mode, style="Custom.TButton")
        self.dark_mode_button.pack(side=tk.TOP, padx=5, pady=5)

        # Footer label placed inside the footer frame
        self.footer_label = tk.Label(self.tool_frame, text="Made with ❤", bg="lightgray")
        self.footer_label.pack(fill=tk.X)

    def setup_events(self):
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def select_pen_tool(self):
        self.selected_tool = "pen"

    def select_eraser_tool(self):
        self.selected_tool = "eraser"

    def select_size(self, size):
        self.selected_size = size

    def select_color(self, color):
        self.selected_color = color

    def select_pen_type(self, pen_type):
        self.selected_pen_type = pen_type

    def draw(self, event):
        if self.selected_tool == "pen":
            if self.prev_x is not None and self.prev_y is not None:
                if self.selected_pen_type == "line":
                    self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill=self.selected_color,
                                            width=self.selected_size, smooth=True)
                elif self.selected_pen_type == "Round":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_oval(x1, y1, x2, y2, fill=self.selected_color, outline=self.selected_color)
                elif self.selected_pen_type == "Square":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.selected_color, outline=self.selected_color)
                elif self.selected_pen_type == "Arrow":
                    x1 = event.x - self.selected_size
                    y1 = event.y - self.selected_size
                    x2 = event.x + self.selected_size
                    y2 = event.y + self.selected_size
                    self.canvas.create_polygon(x1, y1, x1, y2, event.x, y2, fill=self.selected_color,
                                            outline=self.selected_color)
                elif self.selected_pen_type == "Diamond":
                    x1 = event.x - self.selected_size
                    y1 = event.y
                    x2 = event.x
                    y2 = event.y - self.selected_size
                    x3 = event.x + self.selected_size
                    y3 = event.y
                    x4 = event.x
                    y4 = event.y + self.selected_size
                    self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, x4, y4, fill=self.selected_color, outline=self.selected_color)
            self.prev_x = event.x
            self.prev_y = event.y

        elif self.selected_tool == "eraser":
            if self.prev_x is not None and self.prev_y is not None:
                x1 = event.x - self.selected_size
                y1 = event.y - self.selected_size
                x2 = event.x + self.selected_size
                y2 = event.y + self.selected_size
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="white")
            self.prev_x = event.x
            self.prev_y = event.y

    def release(self, event):
        self.prev_x = None
        self.prev_y = None

    def clear_canvas(self):
        self.canvas.delete("all")

    def take_snapshot(self):
        self.canvas.postscript(file="snapshot.eps")

    def undo(self):
        if self.undo_stack:
            item = self.undo_stack.pop()
            self.canvas.delete(item)

    def toggle_dark_mode(self):
        # Toggle dark mode
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.root.configure(bg="black")
            self.canvas.configure(bg=self.canvas_bg_dark)
            self.footer_label.configure(bg="black", fg="white")
        else:
            self.root.configure(bg="white")
            self.canvas.configure(bg=self.canvas_bg_light)
            self.footer_label.configure(bg="lightgray", fg="black")

    def choose_custom_color(self):
        custom_color = colorchooser.askcolor()[1]  # Opens a color dialog and returns the selected color in hex format
        if custom_color:
            self.selected_color = custom_color

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RePaint")
    app = PaintApp(root)
    root.mainloop()
