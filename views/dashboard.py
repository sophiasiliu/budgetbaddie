# views/dashboard.py

import tkinter as tk
from tkinter import ttk, simpledialog
from controllers.budget_controller import BudgetController

EMOJIS = ["💵","🛒","🚗","🏠","🍔","🐶","🎉","👜","📚","❤️","💄"]

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.envelope_widgets = {}
        self.title("Budget Baddie 👛")
        self.geometry("850x650")
        self.configure(bg="white")
        self.controller = BudgetController()

        style = ttk.Style()
        style.theme_use("clam")  # needed for custom colors
        style.configure("White.TFrame", background="white")
        style.configure("White.TLabel", background="white")

        # ====== PINK ROUNDED PROGRESS BAR STYLE ======
        style = ttk.Style()
        style.configure("White.TFrame", background="white")
        style.theme_use('clam')  # clam theme supports rounded progress bars
        style.configure(
            "Pink.Horizontal.TProgressbar",
            troughcolor="#f0f0f0",   # background (empty)
            background="#ff69b4",    # fill color (pink)
            thickness=20,            # bar height
            bordercolor="#f0f0f0",   # optional border
            lightcolor="#ff69b4",    # optional highlight
            darkcolor="#ff69b4"      # optional shadow
        )
        # ============================================

        # Pink ttk button
        style.configure(
            "Pink.TButton",
            background="#f5b3d4",   # button fill
            foreground="white",     # text color
            font=("Helvetica", 10, "bold"),
            borderwidth=0,
            focusthickness=3,
            focuscolor='none'
        )

        # Optional: change hover color
        style.map(
            "Pink.TButton",
            background=[("active", "#f9e7f0")],  # lighter pink on hover
            foreground=[("active", "white")]
        )
        self.draw_ui()

    def draw_ui(self):
        # To budget
        cash_frame = ttk.Frame(self, style="White.TFrame")
        cash_frame.pack(pady=10)

        tk.Label(cash_frame, text="Money To Budget:", bg="white").pack(side="left")

        self.cash_var = tk.StringVar(value=f"${self.controller.money_to_budget:.2f}")
        self.cash_entry = tk.Entry(cash_frame, textvariable=self.cash_var, width=10, bg="white")
        self.cash_entry.pack(side="left", padx=5)

        ttk.Button(cash_frame, text="Update Cash", command=self.update_money_to_budget, style="Pink.TButton").pack(side="left", padx=5)
        
        ttk.Button(self, text="Add Envelope", command=self.add_dialog, style="Pink.TButton").pack(pady=5)
        ttk.Button(self, text="Apply Recurrence", command=self.apply_recur, style="Pink.TButton").pack(pady=5)
        ttk.Button(self, text="Clear All", command=self.apply_clear_all, style="Pink.TButton").pack()
        self.list_frame = ttk.Frame(self, style="White.TFrame")
        self.list_frame.pack(fill="both", expand=True)
        self.refresh()


    def update_money_to_budget(self):
        # Remove $ if the user typed it
        raw_value = self.cash_var.get().replace("$", "").strip()
        try:
            amount = float(raw_value)
            self.controller.set_money_to_budget(amount)  # update controller data
            # Update display in Entry with $ and two decimals
            self.cash_var.set(f"${self.controller.money_to_budget:.2f}")
        except ValueError:
            # Reset to previous value if invalid input
            self.cash_var.set(f"${self.controller.money_to_budget:.2f}")

    def refresh(self):
        categories = ["fixed", "variable", "savings"]

        if not hasattr(self, "category_frames"):
            self.category_frames = {}
            self.envelope_widgets = {}

            for cat in categories:
                # Category header
                cat_label = tk.Label(
                    self.list_frame,
                    text=cat.capitalize(),
                    font=("Helvetica", 16, "bold"),
                    fg="#ff69b4",
                    bg="white"
                )
                cat_label.pack(anchor="w", pady=(10, 5), padx=10)

                # Container for this category
                rows_container = ttk.Frame(self.list_frame, style="White.TFrame")
                rows_container.pack(fill="x", padx=10)
                self.category_frames[cat] = rows_container

                # Create envelope rows
                for env in sorted(
                    [e for e in self.controller.envelopes if e.category.lower() == cat],
                    key=lambda x: x.name.lower()
                ):
                    self.create_envelope_row(env, rows_container)
        else:
            # Clear all category frames
            for frame in self.category_frames.values():
                for child in frame.winfo_children():
                    child.destroy()

            self.envelope_widgets = {}  # reset widget lookup

            # Recreate sorted envelope rows for each category
            for cat in categories:
                parent = self.category_frames[cat]
                for env in sorted(
                    [e for e in self.controller.envelopes if e.category.lower() == cat],
                    key=lambda x: x.name.lower()
                ):
                    self.create_envelope_row(env, parent)

    def add_dialog(self):
        import subprocess
        from tkinter import simpledialog

        def pick_apple_emoji():
            """Open macOS emoji picker and ask user to paste the selected emoji."""
            subprocess.run([
                "osascript",
                "-e",
                'tell application "System Events" to keystroke " " using {control down, command down}'
            ])
            emoji = simpledialog.askstring("Emoji", "Paste your selected emoji here:")
            return emoji or "💵"

        # Create the dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add Envelope 💌")
        dialog.geometry("300x450")

        # Envelope Name
        tk.Label(dialog, text="Envelope Name:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(dialog, textvariable=name_var).pack(pady=5)

        # Category Dropdown
        tk.Label(dialog, text="Category:").pack(pady=5)
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(dialog, textvariable=category_var, state="readonly")
        category_dropdown['values'] = ["variable", "fixed", "savings"]
        category_dropdown.current(0)
        category_dropdown.pack(pady=5)

        # Budget Amount
        tk.Label(dialog, text="Budget Amount:").pack(pady=5)
        budget_var = tk.StringVar(value="$0.00")
        tk.Entry(dialog, textvariable=budget_var).pack(pady=5)

        # Recurrence Dropdown
        tk.Label(dialog, text="Recurrence:").pack(pady=5)
        recur_var = tk.StringVar()
        recur_dropdown = ttk.Combobox(dialog, textvariable=recur_var, state="readonly")
        recur_dropdown['values'] = ["none", "daily", "weekly", "monthly"]
        recur_dropdown.current(0)
        recur_dropdown.pack(pady=5)

        # Emoji Picker Button
        tk.Label(dialog, text="Pick an Emoji:").pack(pady=5)
        emoji_var = tk.StringVar(value="💵")
        tk.Button(
            dialog, 
            text="Pick Emoji 🍎", 
            command=lambda: emoji_var.set(pick_apple_emoji())
        ).pack(pady=5)

        # Display currently selected emoji
        emoji_display = tk.Label(dialog, textvariable=emoji_var, font=("Apple Color Emoji", 20))
        emoji_display.pack(pady=5)

        # Submit Button
        def submit():
            name = name_var.get()
            category = category_var.get()
            recurrence = recur_var.get()
            emoji = emoji_var.get()

            raw_budget = budget_var.get().replace("$", "").strip()
            try:
                budget = float(raw_budget)
            except ValueError:
                tk.messagebox.showerror("Error", "Enter a valid number for budget!")
                return

            if name and category:
                try:
                    self.controller.add_envelope(name, category, budget, emoji, recurrence)
                except ValueError as e:
                    tk.messagebox.showerror("Error", str(e))
                    return
                self.refresh()
                self.show_overview()
                dialog.destroy()

        tk.Button(dialog, text="Add Envelope", command=submit).pack(pady=10)

    def spend_dialog(self, env):
        dialog = tk.Toplevel(self)
        dialog.title(f"Spend from {env.name} {env.emoji}")
        dialog.geometry("300x230")
        dialog.configure(bg="white")

        tk.Label(dialog, text=f"Spending from: {env.name} {env.emoji}", bg="white").pack(pady=(15, 5))

        tk.Label(dialog, text="Amount to spend:", bg="white").pack()
        amount_var = tk.StringVar(value="$0.00")
        tk.Entry(dialog, textvariable=amount_var, width=10, bg="white").pack(pady=5)

        # --- Standard spend of typed amount ---
        def confirm_spend(amount=None):
            try:
                if amount is None:     # user manually entered value
                    amount = float(amount_var.get().replace("$", "").strip())

                # Spend, and clamp so we never overspend
                amount = min(amount, env.budget)

                if amount <= 0:
                    tk.messagebox.showerror("Error", "Not enough in envelope to spend!")
                    return

                self.controller.spend(env.name, amount)

                # update UI & close
                self.update_envelope_row(env)
                dialog.destroy()

            except ValueError:
                tk.messagebox.showerror("Error", "Enter a valid number!")

        # --- NEW: spend everything currently in the envelope ---
        def spend_all():
            if env.balance <= 0:
                tk.messagebox.showinfo("Empty", "This envelope is already empty!")
                return
            confirm_spend(env.balance)

        ttk.Button(dialog, text="Spend", command=lambda: confirm_spend(), style="Pink.TButton").pack(pady=8)
        ttk.Button(dialog, text="Spend All", command=spend_all, style="Pink.TButton").pack(pady=4)

    def add_cash_dialog(self, env):
        dialog = tk.Toplevel(self)
        dialog.title(f"Add Cash to {env.name} {env.emoji}")
        dialog.geometry("300x200")
        dialog.configure(bg="white")

        tk.Label(dialog, text=f"Stuffing: {env.name} {env.emoji}", bg="white").pack(pady=(15, 5))
        tk.Label(dialog, text="Amount to add:", bg="white").pack()
        amount_var = tk.StringVar(value="$0.00")
        tk.Entry(dialog, textvariable=amount_var, width=10, bg="white").pack(pady=5)

        def confirm_add(amount=None):
            try:
                if amount is None:   # manual entry
                    amount = float(amount_var.get().replace("$", "").strip())

                self.controller.add_cash(env.name, amount)

                # update envelope row
                if env.name not in self.envelope_widgets:
                    self.create_envelope_row(env)
                else:
                    self.update_envelope_row(env)

                # refresh money-to-budget display
                self.cash_var.set(f"${self.controller.money_to_budget:.2f}")
                dialog.destroy()

            except ValueError:
                tk.messagebox.showerror("Error", "Enter a valid number or not enough cash!")
        def fill_envelope():
            remaining_needed = env.budget - env.balance
            if remaining_needed <= 0:
                tk.messagebox.showinfo("Already Full", "This envelope is already fully funded!")
                return

            # respect available money_to_budget
            amount = min(remaining_needed, self.controller.money_to_budget)
            if amount <= 0:
                tk.messagebox.showerror("Error", "No money available to budget!")
                return
            confirm_add(amount)

        ttk.Button(dialog, text="Add Cash", command=confirm_add, style="Pink.TButton").pack(pady=15)
        ttk.Button(dialog, text="Fill Envelope", command=fill_envelope, style="Pink.TButton").pack(pady=4)



    def delete(self, name, category):
        # Remove from controller
        self.controller.delete_envelope(name)

        # Remove from UI if it exists
        if name in self.envelope_widgets:
            widgets = self.envelope_widgets.pop(name)
            # any widget can tell us the parent frame — use name_label
            row_frame = widgets["name_label"].master
            row_frame.destroy()

    def apply_recur(self):
        self.controller.reset_all()
        self.refresh()

    def apply_clear_all(self):
        self.controller.clear()
        self.refresh()

    def pick_emoji(self):
        picker = tk.Toplevel(self)
        picker.title("Pick an emoji")
        emoji_var = tk.StringVar(value="💵")

        for emoji in EMOJIS:
            ttk.Radiobutton(picker, text=emoji, value=emoji, variable=emoji_var).pack(anchor="w")

        ttk.Button(picker, text="Select", command=picker.destroy, style="Pink.TButton").pack()
        picker.wait_window()
        return emoji_var.get()
    
    def show_overview(self):
        """Show all envelopes in a full table window."""
        overview = tk.Toplevel(self)
        overview.title("All Envelopes 📋")
        overview.geometry("700x450")

        cols = ("emoji", "name", "category", "budget", "spent", "remaining", "recurrence")

        tree = ttk.Treeview(overview, columns=cols, show="headings")
        tree.pack(fill="both", expand=True)

        # column headings & widths
        widths = [60, 150, 120, 100, 100, 120, 120]
        for col, w in zip(cols, widths):
            tree.heading(col, text=col.title())
            tree.column(col, width=w, anchor="center")

        # insert rows
        for env in self.controller.envelopes:
            remaining = env.budget - env.spent
            tree.insert(
                "",
                "end",
                values=(
                    env.emoji,
                    env.name,
                    env.category,
                    f"${env.budget:.2f}",
                    f"${env.spent:.2f}",
                    f"${remaining:.2f}",
                    env.recurrence
                )
            )

    def edit_dialog(self, env):
        dialog = tk.Toplevel(self)
        dialog.title("Edit 💌")
        dialog.geometry("300x260")

        tk.Label(dialog, text=f"Envelope: {env.name}").pack(pady=5)

        # --- Edit goal ---
        tk.Label(dialog, text="Edit Goal Amount:").pack(pady=5)
        new_goal_var = tk.StringVar(value=env.budget)
        tk.Entry(dialog, textvariable=new_goal_var).pack(pady=5)

        # --- Edit emoji ---
        tk.Label(dialog, text="Edit Emoji:").pack(pady=5)
        new_emoji_var = tk.StringVar(value=env.emoji)
        tk.Entry(dialog, textvariable=new_emoji_var, width=4, font=("Arial", 18)).pack()

        # --- Delete envelope ---
        def confirm_delete():
            # Remove from controller
            self.controller.delete_envelope(env.name)

            # Remove from UI
            if env.name in self.envelope_widgets:
                widgets = self.envelope_widgets.pop(env.name)
                # any widget can tell us the parent frame — use name_label
                row_frame = widgets["name_label"].master
                row_frame.destroy()

            dialog.destroy()

        # --- Update goal + emoji ---
        def edit_goal_and_emoji():
            raw_value = new_goal_var.get().strip()
            if raw_value == "":
                # user cleared field — handle it gracefully
                return
            # update it user entered new value
            try:
                new_budget = float(raw_value)
            except ValueError:
                tk.messagebox.showerror("Error", "Goal must be a valid number.")
                return

            # apply update
            env.budget = new_budget

            # Update emoji if changed
            new_emoji = new_emoji_var.get().strip()
            if new_emoji:
                env.emoji = new_emoji

            # Save + refresh UI
            from utils.storage import save_envelopes
            save_envelopes(self.controller.envelopes)
            self.update_envelope_row(env)
            dialog.destroy()

        ttk.Button(dialog, text="Delete Envelope", command=confirm_delete, style="Pink.TButton").pack(pady=5)
        ttk.Button(dialog, text="Update", command=edit_goal_and_emoji, style="Pink.TButton").pack(pady=5)

    def create_envelope_row(self, env, parent):
        frame = ttk.Frame(parent, style="White.TFrame")
        frame.pack(fill='x', pady=4, padx=10)
        frame.grid_columnconfigure(2, weight=1)

        # Name + emoji
        name_label = ttk.Label(frame, text=f"{env.emoji} {env.name}", style="White.TLabel")
        name_label.grid(row=0, column=0, padx=(0,10), sticky="w")

        # Balance / Goal
        balance_label = ttk.Label(frame, text=f"${env.balance:.2f} / ${env.budget:.2f}", style="White.TLabel")
        balance_label.grid(row=0, column=1, padx=10, sticky="w")

        # Progress bar
        progress = ttk.Progressbar(frame, value=env.progress() * 100, style="Pink.Horizontal.TProgressbar")
        progress.grid(row=0, column=2, sticky="ew", padx=10)

        # Buttons
        ttk.Button(frame, text="Edit", command=lambda e=env: self.edit_dialog(e), style="Pink.TButton") \
            .grid(row=0, column=3, padx=5)
        ttk.Button(frame, text="Add Cash", command=lambda e=env: self.add_cash_dialog(e), style="Pink.TButton") \
            .grid(row=0, column=4, padx=5)
        ttk.Button(frame, text="Spend", command=lambda e=env: self.spend_dialog(e), style="Pink.TButton") \
            .grid(row=0, column=5, padx=5)

        # Store as a dictionary, not a tuple
        self.envelope_widgets[env.name] = {
            "name_label": name_label,
            "balance_label": balance_label,
            "progress_bar": progress,
            "category": env.category.lower()
        }

            
    def update_envelope_row(self, env):
        widgets = self.envelope_widgets[env.name]
        widgets["name_label"].config(text=f"{env.emoji} {env.name}")
        widgets["balance_label"].config(text=f"${env.balance:.2f} / ${env.budget:.2f}")
        widgets["progress_bar"].config(value=env.progress() * 100)

