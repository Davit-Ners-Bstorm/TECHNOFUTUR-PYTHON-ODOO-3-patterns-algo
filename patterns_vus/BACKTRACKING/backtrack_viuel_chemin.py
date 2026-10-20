import tkinter as tk

# Grille 8x8. 0 = case libre, 1 = mur.
# Départ en haut-gauche, arrivée en bas-droite.
# Cette grille a été vérifiée : elle contient un chemin solution ET
# plusieurs vraies impasses, pour que le backtracking ait l'occasion
# de reculer plusieurs fois avant de trouver la sortie.
GRID = [
    [0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 1, 0],
]

START = (0, 0)
END = (7, 7)
ROWS = len(GRID)
COLS = len(GRID[0])

# Ordre d'exploration des directions : Haut, Bas, Gauche, Droite.
# Doit correspondre exactement à l'ordre affiché dans le panneau de code.
DIRECTIONS = [(-1, 0, "Haut"), (1, 0, "Bas"), (0, -1, "Gauche"), (0, 1, "Droite")]

# Couleurs
COLOR_WALL = "#37474f"
COLOR_FREE = "#fafafa"
COLOR_CURRENT = "#ffb74d"     # orange : case active en ce moment
COLOR_PATH = "#64b5f6"        # bleu : fait partie du chemin en cours de construction
COLOR_DEADEND = "#e57373"     # rouge : case explorée puis abandonnée (backtrack)
COLOR_SOLUTION = "#81c784"    # vert : fait partie du chemin solution final
COLOR_START_END = "#ffd54f"   # jaune : départ / arrivée

# Squelette de code affiché aux élèves. Indices = numéros de ligne (0-based).
CODE_LINES = [
    "def solve(r, c, visited, path):",                         # 0
    "    visited.add((r, c))",                                  # 1
    "    path.append((r, c))",                                  # 2
    "",                                                          # 3
    "    if (r, c) == END:",                                     # 4
    "        return True   # chemin trouvé !",                  # 5
    "",                                                          # 6
    "    for (dr, dc) in [Haut, Bas, Gauche, Droite]:",          # 7
    "        nr, nc = r + dr, c + dc",                           # 8
    "        if is_valid(nr, nc, visited):",                     # 9
    "            if solve(nr, nc, visited, path):",              # 10
    "                return True",                               # 11
    "",                                                          # 12
    "    path.pop()        # impasse : on retire (r, c)",        # 13
    "    return False",                                          # 14
]

LINE_VISIT_ADD = 1
LINE_PATH_APPEND = 2
LINE_CHECK_END = 4
LINE_FOUND = 5
LINE_LOOP_DIR = 7
LINE_COMPUTE_NEIGHBOR = 8
LINE_IS_VALID = 9
LINE_RECURSE = 10
LINE_RETURN_TRUE = 11
LINE_POP = 13
LINE_RETURN_FALSE = 14


class Step:
    def __init__(self, kind, r, c, message, color, code_line, path_snapshot, found=False):
        self.kind = kind
        self.r = r
        self.c = c
        self.message = message
        self.color = color
        self.code_line = code_line
        self.path_snapshot = path_snapshot
        self.found = found


class MazeBacktrackVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Backtracking — recherche de chemin dans un labyrinthe")

        self.cell_size = 62

        margin = 28  # marge pour afficher les numéros de ligne/colonne autour de la grille

        # --- Grille (haut gauche) ---
        grid_frame = tk.Frame(root)
        grid_frame.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.canvas = tk.Canvas(
            grid_frame,
            width=COLS * self.cell_size + margin,
            height=ROWS * self.cell_size + margin,
            bg="white", highlightthickness=0
        )
        self.canvas.pack()
        self.grid_margin = margin

        # --- Panneau code (haut droite) ---
        code_frame = tk.Frame(root, bg="#1e1e1e")
        code_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        tk.Label(code_frame, text="Code en train de s'exécuter", font=("Arial", 12, "bold"),
                 bg="#1e1e1e", fg="white").pack(anchor="w", padx=10, pady=(8, 4))

        self.code_text = tk.Text(code_frame, width=44, height=17, font=("Consolas", 12),
                                  bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                                  state="disabled", borderwidth=0, highlightthickness=0, wrap="none")
        self.code_text.pack(padx=10, pady=(0, 10))
        self.code_text.tag_configure("highlight", background="#264f78", foreground="white")
        self._render_code()

        # --- Pile + journal (bas, pleine largeur) ---
        bottom = tk.Frame(root)
        bottom.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 5), sticky="nsew")

        left_bottom = tk.Frame(bottom)
        left_bottom.pack(side="left", anchor="n", padx=(0, 20))
        tk.Label(left_bottom, text="Pile actuelle (path)", font=("Arial", 11, "bold")).pack(anchor="w")
        self.stack_label = tk.Label(left_bottom, text="vide", font=("Consolas", 10), fg="#1565c0",
                                     wraplength=300, justify="left")
        self.stack_label.pack(anchor="w", pady=(0, 8))

        tk.Label(left_bottom, text="Position actuelle", font=("Arial", 11, "bold")).pack(anchor="w")
        self.pos_label = tk.Label(left_bottom, text="—", font=("Consolas", 16, "bold"), fg="#e65100")
        self.pos_label.pack(anchor="w")

        right_bottom = tk.Frame(bottom)
        right_bottom.pack(side="left", fill="both", expand=True)
        tk.Label(right_bottom, text="Journal des étapes", font=("Arial", 11, "bold")).pack(anchor="w")
        self.log_text = tk.Text(right_bottom, width=60, height=7, font=("Consolas", 10), state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True)

        # --- Légende ---
        legend = tk.Frame(root)
        legend.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        self._legend_item(legend, COLOR_START_END, "départ / arrivée")
        self._legend_item(legend, COLOR_CURRENT, "case active")
        self._legend_item(legend, COLOR_PATH, "chemin en construction")
        self._legend_item(legend, COLOR_DEADEND, "impasse (backtrack)")
        self._legend_item(legend, COLOR_SOLUTION, "chemin solution final")

        # --- Progression ---
        progress_frame = tk.Frame(root)
        progress_frame.grid(row=3, column=0, columnspan=2, pady=(6, 0))
        self.progress_label = tk.Label(progress_frame, text="Étape 0 / 0", font=("Arial", 9), fg="#555")
        self.progress_label.pack(side="left", padx=15)
        self.backtrack_label = tk.Label(progress_frame, text="Retours en arrière : 0", font=("Arial", 9, "bold"), fg="#c62828")
        self.backtrack_label.pack(side="left", padx=15)

        # --- Contrôles ---
        controls = tk.Frame(root)
        controls.grid(row=4, column=0, columnspan=2, pady=10)

        self.start_btn = tk.Button(controls, text="Démarrer", command=self.start, width=12)
        self.start_btn.pack(side="left", padx=5)

        self.next_btn = tk.Button(controls, text="Étape suivante ▶", command=self.next_step, width=16, state="disabled")
        self.next_btn.pack(side="left", padx=5)

        self.auto_btn = tk.Button(controls, text="Lecture auto", command=self.toggle_auto, width=12, state="disabled")
        self.auto_btn.pack(side="left", padx=5)

        self.reset_btn = tk.Button(controls, text="Réinitialiser", command=self.reset, width=12)
        self.reset_btn.pack(side="left", padx=5)

        self.status_label = tk.Label(root, text="Clique sur Démarrer pour commencer.", font=("Arial", 10, "italic"), fg="#555")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # --- État interne ---
        self.steps = []
        self.step_index = 0
        self.auto_playing = False
        self.backtrack_count = 0
        self.cell_state = {}  # (r,c) -> couleur actuelle affichée

        self.draw_grid_base()

    # ---------- UI helpers ----------

    def _legend_item(self, parent, color, text):
        f = tk.Frame(parent)
        f.pack(side="left", padx=8)
        c = tk.Canvas(f, width=18, height=18, highlightthickness=0)
        c.create_rectangle(2, 2, 16, 16, fill=color, outline="black")
        c.pack(side="left")
        tk.Label(f, text=text, font=("Arial", 9)).pack(side="left", padx=3)

    def _render_code(self):
        self.code_text.configure(state="normal")
        self.code_text.delete("1.0", "end")
        for line in CODE_LINES:
            self.code_text.insert("end", line + "\n")
        self.code_text.configure(state="disabled")

    def _highlight_line(self, line_index):
        self.code_text.configure(state="normal")
        self.code_text.tag_remove("highlight", "1.0", "end")
        self.code_text.tag_add("highlight", f"{line_index + 1}.0", f"{line_index + 1}.end")
        self.code_text.see(f"{line_index + 1}.0")
        self.code_text.configure(state="disabled")

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{self.step_index}. {message}\n\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    @staticmethod
    def _format_path(path_snapshot):
        if not path_snapshot:
            return "vide"
        return " → ".join(f"({r},{c})" for r, c in path_snapshot)

    # ---------- Dessin de la grille ----------

    def cell_coords(self, r, c):
        m = self.grid_margin
        x0 = m + c * self.cell_size
        y0 = m + r * self.cell_size
        return x0, y0, x0 + self.cell_size, y0 + self.cell_size

    def draw_grid_base(self):
        self.canvas.delete("all")
        m = self.grid_margin

        # Numéros de colonnes (au-dessus) et de lignes (à gauche)
        for c in range(COLS):
            x0, y0, x1, y1 = self.cell_coords(0, c)
            self.canvas.create_text((x0 + x1) / 2, m / 2, text=str(c), font=("Arial", 10), fill="#757575")
        for r in range(ROWS):
            x0, y0, x1, y1 = self.cell_coords(r, 0)
            self.canvas.create_text(m / 2, (y0 + y1) / 2, text=str(r), font=("Arial", 10), fill="#757575")

        for r in range(ROWS):
            for c in range(COLS):
                x0, y0, x1, y1 = self.cell_coords(r, c)
                if GRID[r][c] == 1:
                    color = COLOR_WALL
                elif (r, c) in (START, END):
                    color = COLOR_START_END
                else:
                    color = COLOR_FREE
                tag = f"cell_{r}_{c}"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#b0bec5", width=1, tags=tag)
                self.cell_state[(r, c)] = color
        # Labels Départ / Arrivée
        x0, y0, x1, y1 = self.cell_coords(*START)
        self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="DÉPART", font=("Arial", 9, "bold"), fill="#5d4037")
        x0, y0, x1, y1 = self.cell_coords(*END)
        self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text="ARRIVÉE", font=("Arial", 9, "bold"), fill="#5d4037")

        # Cadre extérieur net autour de toute la grille
        gx0, gy0, _, _ = self.cell_coords(0, 0)
        gx1, gy1, _, _ = self.cell_coords(ROWS - 1, COLS - 1)
        self.canvas.create_rectangle(gx0, gy0, gx1 + self.cell_size, gy1 + self.cell_size,
                                      outline="#263238", width=2)

    def color_cell(self, r, c, color, active=False):
        if GRID[r][c] == 1:
            return  # ne jamais repeindre un mur
        x0, y0, x1, y1 = self.cell_coords(r, c)
        tag = f"cell_{r}_{c}"
        self.canvas.delete(tag)
        outline = "#e65100" if active else "#b0bec5"
        width = 3 if active else 1
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline, width=width, tags=tag)
        label = ""
        if (r, c) == START:
            label = "DÉPART"
        elif (r, c) == END:
            label = "ARRIVÉE"
        if label:
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=label, font=("Arial", 9, "bold"), fill="#5d4037")
        self.cell_state[(r, c)] = color

    # ---------- Génération des étapes (simulation de solve()) ----------

    def generate_steps(self):
        visited = set()
        path = []

        def is_valid(r, c):
            if r < 0 or r >= ROWS or c < 0 or c >= COLS:
                return False
            if GRID[r][c] == 1:
                return False
            if (r, c) in visited:
                return False
            return True

        def solve(r, c):
            visited.add((r, c))
            path.append((r, c))
            self.steps.append(Step("visit", r, c, f"On arrive en ({r},{c}) : visited.add, path.append → path = {list(path)}.",
                                    COLOR_CURRENT, LINE_PATH_APPEND, list(path)))

            if (r, c) == END:
                self.steps.append(Step("found", r, c, f"({r},{c}) est la case ARRIVÉE ! On retourne True : chemin trouvé.",
                                        COLOR_SOLUTION, LINE_FOUND, list(path), found=True))
                return True

            self.steps.append(Step("loop", r, c, f"Pas encore arrivé. On va tester les 4 directions depuis ({r},{c}).",
                                    COLOR_CURRENT, LINE_LOOP_DIR, list(path)))

            for dr, dc, dir_name in DIRECTIONS:
                nr, nc = r + dr, c + dc
                ok = is_valid(nr, nc)
                reason = ""
                if not ok:
                    if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                        reason = "hors grille"
                    elif GRID[nr][nc] == 1:
                        reason = "c'est un mur"
                    else:
                        reason = "déjà visitée"
                msg = f"Direction {dir_name} → case ({nr},{nc}) : {'valide, on continue' if ok else 'invalide (' + reason + '), on saute'}."
                self.steps.append(Step("check", r, c, msg, COLOR_CURRENT, LINE_IS_VALID, list(path)))

                if not ok:
                    continue

                self.steps.append(Step("recurse", nr, nc, f"solve({nr},{nc}) → on descend dans cette direction.",
                                        COLOR_PATH, LINE_RECURSE, list(path)))

                if solve(nr, nc):
                    return True

            removed = path.pop()
            self.backtrack_count += 1
            msg = f"Aucune direction ne mène à la sortie depuis ({r},{c}) : IMPASSE. path.pop() retire {removed} → path = {list(path)}."
            self.steps.append(Step("backtrack", r, c, msg, COLOR_DEADEND, LINE_POP, list(path)))
            return False

        found = solve(START[0], START[1])
        if not found:
            self.steps.append(Step("nosolution", -1, -1, "Aucun chemin n'existe vers l'arrivée.", None, LINE_RETURN_FALSE, []))

    # ---------- Pilotage pas à pas ----------

    def start(self):
        self.draw_grid_base()
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.steps = []
        self.step_index = 0
        self.backtrack_count = 0
        self.generate_steps()

        self.start_btn.config(state="disabled")
        self.next_btn.config(state="normal")
        self.auto_btn.config(state="normal")
        self.progress_label.config(text=f"Étape 0 / {len(self.steps)}")
        self.backtrack_label.config(text="Retours en arrière : 0")
        self.status_label.config(text=f"{len(self.steps)} étapes prêtes. Avance pas à pas, ou lance la lecture auto.")
        self.next_step()

    def next_step(self):
        if self.step_index >= len(self.steps):
            self._finish()
            return

        step = self.steps[self.step_index]

        if step.kind == "nosolution":
            self.status_label.config(text=step.message)
            self._finish()
            return

        if step.kind == "backtrack":
            self.color_cell(step.r, step.c, COLOR_DEADEND)
            self.backtrack_label.config(text=f"Retours en arrière : {self.backtrack_count}")
        elif step.kind == "found":
            # Colore tout le chemin final en vert
            for (r, c) in step.path_snapshot:
                self.color_cell(r, c, COLOR_SOLUTION)
        else:
            self.color_cell(step.r, step.c, step.color)
            # Les cases déjà dans le chemin (hors la case active) repassent en bleu "chemin"
            for (r, c) in step.path_snapshot[:-1]:
                if (r, c) not in (START,):
                    self.color_cell(r, c, COLOR_PATH)
            if step.path_snapshot:
                last = step.path_snapshot[-1]
                self.color_cell(last[0], last[1], COLOR_CURRENT, active=True)

        self._highlight_line(step.code_line)
        self.log(step.message)
        self.status_label.config(text=step.message)
        self.stack_label.config(text=self._format_path(step.path_snapshot))
        if step.r >= 0:
            self.pos_label.config(text=f"({step.r}, {step.c})")

        self.step_index += 1
        self.progress_label.config(text=f"Étape {self.step_index} / {len(self.steps)}")

        if self.step_index >= len(self.steps):
            self._finish()

        if self.auto_playing:
            self.root.after(450, self.next_step)

    def _finish(self):
        last_msg = "Parcours terminé."
        if self.steps:
            last_step = self.steps[-1]
            if last_step.kind == "found":
                last_msg = "Chemin trouvé ! Le trajet vert est la solution retenue."
            elif last_step.kind == "nosolution":
                last_msg = last_step.message
        self.status_label.config(text=last_msg)
        self.next_btn.config(state="disabled")
        self.auto_btn.config(state="disabled")
        self.auto_playing = False

    def toggle_auto(self):
        self.auto_playing = not self.auto_playing
        if self.auto_playing:
            self.auto_btn.config(text="⏸ Pause")
            self.next_btn.config(state="disabled")
            self.next_step()
        else:
            self.auto_btn.config(text="Lecture auto")
            self.next_btn.config(state="normal")

    def reset(self):
        self.draw_grid_base()
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self.stack_label.config(text="vide")
        self.pos_label.config(text="—")
        self.code_text.configure(state="normal")
        self.code_text.tag_remove("highlight", "1.0", "end")
        self.code_text.configure(state="disabled")
        self.steps = []
        self.step_index = 0
        self.backtrack_count = 0
        self.auto_playing = False
        self.progress_label.config(text="Étape 0 / 0")
        self.backtrack_label.config(text="Retours en arrière : 0")
        self.start_btn.config(state="normal")
        self.next_btn.config(state="disabled", text="Étape suivante ▶")
        self.auto_btn.config(state="disabled", text="Lecture auto")
        self.status_label.config(text="Clique sur Démarrer pour commencer.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeBacktrackVisualizer(root)
    root.update_idletasks()
    req_w = root.winfo_reqwidth()
    req_h = root.winfo_reqheight()
    root.geometry(f"{req_w}x{req_h}")
    root.minsize(req_w, req_h)
    root.mainloop()
