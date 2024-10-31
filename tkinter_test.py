import tkinter as tk


class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Your Seed!")

        self.rows = 20
        self.cols = 20
        self.square_size = 10  # Size of each square (pixels)
        self.grid = []

        # Create a canvas
        self.canvas = tk.Canvas(
            root,
            width=self.cols * self.square_size,
            height=self.rows * self.square_size,
        )
        self.canvas.pack()

        # Create the grid of squares (alternating black and white)
        for row in range(self.rows):
            row_squares = []
            for col in range(self.cols):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                square = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="black", outline="black"
                )
                self.canvas.tag_bind(square, "<Button-1>", self.change_color)
                row_squares.append(square)
            self.grid.append(row_squares)

    def change_color(self, event):
        # Get the item clicked
        square = self.canvas.find_closest(event.x, event.y)[0]

        # Get the current color
        current_color = self.canvas.itemcget(square, "fill")

        # Toggle the color
        new_color = "white" if current_color == "black" else "black"
        self.canvas.itemconfig(square, fill=new_color)


# Create the main window
root = tk.Tk()

# Instantiate the grid application
app = GridApp(root)

# Start the Tkinter event loop
root.mainloop()
