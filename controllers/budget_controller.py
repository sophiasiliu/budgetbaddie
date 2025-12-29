# controllers/budget_controller.py

from utils.storage import save_envelopes, load_envelopes, save_settings, load_settings
from models.envelopes import Envelope, apply_recurrence

class BudgetController:
    def __init__(self):
        self.envelopes = load_envelopes()
        settings = load_settings()
        self.money_to_budget = settings.get("money_to_budget", 0)  

    def set_money_to_budget(self, amount):
        self.money_to_budget = float(amount)
        save_settings(self.money_to_budget)

    def add_envelope(self, name, category, budget, emoji, recurrence):
        self.envelopes.append(
            Envelope(
                name=name,
                category=category,
                budget=float(budget),
                emoji=emoji,
                recurrence=recurrence
            )
        )
        save_envelopes(self.envelopes)

    def delete_envelope(self, name):
        self.envelopes = [e for e in self.envelopes if e.name != name]
        save_envelopes(self.envelopes)

    def spend(self, name, amount):
        """Take money from envelope."""
        for e in self.envelopes:
            if e.name == name:
                e.balance -= float(amount)   # reduce current cash
                e.spent += float(amount)     # record spending
                break
        save_envelopes(self.envelopes)

    def add_cash(self, name, amount):
        """Stuff money from money_to_budget into envelope."""
        amount = float(amount)
        if amount > self.money_to_budget:
            raise ValueError("Not enough cash to stuff envelope!")
        for e in self.envelopes:
            if e.name == name:
                e.balance += amount
                break
        self.money_to_budget -= amount  # subtract from money_to_budget
        save_envelopes(self.envelopes)
        save_settings(self.money_to_budget)

    def reset_all(self):
        apply_recurrence(self.envelopes)
        save_envelopes(self.envelopes)
        self.money_to_budget = 0 # think about this
        save_settings(self.money_to_budget)
