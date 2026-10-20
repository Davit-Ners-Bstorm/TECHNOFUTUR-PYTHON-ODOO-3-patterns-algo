import tkinter as tk

VALUES = ["A", "B", "C"]

# Couleurs avec une signification fixe (légende affichée à l'écran)
COLOR_EXPLORING = "#ffb74d"   # orange : ce nœud est actif RIGHT NOW (ligne en cours sur lui)
COLOR_DONE = "#cfd8dc"        # gris-bleu clair : ce nœud a été visité mais on est reparti ailleurs
COLOR_SOLUTION = "#81c784"    # vert : combinaison complète valide
COLOR_BACKTRACK = "#e57373"   # rouge : on vient juste de revenir en arrière sur ce nœud
ACTIVE_OUTLINE = "#1565c0"    # contour bleu épais : LE nœud où l'exécution se trouve maintenant
EDGE_DEFAULT = "#9e9e9e"      # arête grise : chemin déjà visité
EDGE_ACTIVE = "#1565c0"       # arête bleue : chemin actuellement actif (de la racine au nœud courant)

# Le squelette de code affiché aux élèves, ligne par ligne.
# C'est volontairement le code "nu" (sans gestion x/y/tkinter) pour qu'ils
# voient exactement la logique du backtracking, rien d'autre.
CODE_LINES = [
    "def backtrack(path=None):",                         # 0
    "    if path is None:",                               # 1
    "        path = []",                                  # 2
    "",                                                    # 3
    "    if len(path) == len(VALUES):",                   # 4
    "        print(path, \"=> solution complète\")",       # 5
    "        return",                                      # 6
    "",                                                    # 7
    "    for v in VALUES:",                                # 8
    "        if v not in path:",                           # 9
    "            path.append(v)      # on choisit v",      # 10
    "            backtrack(path)     # on descend",        # 11
    "            path.pop()          # on revient (backtrack)",  # 12
]

# Lignes associées à chaque type d'étape (voir generate_steps)
LINE_ENTER_CHECK_NONE = 1      # if path is None / path = []
LINE_ENTER_CHECK_LEN = 4       # if len(path) == len(VALUES)
LINE_LEAF = 5                  # print(...) => solution
LINE_LOOP = 8                  # for v in VALUES
LINE_IF_NOT_IN = 9             # if v not in path
LINE_APPEND = 10               # path.append(v)
LINE_RECURSE = 11              # backtrack(path)
LINE_POP = 12                  # path.pop()


class Step:
    """Une étape = une action atomique du backtracking : ce qu'on dessine,
    ce qu'on écrit dans le journal, ET quelle ligne de code est en train
    de s'exécuter.

    active_path : liste de positions (x, y) du chemin racine -> nœud actif,
    utilisée pour colorer les arêtes du trajet courant en bleu.
    """
    def __init__(self, x, y, label, parent_pos, message, color, path_snapshot, code_line, active_path):
        self.x = x
        self.y = y
        self.label = label
        self.parent_pos = parent_pos
        self.message = message
        self.color = color
        self.path_snapshot = path_snapshot
        self.code_line = code_line
        self.active_path = active_path


class BacktrackingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Backtracking Visualizer — pas à pas")

        # --- Zone d'arbre (haut, pleine largeur) ---
        self.canvas = tk.Canvas(root, width=900, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5))

        # --- Panneau de code (bas gauche) ---
        code_frame = tk.Frame(root, bg="#1e1e1e")
        code_frame.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="nsew")

        tk.Label(code_frame, text="Code en train de s'exécuter", font=("Arial", 11, "bold"),
                 bg="#1e1e1e", fg="white").pack(anchor="w", padx=8, pady=(6, 2))

        self.code_text = tk.Text(code_frame, width=46, height=11, font=("Consolas", 11),
                                  bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
                                  state="disabled", borderwidth=0, highlightthickness=0)
        self.code_text.pack(padx=8, pady=(0, 8))
        self.code_text.tag_configure("highlight", background="#264f78", foreground="white")
        self._render_code()

        # --- Panneau pile + journal (bas droite) ---
        side = tk.Frame(root)
        side.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="nsew")

        tk.Label(side, text="Pile actuelle (path)", font=("Arial", 11, "bold")).pack(anchor="w")
        self.stack_label = tk.Label(side, text="[]", font=("Consolas", 13), fg="#1565c0")
        self.stack_label.pack(anchor="w", pady=(0, 8))

        tk.Label(side, text="Journal des étapes", font=("Arial", 11, "bold")).pack(anchor="w")
        self.log_text = tk.Text(side, width=44, height=8, font=("Consolas", 10), state="disabled", wrap="word")
        self.log_text.pack()

        # --- Légende ---
        legend = tk.Frame(root)
        legend.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        self._legend_item(legend, COLOR_EXPLORING, "nœud actif (en cours)")
        self._legend_item(legend, COLOR_DONE, "déjà visité, en attente")
        self._legend_item(legend, COLOR_SOLUTION, "combinaison complète")
        self._legend_item(legend, COLOR_BACKTRACK, "retour arrière (pop)")
        self._legend_item(legend, COLOR_DONE, "contour bleu épais = position courante", outline=ACTIVE_OUTLINE, outline_width=3)

        # --- Compteurs de progression ---
        progress_frame = tk.Frame(root)
        progress_frame.grid(row=3, column=0, columnspan=2, pady=(8, 0))
        self.progress_label = tk.Label(progress_frame, text="Étape 0 / 0", font=("Arial", 9), fg="#555")
        self.progress_label.pack(side="left", padx=15)
        self.solutions_label = tk.Label(progress_frame, text="Combinaisons complètes trouvées : 0 / 0", font=("Arial", 9, "bold"), fg="#2e7d32")
        self.solutions_label.pack(side="left", padx=15)

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
        self.edges_drawn = []
        self.auto_playing = False
        self.previous_active_pos = None
        self.node_final_colors = {}
        self.node_labels = {}
        self.solutions_found = 0
        self.total_solutions = self._factorial(len(VALUES))

    def _legend_item(self, parent, color, text, outline="black", outline_width=1):
        f = tk.Frame(parent)
        f.pack(side="left", padx=8)
        c = tk.Canvas(f, width=18, height=18, highlightthickness=0)
        c.create_oval(2, 2, 16, 16, fill=color, outline=outline, width=outline_width)
        c.pack(side="left")
        tk.Label(f, text=text, font=("Arial", 9)).pack(side="left", padx=3)

    @staticmethod
    def _factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

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

    # ---------- Génération de toutes les étapes (sans dessiner) ----------
    # Chaque étape correspond très précisément à une ligne du squelette
    # de code affiché : c'est ce qui permet la synchronisation.

    def generate_steps(self, path=None, depth=0, x=450, y=35, parent_pos=None, ancestors=None):
        if path is None:
            path = []
        if ancestors is None:
            ancestors = []

        label = "".join(path) if path else "∅"
        current_pos = (x, y)
        active_path = ancestors + [current_pos]

        # ligne "if len(path) == len(VALUES)"
        msg = f"On vérifie : len(path) == len(VALUES) ? Pile actuelle = {path}."
        self.steps.append(Step(x, y, label, parent_pos, msg, COLOR_EXPLORING, list(path), LINE_ENTER_CHECK_LEN, active_path))

        if len(path) == len(VALUES):
            msg = f"Oui ! Pile = {path}, taille = {len(VALUES)} → on affiche la solution et on return."
            self.steps.append(Step(x, y, label, parent_pos, msg, COLOR_SOLUTION, list(path), LINE_LEAF, active_path))
            return

        msg = "Non, il manque des lettres. On entre dans la boucle : for v in VALUES."
        self.steps.append(Step(x, y, label, parent_pos, msg, COLOR_EXPLORING, list(path), LINE_LOOP, active_path))

        spacing = 220 // (depth + 1)
        available = [v for v in VALUES if v not in path]
        start_x = x - spacing * (len(available) - 1) / 2
        child_index = 0

        for v in VALUES:
            in_path = v in path
            msg = f"On teste : \"{v}\" not in path ({path}) → {'Faux, on saute' if in_path else 'Vrai, on continue'}."
            self.steps.append(Step(x, y, label, parent_pos, msg, COLOR_EXPLORING, list(path), LINE_IF_NOT_IN, active_path))

            if in_path:
                continue

            child_x = start_x + child_index * spacing
            child_y = y + 90
            child_index += 1

            path.append(v)
            msg = f"path.append(\"{v}\") → path = {path}. On choisit cette branche."
            self.steps.append(Step(child_x, child_y, "".join(path), current_pos, msg, COLOR_EXPLORING, list(path), LINE_APPEND, active_path + [(child_x, child_y)]))

            msg = f"backtrack(path) → on appelle récursivement la fonction avec path = {path}."
            self.steps.append(Step(child_x, child_y, "".join(path), current_pos, msg, COLOR_EXPLORING, list(path), LINE_RECURSE, active_path + [(child_x, child_y)]))

            self.generate_steps(path, depth + 1, child_x, child_y, current_pos, active_path)

            removed = path.pop()
            msg = f"De retour sur \"{label}\" : path.pop() retire \"{removed}\" → path = {path}."
            self.steps.append(Step(x, y, label, parent_pos, msg, COLOR_BACKTRACK, list(path), LINE_POP, active_path))

    # ---------- Dessin ----------

    def draw_node(self, x, y, text, color, active=False):
        radius = 22
        tag = f"node_{x}_{y}"
        self.canvas.delete(tag)
        outline_color = ACTIVE_OUTLINE if active else "black"
        outline_width = 4 if active else 2
        self.canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline=outline_color, width=outline_width, tags=tag
        )
        self.canvas.create_text(x, y, text=text, font=("Arial", 12, "bold"), tags=tag)
        self.canvas.tag_raise(tag)

    def draw_edge(self, x1, y1, x2, y2):
        key = (x1, y1, x2, y2)
        if key in self.edges_drawn:
            return
        self.edges_drawn.append(key)
        tag = f"edge_{x1}_{y1}_{x2}_{y2}"
        self.canvas.create_line(x1, y1 + 22, x2, y2 - 22, arrow=tk.LAST, fill=EDGE_DEFAULT, width=2, tags=tag)

    def recolor_edges(self, active_path):
        """Repasse toutes les arêtes en gris, puis colore en bleu celles qui
        relient deux nœuds consécutifs du chemin actif (racine -> nœud courant)."""
        active_pairs = set(zip(active_path[:-1], active_path[1:]))
        for (x1, y1, x2, y2) in self.edges_drawn:
            tag = f"edge_{x1}_{y1}_{x2}_{y2}"
            is_active = ((x1, y1), (x2, y2)) in active_pairs
            color = EDGE_ACTIVE if is_active else EDGE_DEFAULT
            width = 3 if is_active else 2
            self.canvas.itemconfig(tag, fill=color, width=width)

    def log(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{self.step_index}. {message}\n\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def update_stack_display(self, path_snapshot):
        self.stack_label.config(text=str(path_snapshot) if path_snapshot else "[]")

    # ---------- Pilotage pas à pas ----------

    def start(self):
        self.canvas.delete("all")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

        self.steps = []
        self.step_index = 0
        self.edges_drawn = []
        self.previous_active_pos = None
        self.node_final_colors = {}
        self.node_labels = {}
        self.solutions_found = 0
        self.solutions_label.config(text=f"Combinaisons complètes trouvées : 0 / {self.total_solutions}")
        self.generate_steps()

        self.start_btn.config(state="disabled")
        self.next_btn.config(state="normal")
        self.auto_btn.config(state="normal")
        self.progress_label.config(text=f"Étape 0 / {len(self.steps)}")
        self.status_label.config(text=f"{len(self.steps)} étapes prêtes. Avance pas à pas, ou lance la lecture auto.")
        self.next_step()

    def next_step(self):
        if self.step_index >= len(self.steps):
            self._finish()
            return

        step = self.steps[self.step_index]

        # Le nœud qui était actif à l'étape précédente redevient neutre
        # (sauf s'il s'agit d'une solution validée ou d'un retour très récent,
        # qu'on garde affiché un court instant pour que ça se voie).
        if self.previous_active_pos is not None and self.previous_active_pos != (step.x, step.y):
            prev_color = self.node_final_colors.get(self.previous_active_pos, COLOR_DONE)
            if prev_color not in (COLOR_SOLUTION,):
                prev_color = COLOR_DONE
            self.draw_node(self.previous_active_pos[0], self.previous_active_pos[1],
                            self.node_labels.get(self.previous_active_pos, ""), prev_color, active=False)
            self.node_final_colors[self.previous_active_pos] = prev_color

        if step.parent_pos is not None:
            self.draw_edge(step.parent_pos[0], step.parent_pos[1], step.x, step.y)

        self.recolor_edges(step.active_path)
        self.draw_node(step.x, step.y, step.label, step.color, active=True)
        self.node_labels[(step.x, step.y)] = step.label
        self.node_final_colors[(step.x, step.y)] = step.color
        self.previous_active_pos = (step.x, step.y)

        self.update_stack_display(step.path_snapshot)
        self._highlight_line(step.code_line)
        self.log(step.message)
        self.status_label.config(text=step.message)

        if step.code_line == LINE_LEAF:
            self.solutions_found += 1
            self.solutions_label.config(text=f"Combinaisons complètes trouvées : {self.solutions_found} / {self.total_solutions}")

        self.step_index += 1
        self.progress_label.config(text=f"Étape {self.step_index} / {len(self.steps)}")

        if self.step_index >= len(self.steps):
            self._finish()

        if self.auto_playing:
            self.root.after(1000, self.next_step)

    def _finish(self):
        self.status_label.config(text="Parcours terminé : toutes les combinaisons ont été explorées.")
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
        self.canvas.delete("all")
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self.stack_label.config(text="[]")
        self.code_text.configure(state="normal")
        self.code_text.tag_remove("highlight", "1.0", "end")
        self.code_text.configure(state="disabled")
        self.steps = []
        self.step_index = 0
        self.edges_drawn = []
        self.auto_playing = False
        self.previous_active_pos = None
        self.node_final_colors = {}
        self.node_labels = {}
        self.solutions_found = 0
        self.progress_label.config(text="Étape 0 / 0")
        self.solutions_label.config(text=f"Combinaisons complètes trouvées : 0 / {self.total_solutions}")
        self.start_btn.config(state="normal")
        self.next_btn.config(state="disabled", text="Étape suivante ▶")
        self.auto_btn.config(state="disabled", text="Lecture auto")
        self.status_label.config(text="Clique sur Démarrer pour commencer.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("960x800")
    root.minsize(900, 680)
    app = BacktrackingVisualizer(root)
    root.mainloop()
