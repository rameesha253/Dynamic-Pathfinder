import tkinter as tk
from tkinter import ttk
import heapq
import random
import time
import math

CELL_SIZE = 30

class PathfindingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Pathfinding Visualizer")
        self.root.configure(bg="#f0f4f8")
        
        # Make window maximized
        self.root.state('zoomed')  # Windows
        try:
            self.root.attributes('-zoomed', True)  # Linux
        except:
            pass

        self.rows = 20
        self.cols = 20
        self.grid = []
        self.start = (0, 0)
        self.goal = (19, 19)

        self.algorithm = tk.StringVar(value="A*")
        self.heuristic_type = tk.StringVar(value="Manhattan")
        self.dynamic_mode = tk.BooleanVar()

        self.running = False
        self.current_path = []

        self.create_header()
        self.create_controls()
        self.create_grid()
        self.create_legend()

    # ---------------- HEADER ----------------

    def create_header(self):
        header = tk.Frame(self.root, bg="#2c3e50", height=50)
        header.pack(fill="x")
        
        title = tk.Label(
            header, 
            text="🤖 Dynamic Pathfinding Agent",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack(pady=10)

    # ---------------- CONTROLS ----------------

    def create_controls(self):
        # Main control frame with reduced padding
        control_bg = tk.Frame(self.root, bg="#f0f4f8")
        control_bg.pack(fill="x", padx=15, pady=8)
        
        control = tk.Frame(control_bg, bg="white", relief="flat", bd=0)
        control.pack(fill="x", padx=5, pady=5)
        
        # Add inner padding
        inner_frame = tk.Frame(control, bg="white")
        inner_frame.pack(padx=10, pady=8)

        # Row 1: Grid Settings
        settings_row = tk.Frame(inner_frame, bg="white")
        settings_row.pack(fill="x", pady=3)
        
        tk.Label(
            settings_row, 
            text="Grid Size:", 
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side="left", padx=5)
        
        tk.Label(settings_row, text="Rows:", bg="white", fg="#555", font=("Arial", 9)).pack(side="left", padx=(10, 2))
        self.row_entry = tk.Entry(settings_row, width=5, font=("Arial", 9))
        self.row_entry.insert(0, "20")
        self.row_entry.pack(side="left", padx=2)
        
        tk.Label(settings_row, text="Cols:", bg="white", fg="#555", font=("Arial", 9)).pack(side="left", padx=(10, 2))
        self.col_entry = tk.Entry(settings_row, width=5, font=("Arial", 9))
        self.col_entry.insert(0, "20")
        self.col_entry.pack(side="left", padx=2)

        # Row 2: Algorithm Settings
        algo_row = tk.Frame(inner_frame, bg="white")
        algo_row.pack(fill="x", pady=5)
        
        tk.Label(
            algo_row, 
            text="Algorithm:", 
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side="left", padx=5)
        
        algo_combo = ttk.Combobox(
            algo_row, 
            textvariable=self.algorithm,
            values=["A*", "Greedy"], 
            width=10,
            font=("Arial", 9),
            state="readonly"
        )
        algo_combo.pack(side="left", padx=5)
        
        tk.Label(
            algo_row, 
            text="Heuristic:", 
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side="left", padx=(15, 5))
        
        heur_combo = ttk.Combobox(
            algo_row, 
            textvariable=self.heuristic_type,
            values=["Manhattan", "Euclidean"], 
            width=10,
            font=("Arial", 9),
            state="readonly"
        )
        heur_combo.pack(side="left", padx=5)
        
        dynamic_check = tk.Checkbutton(
            algo_row, 
            text="🔄 Dynamic Obstacles",
            variable=self.dynamic_mode,
            bg="white", 
            fg="#2c3e50",
            font=("Arial", 9),
            selectcolor="white",
            activebackground="white"
        )
        dynamic_check.pack(side="left", padx=15)

        # Row 3: Action Buttons
        button_row = tk.Frame(inner_frame, bg="white")
        button_row.pack(fill="x", pady=5)
        
        # Style buttons with compact size
        btn_config = {
            "font": ("Arial", 9, "bold"),
            "width": 18,
            "height": 1,
            "relief": "flat",
            "cursor": "hand2"
        }
        
        tk.Button(
            button_row, 
            text="🔧 Generate Grid", 
            bg="#3498db",
            fg="white",
            command=self.generate_grid,
            **btn_config
        ).pack(side="left", padx=3)

        tk.Button(
            button_row, 
            text="🎲 Random Obstacles", 
            bg="#e67e22",
            fg="white",
            command=self.random_obstacles,
            **btn_config
        ).pack(side="left", padx=3)

        tk.Button(
            button_row, 
            text="▶️ Start Search", 
            bg="#27ae60",
            fg="white",
            command=self.start_search,
            **btn_config
        ).pack(side="left", padx=3)
        
        tk.Button(
            button_row, 
            text="🗑️ Clear Grid", 
            bg="#e74c3c",
            fg="white",
            command=self.clear_grid,
            **btn_config
        ).pack(side="left", padx=3)

        # Metrics display
        self.metrics = tk.Label(
            self.root, 
            text="Click 'Start Search' to begin",
            fg="#2c3e50",
            bg="#ecf0f1",
            font=("Arial", 10, "bold"),
            height=1,
            relief="flat"
        )
        self.metrics.pack(fill="x", padx=15, pady=3)

    # ---------------- GRID ----------------

    def create_grid(self):
        # Create scrollable canvas frame if it doesn't exist
        if not hasattr(self, 'canvas_container'):
            self.canvas_container = tk.Frame(self.root, bg="#f0f4f8")
            self.canvas_container.pack(fill="both", expand=True, padx=15, pady=5)
            
            # Create canvas for scrolling
            self.scroll_canvas = tk.Canvas(self.canvas_container, bg="#f0f4f8", highlightthickness=0)
            self.scroll_canvas.pack(side="left", fill="both", expand=True)
            
            # Add scrollbars
            v_scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.scroll_canvas.yview)
            v_scrollbar.pack(side="right", fill="y")
            
            h_scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.scroll_canvas.xview)
            h_scrollbar.pack(fill="x", padx=15, before=self.canvas_container)
            
            self.scroll_canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
            
            # Frame inside canvas to hold the grid
            self.canvas_frame = tk.Frame(self.scroll_canvas, bg="#f0f4f8")
            self.scroll_canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        
        # Destroy old canvas if it exists
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.cols * CELL_SIZE,
            height=self.rows * CELL_SIZE,
            bg="white",
            highlightthickness=2,
            highlightbackground="#bdc3c7"
        )
        self.canvas.pack()

        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.toggle_wall)
        
        # Update scroll region
        self.canvas_frame.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        
        # Enable mouse wheel scrolling
        self.scroll_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.scroll_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.scroll_canvas.bind_all("<Button-5>", self._on_mousewheel)

    def generate_grid(self):
        self.rows = int(self.row_entry.get())
        self.cols = int(self.col_entry.get())
        self.goal = (self.rows-1, self.cols-1)
        self.create_grid()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.scroll_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.scroll_canvas.yview_scroll(-1, "units")

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"
                
                if (r,c) == self.start:
                    color = "#00ff88"  # Green start
                elif (r,c) == self.goal:
                    color = "#ff4444"  # Red goal
                elif self.grid[r][c] == 1:
                    color = "#2c3e50"  # Dark walls

                self.canvas.create_rectangle(
                    c*CELL_SIZE, r*CELL_SIZE,
                    (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
                    fill=color, 
                    outline="#dfe6e9",
                    width=1
                )

    def toggle_wall(self, event):
        r = event.y // CELL_SIZE
        c = event.x // CELL_SIZE
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if (r,c) != self.start and (r,c) != self.goal:
                self.grid[r][c] = 1 - self.grid[r][c]
                self.draw_grid()

    def random_obstacles(self):
        density = 0.3
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) not in [self.start, self.goal]:
                    if random.random() < density:
                        self.grid[r][c] = 1
        self.draw_grid()

    def clear_grid(self):
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.draw_grid()
        self.metrics.config(text="Grid cleared! Ready for new search.")

    # ---------------- LEGEND ----------------

    def create_legend(self):
        legend_frame = tk.Frame(self.root, bg="white", relief="flat")
        legend_frame.pack(fill="x", padx=15, pady=5)
        
        tk.Label(
            legend_frame, 
            text="Legend:", 
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(side="left", padx=10)
        
        legend_items = [
            ("#00ff88", "Start"),
            ("#ff4444", "Goal"),
            ("#2c3e50", "Wall"),
            ("#fff176", "Frontier"),
            ("#87cefa", "Visited"),
            ("#4caf50", "Path")
        ]
        
        for color, label in legend_items:
            item_frame = tk.Frame(legend_frame, bg="white")
            item_frame.pack(side="left", padx=3)
            
            color_box = tk.Canvas(item_frame, width=18, height=18, bg=color, highlightthickness=1, highlightbackground="#bdc3c7")
            color_box.pack(side="left", padx=2)
            
            tk.Label(item_frame, text=label, bg="white", fg="#555", font=("Arial", 8)).pack(side="left", padx=2)

    # ---------------- HEURISTIC ----------------

    def heuristic(self, node):
        r, c = node
        gr, gc = self.goal
        if self.heuristic_type.get() == "Manhattan":
            return abs(r-gr) + abs(c-gc)
        return math.sqrt((r-gr)**2 + (c-gc)**2)

    # ---------------- SEARCH ----------------

    def start_search(self):
        self.running = True
        self.draw_grid()  # Reset visual
        start_time = time.time()

        frontier = []
        heapq.heappush(frontier, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        visited = set()
        visited_count = 0

        while frontier and self.running:
            _, current = heapq.heappop(frontier)

            if current == self.goal:
                break

            if current in visited:
                continue

            visited.add(current)
            visited_count += 1

            self.color_cell(current, "#87cefa")  # Visited blue
            self.root.update()
            time.sleep(0.01)  # Smooth animation

            for neighbor in self.get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g

                    if self.algorithm.get() == "A*":
                        f = tentative_g + self.heuristic(neighbor)
                    else:
                        f = self.heuristic(neighbor)

                    heapq.heappush(frontier, (f, neighbor))
                    self.color_cell(neighbor, "#fff176")  # Frontier yellow

            if self.dynamic_mode.get():
                self.spawn_dynamic_obstacle()

        path = self.reconstruct_path(came_from)
        exec_time = (time.time() - start_time) * 1000

        self.draw_path(path)

        self.metrics.config(
            text=f"✅ Search Complete! | Nodes Visited: {visited_count} | Path Length: {len(path)} | Time: {exec_time:.2f} ms"
        )

    def get_neighbors(self, node):
        r, c = node
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = []
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.grid[nr][nc] == 0:
                    neighbors.append((nr, nc))
        return neighbors

    def reconstruct_path(self, came_from):
        node = self.goal
        path = []
        while node in came_from:
            path.append(node)
            node = came_from[node]
        path.append(self.start)
        path.reverse()
        return path

    # ---------------- VISUAL ----------------

    def color_cell(self, node, color):
        r, c = node
        self.canvas.create_rectangle(
            c*CELL_SIZE, r*CELL_SIZE,
            (c+1)*CELL_SIZE, (r+1)*CELL_SIZE,
            fill=color, 
            outline="#dfe6e9",
            width=1
        )

    def draw_path(self, path):
        for r, c in path:
            if (r,c) not in [self.start, self.goal]:
                self.color_cell((r,c), "#4caf50")

    # ---------------- DYNAMIC OBSTACLE ----------------

    def spawn_dynamic_obstacle(self):
        if random.random() < 0.02:
            r = random.randint(0, self.rows-1)
            c = random.randint(0, self.cols-1)
            if (r,c) not in [self.start, self.goal]:
                self.grid[r][c] = 1
                self.draw_grid()

# ---------------- RUN ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()