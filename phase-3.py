import tkinter as tk
from tkinter import messagebox

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Simulator")
        self.root.geometry("700x450")

        tk.Label(root, text="Tower of Hanoi Simulator",
                 font=("Arial", 20, "bold")).pack(pady=10)

        tk.Label(root, text="Number of disks (1-8):").pack()
        self.entry = tk.Entry(root, width=10)
        self.entry.insert(0, "3")
        self.entry.pack()

        self.canvas = tk.Canvas(root, width=650, height=260,
                                bg="white")
        self.canvas.pack(pady=10)

        buttons = tk.Frame(root)
        buttons.pack()

        tk.Button(buttons, text="Start", command=self.start).pack(side="left", padx=5)
        tk.Button(buttons, text="Previous", command=self.previous).pack(side="left", padx=5)
        tk.Button(buttons, text="Next", command=self.next).pack(side="left", padx=5)
        tk.Button(buttons, text="Reset", command=self.start).pack(side="left", padx=5)

        self.status = tk.Label(root, text="Enter disks and press Start")
        self.status.pack(pady=5)

    def start(self):
        try:
            n = int(self.entry.get())
            if not 1 <= n <= 8:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a number from 1 to 8")
            return

        self.towers = [list(range(n, 0, -1)), [], []]
        self.moves = []
        self.solve(n, 0, 1, 2)
        self.step = 0
        self.draw()

    def solve(self, n, a, b, c):
        if n == 0:
            return
        self.solve(n - 1, a, c, b)
        self.moves.append((a, c))
        self.solve(n - 1, b, a, c)

    def next(self):
        if self.step < len(self.moves):
            a, b = self.moves[self.step]
            self.towers[b].append(self.towers[a].pop())
            self.step += 1
            self.draw()

    def previous(self):
        if self.step > 0:
            a, b = self.moves[self.step - 1]
            self.towers[a].append(self.towers[b].pop())
            self.step -= 1
            self.draw()

    def draw(self):
        self.canvas.delete("all")
        width = 650
        base_y = 225
        centers = [110, 325, 540]

        for i, tower in enumerate(self.towers):
            x = centers[i]
            self.canvas.create_line(x, 45, x, base_y, width=5)
            self.canvas.create_line(x-75, base_y, x+75, base_y, width=5)

            for j, disk in enumerate(tower):
                y = base_y - (j + 1) * 22
                w = disk * 18
                self.canvas.create_rectangle(
                    x-w, y, x+w, y+18,
                    fill="skyblue", outline="black"
                )

            self.canvas.create_text(x, 245, text=f"Tower {i+1}")

        self.status.config(
            text=f"Move: {self.step}/{len(self.moves)} | "
                 f"Minimum moves: {len(self.moves)}"
        )

root = tk.Tk()
app = TowerOfHanoi(root)
root.mainloop()
